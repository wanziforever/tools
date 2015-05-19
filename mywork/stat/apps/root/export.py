#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from datetime import datetime
from common import fileutil
from core import util
from model import *
from sqlalchemy.orm.exc import NoResultFound
from core.settings import settings
import hashlib
from common.types import Dict
from common.errors import ResourceNotFoundError

ROLE_ADMIN = 1


def get_modules(customer_id, db):
    q = db.query(Modules).filter('customerId=:customerId').\
        params(customerId = customer_id).first()
    return q.modules.split(',')


def get_modules_with_role(customer_id, role_id, db):
    modules = get_modules(customer_id, db)
    m = set()
    q = db.query(Permission).\
        filter('customerId=:customerId and roleId=:roleId').\
        params(customerId = customer_id, roleId = role_id)

    for p in q:
        m.add(p.module_name)

    return list(m.intersection(set(modules)))


def has_permission_on_function(customer_id, role_id, module_name, func_name, db):
    p = db.query(Permission)\
               .filter('customerId=:customerId and role_id=:roleId and module_name:module_name and func_name=:func_name')\
               .count()
    return p > 0

'''
def auth(fn, *q, **kv):
    @wraps(fn)
    def wrap(*q, **kv):
        auth_str = request.get_cookie('jamdeo_cloud_token')
        try:
            customer_id, user_id, role_id = valid_token(auth_str)
        except errors.AuthError as auth_error:
            return redirect('/api/login', 302)
        if(has_permission(customer_id, user_id, role_id, module_name=None, func_name=None)):
            fn(q, kv)
        else:
            raise errors.Authorization('no permission')
    return wrap

def has_permission(customer_id, user_id, role_id, module_name, func_name):
    return True
'''


def upload_file(upload_file, asset_type, db):
    base_path = 'asset'
    name, ext = os.path.splitext(upload_file.filename)
    saved_file_name = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
    if ext:
        ext = ext.lower()
        saved_file_name = '{0}{1}'.format(saved_file_name, ext)
    file_key = os.path.join(base_path, saved_file_name)
    fileutil.create_dir_if_not_exist(os.path.dirname(util.get_file_from_fs(file_key)))
    # save file
    buffer_size = 1024 * 1024 # 1M
    with open(util.get_file_from_fs(file_key), 'wb') as f:
        while True:
            buffer_content = upload_file.file.read(buffer_size)
            if buffer_content == '':
                break
            f.write(buffer_content)
    # persist into db
    asset = Asset()
    asset.asset_type = asset_type
    asset.file_key = file_key
    asset.file_type = ext
    asset.file_size = os.path.getsize(util.get_file_from_fs(file_key))
    asset.customer_id = 1
    asset.file_url = settings.STORE_BASE_URL + file_key.replace('\\', '/')
    db.add(asset)
    db.flush()
    return asset


def get_asset_by_id(asset_id, db):
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).one()
        return asset
    except NoResultFound:
        return None

#===============================================================================
# def get_user_by_name( username ):
#     if username != 'jamdeo':
#         return None
#     user = Dict()
#     user.customer_id = 1
#     user.user_id = 1
#     user.role_id = 1
#     user.name = 'jamdeo'
#
#     m = hashlib.md5()
#     m.update( 'test' )
#     encoded_password = m.hexdigest()
#     user.password = encoded_password
#     return user
#===============================================================================

def create_customer(customer, db):
    new_customer = Customer()
    new_customer.company = customer.company
    new_customer.url = customer.company
    new_customer.description = customer.description
    new_customer.address = customer.address
    db.add(new_customer)
    db.flush()
    return new_customer


def get_customer_by_id(customer_id, db):
    try:
        customer = db.query(Customer). \
            filter(Customer.id == customer_id). \
            one()
        return customer
    except NoResultFound:
        return None


def update_customer(customer, db):
    m_customer = get_customer_by_id(customer.id, db)
    if m_customer is None:
        raise ResourceNotFoundError('customer', str(customer.id))
    m_customer.company = customer.company
    m_customer.url = customer.url
    m_customer.description = customer.description
    m_customer.address = customer.address
    return m_customer


def delete_customer_by_id(customer_id, db):
    m_customer = get_customer_by_id(customer_id, db)
    if m_customer is None:
        raise ResourceNotFoundError('customer', str(customer_id))
    db.query(Customer). \
        filter(Customer.id == customer_id). \
        delete()


def create_user(user, db):
    new_user = User()
    new_user.customer_id = user.customer_id
    new_user.role_id = user.role_id
    new_user.name = user.name
    new_user.passwd = user.passwd
    new_user.nick_name = user.nick_name
    new_user.phone = user.phone
    new_user.email = user.email
    db.add(new_user)
    db.flush()
    return new_user


def get_user_by_id(user_id, db):
    try:
        user = db.query(User). \
            filter(User.id == user_id). \
            one()
        return user
    except NoResultFound:
        return None


def get_user_by_email(email, db):
    try:
        user = db.query(User). \
            filter(User.email == email). \
            one()
        return user
    except NoResultFound:
        return None


def get_user_by_name(name, db):
    try:
        user = db.query(User). \
            filter(User.name == name). \
            one()
        return user
    except NoResultFound:
        return None


def update_user(user, db):
    m_user = get_user_by_id(user.id, db)
    if m_user is None:
        raise ResourceNotFoundError('user', str(user.id))
    m_user.role_id = user.role_id
    m_user.name = user.name
    m_user.passwd = user.passwd
    m_user.nick_name = user.nick_name
    m_user.phone = user.phone
    m_user.email = user.email
    return m_user


def delete_user_by_id(user_id, db):
    user = get_user_by_id(user_id, db)
    if user is None:
        raise ResourceNotFoundError('user', str(user_id))
    db.query(User). \
        filter(User.id == user_id). \
        delete()


def create_role(role, db):
    new_role = Role()
    new_role.customer_id = role.customer_id
    new_role.name = role.name
    db.add(new_role)
    db.flush()
    return new_role


def get_role_by_id(role_id, db):
    try:
        role = db.query(Role).filter(Role.id == role_id).one()
        return role
    except NoResultFound:
        return None


def update_role(role, db):
    m_role = get_role_by_id(role.id, db)
    if m_role is None:
        raise ResourceNotFoundError('role', str(role.id))
    m_role.name = role.name
    return m_role


def delete_role_by_id(role_id, db):
    role = get_role_by_id(role_id, db)
    if role is None:
        raise ResourceNotFoundError('role', str(role_id))
    db.query(Role).filter(Role.id == role_id).delete()

