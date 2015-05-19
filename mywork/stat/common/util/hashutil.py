#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Nov 14, 2011

@author: mengchen
'''
from common.error.errors import AuthError
import doctest
import hashlib
import time

def md5(text):
    '''
    >>> md5('tester')
    'f5d1278e8109edd94e1e4197e04873b9'
    '''
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()

def generate_token(secret, expire_seconds, *parts):
    '''
    >>> import re
    >>> t = generate_token('!@#$', 3600, '111', '222', '333')
    >>> re.match('111:222:333:\\d{13}:\\S{32}', t) is not None
    True
    '''
    exp = str(long(time.time() + expire_seconds) * 1000)
    parts = list(parts)
    parts.append(exp)
    hash = md5(':'.join(parts + [secret]))
    return ':'.join(parts + [hash])

def validate_token(secret, token):
    '''
    for valid token, should return token parts
    >>> validate_token('!@#$', '111:222:333:9999999999999:16ab3d7ccad626b1e7d1f5e5ca28c706')
    ['111', '222', '333', '9999999999999']
    
    token is none
    >>> validate_token('!@#$', None)
    Traceback (most recent call last):
    ...
    AuthError: [AUTH_FAILED] Token not found.
    
    invalid part count
    >>> validate_token('!@#$', '3a4d92a1200aad406ac50377c7d863aa')
    Traceback (most recent call last):
    ...
    AuthError: [AUTH_FAILED] Invalid token 3a4d92a1200aad406ac50377c7d863aa.
    
    invalid hash
    >>> validate_token('!@#$', '111:222:333:1324022188000:bad_hash')
    Traceback (most recent call last):
    ...
    AuthError: [AUTH_FAILED] Invalid token 111:222:333:1324022188000:bad_hash.
    
    token expired
    >>> validate_token('!@#$', '111:222:333:1324019736000:314c5b13c821a858768bd6bb3c0c173e')
    Traceback (most recent call last):
    ...
    AuthError: [AUTH_FAILED] Token 111:222:333:1324019736000:314c5b13c821a858768bd6bb3c0c173e expired.
    '''
    if token is None:
        raise AuthError('Token not found.')
    parts = token.split(':')
    if len(parts) <= 2:
        raise AuthError('Invalid token %s.' % token)
    hash = parts[-1]
    exp = int(parts[-2])
    if md5(':'.join(parts[:-1] + [secret])) != hash:
        # invalid hash
        raise AuthError('Invalid token %s.' % token)
    if exp < time.time() * 1000:
        raise AuthError('Token %s expired.' % token)
    return parts[:-1]

if __name__ == '__main__':
    doctest.testmod()
    