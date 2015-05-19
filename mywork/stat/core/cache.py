#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__author__ = 'pliu'

from functools import wraps
import pickle

from core import response, request
from core import redis_util
import logging
from common.log import log_enter, log_error, log_return


redis_cache = redis_util.create_redis_session()
Cache_Service = redis_util.create_redis_session
# def cache(fn, key_prefix, timeout=3600):
#     @wraps(fn)
#     def decorate(*q, **kw):
#         key = _generate_key(fn, *q, **kw)
#         data = _get(key)
#         cache_tag = 'Hit Cache'
#         if not data:
#             cache_tag = 'Miss Cache'
#             data = fn(*q, **kw)
#             _put(key, data, timeout)
#         response.set_header('Cache-Control: max-age', timeout)
#         response.set_header('JAMDEO_CACHE', cache_tag)
#         return data
#     return decorate

def cache(timeout=3600, timeout_key='cache_time'):  
    def func_decorator(fn):
        @wraps(fn)
        def wrapper(*q, **kw):
            cache_time = timeout
            key = _generate_key(request.path, request.query_string)
            data = _get(key)
            cache_tag = 'Hit Cache'
            if not data:
                cache_tag = 'Miss Cache'
                data = fn(*q, **kw)
                if isinstance(data, dict) and data.has_key(timeout_key):
                    cache_time = data.get(timeout_key)
                _put(key, data, cache_time)
            response.set_header('Cache-Control: max-age', cache_time)
            response.set_header('JAMDEO_CACHE', cache_tag)
            return data
        return wrapper
    return func_decorator

def func_cache(key_prefix='',timeout_key='cache_time', 
    timeout=3600):
    def func_decorator(fn):
        def wrapper(*q, **kw):
            if kw.has_key('cache_key'):
                key = kw['cache_key']
            else:
                key = _generate_key(fn, *q, **kw)
            if key_prefix:
                key = key_prefix + '_' + key
            data = _get(key)
            cache_time = timeout
            if not data:
                data = fn(*q, **kw)
                logging.info('func_cache use result '
                    'from function for %s with result %s', 
                    key, data)
                if isinstance(data, dict) and data.has_key(timeout_key):
                    cache_time = data.get(timeout_key)
                _put(key, data, cache_time)
            else:
                logging.info('func_cache use cache  '
                    'for %s with result %s', key, data)
            return data
        return wrapper
    return func_decorator

@log_return('get from redis by key {key} return {ret}')
def _get(key):
    data = redis_cache.get(key)
    return data

@log_enter('set redis by key {key} with data {data}')
def _put(key, data, timeout):
    redis_cache.set(key, data)
    redis_cache.expire(key, timeout)

def _generate_key(fn_str, *q, **kw):
    """
    >>> _generate_key(max, 1, 2, '3', '4', a='1', b='c')
    "max_1,2,3,4_{'a': '1', 'b': 'c'}"
    """
    return '{0}_{1}_{2}'.format(fn_str, 
        ','.join([str(x) for x in q]), str(kw))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

