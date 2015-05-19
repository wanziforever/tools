#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import importlib

from datamodel.schema import SCHEMA
from datamodel.schema import get_cache_policy
from handler import default_db_get
from handler import default_db_update
from handler import default_db_insert
from handler import default_db_delete
from session import create_session, Session
from core.cache import Cache_Service
from df.data_descriptor import DataDesc
from contextlib import contextmanager
from .exceptions import NoSupportDataType
from functools import wraps
import logging
import time

logger = logging.getLogger('db_function')

db_down_timestamp = 0
db_reconnect_timer = 20 # second


def timed(f):
    ''' measure a execution time duration for a function, a threshold
    will be used to indicate whether print the alarm for function take
    a long time '''
    threshold = 500 # mseconds
    @wraps(f)
    def wrapper(*args, **kwds):
        start = int(round(time.time() * 1000))
        result = f(*args, **kwds)
        end =int(round(time.time() * 1000))
        elapsed = end - start
        if elapsed > threshold:
            logger.warn("-%s- %s took %d mseconds to finish" % \
                        (os.getpid(), f.__name__, elapsed))
        return result
    return wrapper

class DataFunctionException(Exception):
    def __init__(self, op, data_desc, msg):
        self.op = op
        self.msg = msg
        self.data_desc = data_desc

    def __str__(self):
        return "operation %s fail for error: %s"%(self.op, self.msg)

    def __repr__(self):
        return "operation fail for error"

# scan the request handler folder to find out all the handlers, and
# register the request to the system, the handler will use the schema
# name as register key
user_handler_map = {}
def registerUserHandlers():
    directory_for_handlers = os.path.dirname(__file__) + "/handler"
    handler_files = os.listdir(directory_for_handlers)
    handler_modules = []
    for file in handler_files:
        if not file.endswith(".py"):
            continue
        module_name, ext = os.path.splitext(file)
        try:
            handler_module = importlib.import_module("df.handler.{0}".format(module_name))
        except ImportError, e:
            logger.info("module {0} is not found".format(module_name))
            continue
        for attr in dir(handler_module):
            if not attr == "registerRequstHander":
                continue
            registerRequestHandler = getattr(handler_module, attr)
            schema_name, schema, handler = registerRequestHandler()
            logger.info("registering the schema %s(%d) to %s"%(schema_name,
                                                               schema,
                                                               handler.__name__))
            user_handler_map[schema] = handler

registerUserHandlers()

def make_cached_key(schema, datatype, keys):
    # pack parameters to:
    # connect schema::data_type::key1::key2::key3
    #keys = [str(data_desc.keys[i]) for i in xrange(1, len(data_desc.keys)+1)]
    sort_keys = [str(keys[key]) for key in sorted(keys.keys())]
    tokens = [str(schema), str(datatype)]
    tokens += sort_keys;
    return "::".join(tokens)

# every notify item handling will use a seperate session
def handle_notify_list(notify_list):
    logger.debug("enter notify_list handling function")
    for data_desc, mode in notify_list:
        cached_key = make_cached_key(data_desc.getSchema(),
                                     data_desc.getDataType(),
                                     data_desc.getKeys())
        logger.info("handler notification for key: %s"%(cached_key))
        if mode == "flush_cache":
            db_flush_cache(data_desc)
        elif mode == "reload":
            db_flush_cache(data_desc)
            db_get(data_desc)
        else:
            logger.warn("not support notify mode %s"%(mode))


@contextmanager
def db_session():
    session = None
    try:
        session = create_session()
        yield session
        session.commit()
    except:
        if session:
            session.rollback()
        logger.exception('error occurs')
    finally:
        Session.remove()

def db_mget(data_descriptor, session=None):
    '''to get multiple record , at the testing stage'''
    cache_time = get_cache_policy(data_descriptor.getSchema(),
                                  data_descriptor.getDataType())
    if cache_time < 0:
        cache_time = None

    cache = Cache_Service() if cache_time is not None else None

    if cache is None and data_descriptor.isCacheOnly():
        return None
        
    keys = data_descriptor.getmKey()
    if not isinstance(keys, (list, tuple)):
        return False

    cached_keys = [make_cached_key(data_descriptor.getSchema(),
                                   data_descriptor.getDataType(), k) \
                                   for k in keys]
    collection = []
    if cache is not None:
        collection = cache.mget(cached_keys)

    if data_descriptor.isCacheOnly():
        return collection
    
    keys_index_not_cached = [i for i, item in enumerate(collection) \
                                if item is None]
    keys_to_db = [keys[i] for i in keys_index_not_cached ]
    for i in keys_index_not_cached:
        data_desc = DataDesc(data_descriptor.getSchema(),
                             data_descriptor.getDataType())
        data_desc.setKey(i, keys[i])
        ret = db_get(data_desc, session)
        collection[i] = ret

    return collection
        
