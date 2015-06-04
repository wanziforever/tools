#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
from core.settings import settings
from core.redis_util import create_redis_session, VodRedis
from core import request, response
from redis.exceptions import ConnectionError
from functools import wraps
import pickle
import time
import logging

logger = logging.getLogger('cache_service')

redis_session = create_redis_session()


def has_key(session, cur_request):
    return session.hexists(cur_request.fullpath,
                           cur_request.query_string)


def default_get_from_key(session, cur_request):
    return pickle.loads(session.hget(cur_request.fullpath, cur_request.query_string))


def default_set_data(session, cur_request, data):
    session.hset(cur_request.fullpath, cur_request.query_string, data)


def cache(timeout=3600, key_exist=has_key,
          get_from_key=default_get_from_key,
          set_data=default_set_data):
    def wrap(f):
        @wraps(f)
        def callback(*q, **kw):
            data = None
            expired  = 0
            cur_time = long(time.time())
            if key_exist(redis_session, request):
                result = get_from_key(redis_session, request)

                if result.get('expired', 0) <= cur_time:
                    # cache expired
                    data = f(*q, **kw)
                    expired = cur_time + timeout
                    set_data(redis_session, request,
                             pickle.dumps(dict(data=data, expired=expired)))
                else:
                    data = result['data']
                    expired = result['expired'] - cur_time
            else:
                data = f(*q, **kw)
                expired = cur_time + timeout
                if data:
                    set_data(redis_session, request,
                             pickle.dumps(dict(data=data, expired=expired)))
            if data and expired > 0:
                response.set_header('Cache-Control:max-age', expired)
                response.set_header('JAMDEO_HIT_CACHE', True)
                return data
        return callback
    return wraps

def Cache_Service():
    return create_redis_session()
        
