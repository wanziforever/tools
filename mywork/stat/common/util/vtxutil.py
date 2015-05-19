#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jan 6, 2012

@author: mengchen
'''
from common import settings, log
from common.error.errors import CodedError, AuthError, UnknownError
from common.log import log_enter, log_return, log_error
from common.util import httputil, hashutil
from common.web.context import Context
from common.db import dbutils
from common.file.store import s3
import datetime
import doctest
import logging
import os
import web
import base64
import hashlib
import time

kernel_db = dbutils.KERNEL_DB

@log_enter('Calling api {api} with fields {fields} ...')
@log_return('[DEBUG] API {api} returned {ret}.')
@log_error('API {api} failed.')
def call_api(api, headers={}, **fields):
    url = 'http://%s/%s' % (settings.API_DOMAIN, api)
    r = httputil.curl(url, fields, headers, True)
    if hasattr(r, 'error'):
        raise CodedError(r.error, r['message'])
    return r

def call_internal_api(api, **fields):
    ctx = Context.curctx()
    key = generate_auth_key(ctx.publisher_id, ctx.manager_id, ctx.role)
    headers = { 'INTERNAL-AUTHORIZATION' : key }
    return call_api(api, headers, **fields)



def generate_token(publisher_id, user_id, role, password, expires):
    prefix = publisher_id + ':' + user_id + ':' + role + ':' + expires + ':'
    to_hash = prefix + password + ':' + 'VTX$NB#2011'
    m = hashlib.md5()
    m.update(to_hash)
    hash = m.hexdigest()
    to_encode = prefix + hash
    return base64.urlsafe_b64encode(to_encode).replace('=', '.')

def get_token(pub_id):
    rs = kernel_db.query('select * from Manager where role = "0" and publisherId = "%s"' % pub_id)
    try:
        if rs:
            manager = rs[0]
            if manager:
                expire = str(long(time.time() * 1000 + 3* 24 * 60 * 60 * 1000))
                token = generate_token(manager.publisherId, manager.id, manager.role, manager.passwd, expire)
                return token
            else:
                return None
    except IndexError:
        raise web.seeother('show_message?error=WrongPublisherId%20' + pub_id)


def get_internal_key_header():
    try:
        return web.ctx.env['HTTP_INTERNAL_AUTHORIZATION']
    except KeyError:
        logging.warn('Internal key header not found.')
        raise AuthError('Internal key not found.')

def get_module():
    return get_module_project()[0]

def get_module_project():
    dirname = os.path.abspath(__file__).split('/')[2]
    parts = dirname.split('-')
    if len(parts) == 1:
        return parts + [None]
    elif len(parts) == 2:
        return parts
    else:
        raise UnknownError('Failed to parse project dir %s.' % dirname)

def generate_auth_key(publisherId, managerId, role):
    return hashutil.generate_token(settings.SHARED_KEY, 30 * 60, publisherId, managerId, role)

def get_file_from_fs(key):
    return s3.get(key)

def hashid(id):
    '''
    >>> hashid('tester')
    'f5'
    '''
    return hashutil.md5(id)[:2]

def init_log(prefix):
    mod, proj = get_module_project()
    if proj is None:
        debug_log_file = '/var/log/%s/%s-debug.log' % (mod, prefix)
        warn_log_file = '/var/log/%s/%s-warn.log' % (mod, prefix)
    else:
        debug_log_file = '/var/log/%s-%s/%s-debug.log' % (mod, proj, prefix)
        warn_log_file = '/var/log/%s-%s/%s-warn.log' % (mod, proj, prefix)
    log.set_level(logging.DEBUG)
    log.add_console_handler(logging.DEBUG)
    log.add_file_handler(debug_log_file, logging.DEBUG)
    log.add_file_handler(warn_log_file, logging.WARN)
    
def monthstamp():
    '''
    >>> import re
    >>> re.match('\\d{6}', monthstamp()) is not None
    True
    '''
    return datetime.datetime.now().strftime('%Y%m')

def validate_auth_key(key):
    parts = hashutil.validate_token(settings.SHARED_KEY, key)
    if len(parts) != 4:
        raise AuthError('Invalid token %s.' % key)
    return parts[:3]

if __name__ == '__main__':
    doctest.testmod()
    