@timed    
def db_get(data_descriptor, session=None):
    cached_key = make_cached_key(data_descriptor.getSchema(),
                                 data_descriptor.getDataType(),
                                 data_descriptor.getKeys())
    cache = None
    # cache_time = 0 measn the cache will not timeout
    cache_time = get_cache_policy(data_descriptor.getSchema(),
                                   data_descriptor.getDataType())
    logger.debug ("configured cache_time is %s, cached_key is %s"%(cache_time, cached_key))
    if cache_time < 0:
        cache_time = None

    cache = Cache_Service() if cache_time is not None else None

    try:
        if cache is not None and cache.exists(cached_key):
            return cache.get(cached_key)
    except Exception, e:
        import traceback
        logger.error("exception from redis:\n %s"%traceback.format_exc())

    logger.debug("miss-cached for %s, continue to query database"%cached_key)
    schema = data_descriptor.getSchema()
    data_type = data_descriptor.getDataType()

    handler = None
    #if session is None:
    #    session = create_session()

    # firstly try the default handler, and if there is no support data
    # type found, try to use the user defined handler, this feature can
    # allow the the extention of the default schema to extent its datatype,
    # and better to give the named of the handler who exttended schema
    # a _ext suffix
    try_user_defined_handler = True
    if schema < SCHEMA.schema_default_end:
        try:
            handler = default_db_get(data_descriptor, session)
            try_user_defined_handler = False
        except NoSupportDataType:
            try_user_defined_handler = True
        
    if try_user_defined_handler is True:
        if schema in user_handler_map:
            handler = user_handler_map[schema]("get", data_descriptor, session)
        else:
            logger.error("data_function::db_get not support schema %s"%schema)
            return None

    if handler is None:
        return None
    result = handler.processQuery()
        
    if result is None:
        return None

    try:
        if isinstance(result, (list, tuple)):
            for i in result:
                handler.session.expunge(i)
        else:
            handler.session.expunge(result)
    except:
        pass
    finally:
        handler.cleanup()

    # sometime handler return a success : false result, don't cache it
    if isinstance(result, dict):
        if result.has_key("success"):
            if result["success"] is False:
                return result
            
    if cache is not None:
        cache.set(cached_key, result)
        if cache_time > 0:
            cache.expire(cached_key, cache_time)
        
    return result

@timed
def db_count(data_descriptor, session = None):
    schema = data_descriptor.getSchema()
    if schema < SCHEMA.schema_default_end:
        handler = default_db_get(data_descriptor, session)
    elif schema in user_handler_map:
        handler = user_handler_map[schema]("count", data_descriptor, session)
    else :
        print "data_function::db_get not support schema ", schema
        return None
    if handler is None:
        return None
    try:
        amount = handler.processCount()
    finally:
        handler.cleanup()
    return amount

@timed
def db_update(data_descriptor, session=None):
    schema = data_descriptor.getSchema()
    data_type = data_descriptor.getDataType()
    if schema < SCHEMA.schema_default_end:
        handler = default_db_update(data_descriptor, session)
    elif schema in user_handler_map:
        handler = user_handler_map[schema]("upd", data_descriptor, session)
    else:
        print "data_function::db_update not support schema ", schema
        return None
    if handler is None:
        return None
    try:
        handler.processUpdate()
        handle_notify_list(handler.notify_list)
    finally:
        handler.cleanup()

@timed
def db_insert(data_descriptor, session=None):
    schema = data_descriptor.getSchema()
    if schema < SCHEMA.schema_default_end:
        handler = default_db_insert(data_descriptor, session)
    elif schema in user_handler_map:
        handler = user_handler_map[schema]("insr", data_descriptor, session)
    else:
        print "data_function::db_insert not support schema ", schema
        return None
    try:
        handler.processInsert()
        handle_notify_list(handler.notify_list)
    finally:
        handler.cleanup()

@timed
def db_delete(data_descriptor, session=None):
    schema = data_descriptor.getSchema()
    if schema < SCHEMA.schema_default_end:
        handler = default_db_delete(data_descriptor, session)
    elif schema in user_handler_map:
        handler = user_handler_map[schema]("del", data_descriptor, session)
    else:
        print "data_function::db_delete not support schema ", schema
        return None
    try:
        handler.processDelete()
        handle_notify_list(handler.notify_list)
        db_flush_cache(data_descriptor)

    finally:
        handler.cleanup()
        
@timed
def db_flush_cache(data_descriptor):
    cached_key = make_cached_key(data_descriptor.getSchema(),
                                 data_descriptor.getDataType(),
                                 data_descriptor.getKeys())
    cache = None

    cache_time = get_cache_policy(data_descriptor.getSchema(),
                                   data_descriptor.getDataType())
    if cache_time is None or cache_time < 0:
        cache_time = 0

    cache = Cache_Service() if not cache_time == 0 else None
    
    try:
        if cache is not None and cache.exists(cached_key):
            cache.delete(cached_key)
    except Exception, e:
        import traceback
        logger.error("exception from redis:\n %s"%traceback.format_exc())
