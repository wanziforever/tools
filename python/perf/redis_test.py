#!/usr/bin/env python

import redis
import pickle
import time

redis_host = "10.0.64.233"
redis_port = 6379

redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port,
                                  socket_timeout=5,
                                  db=0)

redis_session = redis.Redis(connection_pool=redis_pool)

if __name__ == "__main__":
    key = "1052::2094::16240"
    start = time.time() * 1000
    if redis_session.exists(key):
        raw = redis_session.get(key)
    else:
        print "data not exist"
    end = time.time() * 1000
    elapsed = end - start
    print "%s ms used"%elapsed
    
