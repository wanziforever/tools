#!/usr/bin/env python

import redis
from settings import settings
import logging
from redis.exceptions import ConnectionError
import time
import cPickle as pickle

logger = logging.getLogger('cache_service')

redis_pool = redis.ConnectionPool(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT,
                                  socket_timeout=5,
                                  db=0)


class VodRedis(redis.Redis):
    """
    1.control redis using setting settings.REDIS_ENABLE
    2.if connection error, don't repeat connection within reconnect_timer
    """
    redis_enabled = True
    reconnect_timer = 10 # second
    connection_down_timestamp = 0

    def switch(self):
        redis_enabled = settings.REDIS_ENABLE
        logger.info("redis_enabled = %s"%redis_enabled)

    def execute_command(self, *args, **options):
        if not self.redis_enabled:
            return None
        try:
            ok_time = time.time() - (self.connection_down_timestamp 
                                        + self.reconnect_timer)
            if ok_time > 0:
                self.connection_down_timestamp = 0
                return super(VodRedis, self).execute_command(*args, **options)
            else:
                return None
        except ConnectionError, e:
            self.connection_down_timestamp = time.time()
            return None
    
    def get(self, key):
        raw_ret = super(VodRedis,self).get(key)
        if raw_ret:
            return pickle.loads(raw_ret)
        else:
            return None

    def _get_media_ids(self, value):
        media_ids = []
        if isinstance(value, dict):
            for k, v in value.items():
                    if isinstance(v, list):
                        for media in v:
                            if isinstance(media, dict) and media.has_key('id'):
                                media_ids.append(media.get('id'))

        return media_ids

    def _get_media_id_key(self, media_id):
        return media_id

    def index_media(self, media_id, key):
        ttl = 2 * 24 * 3600 # media index live 2 days, more than any api cache
        media_id_key = self._get_media_id_key(media_id)
        self.sadd(media_id_key, key)
        self.expire(media_id_key, ttl)


    def un_index_media(self, media_id):
        media_id_key = self._get_media_id_key(media_id)
        # remove api cache
        api_keys = self.smembers(media_id_key)
        if api_keys != set():
            self.delete(*api_keys)
        # remove current index
        self.delete(media_id_key)


    def set(self, key, value):
        super(VodRedis,self).set(key, pickle.dumps(value))
        # index media in cache
        #for media_id in self._get_media_ids(value):
        #    self.index_media(media_id, key)


redis_session = VodRedis(connection_pool=redis_pool)
redis_session.switch()
    
def create_redis_session():
    return redis_session



