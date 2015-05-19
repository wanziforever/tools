#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import time

__APP_TABLE = 'OAuth2App'
__OAUTH_TABLE = 'OAuth2Token'

def get_apps():
    return list(__get_db().select(__APP_TABLE, order='name'))

def create_app(name, description):
    '''
    Create new app.
    
    Returns:
      Created app object.
    '''
    current = __current_time()
    return __get_db().insert(__APP_TABLE, \
            id = __uuid(), \
            name = name, \
            description = description, \
            secretKey = __uuid(), \
            version = 0, \
            creationTime = current, \
            modifiedTime = current)

def update_app(appId, name, description):
    __get_db().update(__APP_TABLE, where='id=$id', vars=dict(id=appId), name=name, description=description)

def delete_app(appId):
    __get_db().delete(__APP_TABLE, where='id=$id', vars=dict(id=appId))

def get_oauth2_access_tokens():
    return list(__get_db().select(__APP_TABLE, order='creationTime desc'))

def create_oauth2_access_token(appId, publisherId, managerId, role):
    current = __current_time()
    return __get_db().insert(__OAUTH_TABLE,
            id = __uuid(), \
            publisherId = publisherId, \
            managerId = managerId, \
            role = role, \
            appId = appId, \
            accessToken = __uuid(), \
            expires = 2000000000000, \
            version = 0, \
            creationTime = current, \
            modifiedTime = current)

def delete_oauth2_access_token(access_token):
    __get_db().delete(__OAUTH_TABLE, where='accessToken=$token', vars=dict(token=access_token))

# private functions:

def __get_db():
    return db

def __uuid():
    return uuid.uuid4().hex

def __current_time():
    return int(time.time() * 1000)
