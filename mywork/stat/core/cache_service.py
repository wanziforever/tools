#!/usr/bin/env python

import redis
import logging
from redis.exceptions import ConnectionError
import time
logger = logging.getLogger('cache_service')
REDIS_HOST = 10.0.64.233
REDIS_PORT = 6379

redis_pool = redis.ConnectionPool(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  socket_timeout=5,
                                  db=0)
redis_session = VodRedis(connection_pool=redis_pool)

class LocalCache(object):
    def __init__(self):
        self.cache_hash = {}

    def get(self, key):
        if key not in self.cache_hash:
            return None
        return self.cache_hash[key]

    def set(self, key, value):
        self.cache_hash[key] = value
        return True
        
class CacheService(object):
    def __init__(self, local=True):
        self.session = None
        if local is True:
            self.session = LocalCache()
        else:
            try:
                self.session = VodRedis(connection_pool=redis_pool)
            except Exception,e :
                import traceback
                print traceback.format_exc()
                self.session = None

    def get(self, key):
        if self.session is None:
            return False
        return self.session.get(key)

    def set(self, key, value):
        if self.session is None:
            return False
        self.session.set(key, value)
        return True





