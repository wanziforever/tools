#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Nov 10, 2011

@author: mengchen
'''
from common import json2
from common.error import validation
from common.error.errors import ModNotFoundError, CodedError
from common.log import log_enter
from common.types import Dict, CiDict
from common.util import modutil, stringutil
import StringIO
import cgi
import doctest
import os
import re
import urllib
import urllib2

def build_fields(fields, use_json=False):
    '''
    >>> build_fields(None) is None
    True
    >>> build_fields({ 'id' : 1, 'name' : 'abc' })
    'id=1&name=abc'
    >>> build_fields({ 'id' : 1, 'name' : 'abc' }, True)
    'id=1&name=%22abc%22'
    '''
    if fields is None:
        return None
    if use_json:
        for k in fields:
            fields[k] = json2.dumps(fields[k])
    return urllib.urlencode(fields)

def curl(url, fields=None, headers=None, use_json=False, resp_headers={}):
    resp_headers.clear()
    req = _build_request(url, fields, headers, use_json)
    resp = _read_response(req, resp_headers)
    resp = _process_resp(resp, resp_headers, use_json)
    return resp

def _build_request(url, fields, headers, use_json):
    '''
    >>> req = _build_request('http://localhost/test', {'id':'1'}, {'INTERNAL-KEY':'abc'}, False)
    >>> req._Request__original
    'http://localhost/test'
    >>> req.data
    'id=1'
    >>> req.headers
    {'Internal-key': 'abc'}
    '''
    data = build_fields(fields, use_json)
    req = urllib2.Request(url, data)
    if headers is not None:
        for k, v in headers.items():
            req.add_header(k, v)
    return req

def _read_response(req, resp_headers):
    f = urllib2.urlopen(req)
    try:
        resp = f.read()
        info = f.info()
        headers = _parse_headers(info.headers)
        resp_headers.update(headers)
        return resp
    finally:
        f.close()		

def _parse_headers(header_list):
    '''
    >>> l = ['Server: nginx/0.7.67\\r\\n', 'Content-Type: application/json;charset=UTF-8\\r\\n']
    >>> headers = _parse_headers(l)
    >>> len(headers)
    2
    >>> h = headers['Server']
    >>> h.key, h.value
    ('Server', 'nginx/0.7.67')
    >>> h.params
    {}
    >>> h = headers['Content-Type']
    >>> h.key, h.value
    ('Content-Type', 'application/json')
    >>> h.params
    {'charset': 'UTF-8'}
    '''
    headers = CiDict()
    for line in header_list:
        main, params = cgi.parse_header(line)
        key, value = main.split(': ')
        headers[key] = Dict(key=key, value=value, params=params)
    return headers


def _process_resp(resp, resp_headers, use_json):
    '''
    >>> headers = CiDict()
    
    no mime type, should return raw response
    >>> _process_resp('abc', {}, False)
    'abc'
    
    charset not found, should use raw response
    >>> header = Dict(value='application/json', params=Dict())
    >>> headers['Content-Type'] = header
    >>> _process_resp('abc', headers, False)
    'abc'
    
    mime type is json, but use_json is False,
    should not decode by json
    >>> header = Dict(value='application/json', params=Dict(charset='utf-8'))
    >>> headers['Content-Type'] = header
    >>> _process_resp('abc', headers, False)
    u'abc'
    
    mime type is json, and use_json is True,
    should decode by json
    >>> header = Dict(value='application/json', params=Dict(charset='utf-8'))
    >>> headers['Content-Type'] = header
    >>> _process_resp('"abc"', headers, True)
    u'abc'
    '''
    content_type_header = resp_headers.get('content-type')
    if content_type_header is not None:
        mime, charset = _parse_content_type_header(content_type_header)
        if mime == 'text/html':
            charset = _parse_html_charset(resp) or charset
        if charset is not None:
            resp = unicode(resp, charset, 'ignore')
        if use_json and mime == 'application/json':
            resp = json2.loads(resp)   
    return resp

def _parse_content_type_header(header):
    '''
    normal situation
    >>> header = Dict(key='Content-Type', value='application/json', params=Dict(charset='UTF-8'))
    >>> _parse_content_type_header(header)
    ('application/json', 'UTF-8')
    
    no charset, should default to utf-8
    >>> header = Dict(key='Content-Type', value='application/json', params=Dict())
    >>> _parse_content_type_header(header)
    ('application/json', None)
    '''
    mime = header.value
    charset = header.params.get('charset')
    return mime, charset

def _parse_html_charset(resp):
    '''
    >>> html = '<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf-8" /></head></html>'
    >>> _parse_html_charset(html)
    'utf-8'
    
    >>> html = '<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf-8"></head></html>'
    >>> _parse_html_charset(html)
    'utf-8'
    
    >>> html = '<html></html>'
    >>> _parse_html_charset(html) is None
    True
    
    >>> html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    >>> _parse_html_charset(html)
    'utf-8'
    '''
    m = re.search('<meta http-equiv="Content-Type" content="text/html; ?charset=(\\S+)"', resp)
    return None if m is None else m.group(1)

@log_enter('Uploading file {path} ({os.path.getsize(path)} bytes) to {url} ...')
@validation.file_exists('path')
def upload(url, path, fields=None, headers=None, use_json=False):
    if modutil.exists('pycurl'):
        import pycurl
        url = stringutil.u2s(url)
        path = stringutil.u2s(path)
        if not os.path.exists(path):
            raise Exception('File "%s" not found.' % path)
        buffer = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.HEADER, 1)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.setopt(c.URL, url)
        field_list = [('file', (c.FORM_FILE, path))]
        if fields is not None:
            for k,v in fields.items():
                if use_json:
                    v = json2.dumps(v)
                field_list.append((k, v))
        c.setopt(c.HTTPPOST, field_list)
        if headers is not None:
            header_list = []
            for k, v in headers.items():
                header = '%s: %s' % (k, v)
                header = str(header) # header may be unicode, which is un-acceptable for curl
                header_list.append(header)
            c.setopt(c.HTTPHEADER, header_list)
        c.perform()
        code = c.getinfo(pycurl.HTTP_CODE)
        c.close()
        if code != 200:
            raise CodedError('UPLOAD_FAILED', 'Failed to upload file %s.' % path)
        resp = buffer.getvalue()
        if use_json:
            json = resp.splitlines()[-1]
            json = unicode(json, 'utf-8')
            resp = json2.loads(json)
        return resp
    else:
        raise ModNotFoundError('pycurl')

if __name__ == '__main__':
    doctest.testmod()
    