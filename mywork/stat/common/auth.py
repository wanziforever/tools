# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# '''
# provides a simple set of methods to implement Authentication and Authorization in web applications
# '''
# import time
# import logging
# import errors
# import urllib2
# # don't know why from core.settings import settings cannot work
# # but logutil.py can work which is in the same directory
# from core.settings import settings
# from functools import wraps
# from common.errors import AuthError
# from Crypto.Cipher import AES
# from base64 import urlsafe_b64decode, urlsafe_b64encode

# from .sac import SACService
# from .sac.ttypes import *
# from .sac.constants import *

# from thrift import Thrift
# from thrift.transport import TSocket
# from thrift.transport import TTransport
# from thrift.protocol import TBinaryProtocol

# log = logging.getLogger(__name__)


# __TOKEN = 'jamdeo-cloud#%^!'
# __MODE = AES.MODE_ECB
# __END = '_$END$_'

# cryptor = AES.new(__TOKEN, __MODE)
# auth_enable=settings.AUTH_ENABLE
# sac = None
# CONSOLE_TOKEN = "1q2w3e4r5t"
# appkey= "1175952793"
# apicode = ""

# def init_auth_service():
#     global sac
#     if settings.AUTH_ENABLE is False:
#         return True
#     server = settings.AUTH_SERVER
#     port = int(settings.AUTH_PORT)
    
#     try:
#         transport = TSocket.TSocket(server, port)
#         transport.open()
#         protocol = TBinaryProtocol.TBinaryProtocol(transport)
#         sac = SACService.Client(protocol)
#     except Thrift.TException, tx:
#         print "%s "%tx.message

# init_auth_service()

# def generate_token(expired, *parts):
#     '''
#     >>> s = generate_token(3600, 1, 1, 1)
#     >>> valid_token(s)
#     '1,1,1'
#     >>> generate_token(3600)
#     Traceback (most recent call last):
#     BadArgValueError: [INVALID_ARG_VALUE] Invalid value for parameter auth key. (_status_code="400", param="auth key")
#     '''
#     if len(parts) < 1:
#         raise errors.BadArgValueError('auth key')
#     expired_sec = expired + int(time.time())
#     parts = list(parts)
#     parts.insert(0, expired_sec)
#     parts.append(__END)
    
#     encrypt_str = ','.join(str(x) for x in parts)
#     str_len = len(encrypt_str)

#     if str_len % 16 > 0:
#         place_hold = 16 - str_len % 16
#         encrypt_str += place_hold * ' '
    
#     token = urlsafe_b64encode(cryptor.encrypt(encrypt_str))
#     return token

# def valid_token_in_request(request):
#     if settings.AUTH_ENABLE is False:
#         return True
#     token = _get_token_from_request(request)

#     if token is None:
#         raise AuthError(msg="no auth token provided")
#     # if the token is CONSOLE_TOKEN, let it go
#     if token == CONSOLE_TOKEN:
#         return True

#     ret = valid_token(token, apicode, appkey)
#     if ret is False:
#         return False
#     if ret.resultcode != 0:
#         log.info("fail to authenticate token %s"%token)
#         return False
    
# def valid_token(token, apicode, appkey):
#     if sac is None:
#         return False
#     return sac.apiAuth(token, apicode, appkey)

# def _get_token_from_request(request):
#     #token = _get_token_from_query(request)
#     #if token is None:
#     #    token = _get_token_from_header(request)
#     #if token is None:
#     #    token = _get_token_from_cookie(request)
#     return  _get_token_from_header(request)


# def _get_token_from_query(request):
#     token = request.query.token
#     if len(token) > 0:
#         log.info('get token from query string: token={0}'.format(token))
#         return token
#     return None

# def _get_token_from_cookie(request):
#     log.info('try to get token from cookie...')
#     token = request.get_cookie('X-JAMDEO-TOKEN')
#     if token is not None:
#         log.info('get token from cookie: {0}'.format(token))
#         return token
#     return None

# def _get_token_from_header(request):
#     """
#     header: {'Authzation': 'JamdeoLogin token=asdfasfdt'}
#     """
#     log.info('try to get token from header...')
#     #auth_value = request.get_header('Authorization')
#     #if auth_value is None:
#     #    return None
#     #log.info('Authorization header: {0}'.format(auth_value))
#     #schema = 'JamdeoLogin'
#     #if not auth_value.startswith(schema):
#     #    log.warn('invalid authorization value')
#     #    return None
#     #kvs = auth_value[auth_value.find(schema) + len(schema):].split(',')
#     #token = None
#     #for kv in kvs:
#     #    kv = kv.strip(' ').split('=', 1)
#     #    if len(kv) < 2:
#     #        continue
#     #    if kv[0] == 'token':
#     #        token = kv[1]
#     #        log.info('get token from Authorization header: {0}'.format(token))
#     token = request.get_header("H-T", None)
#     return token


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
