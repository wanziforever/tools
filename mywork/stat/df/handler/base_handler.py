#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from df.session import create_session
import time
import logging
import inspect
from sqlalchemy.exc import DatabaseError, OperationalError, StatementError

logger = logging.getLogger('base_handler')

class request_handler(object):
    def __init__(self, op, data_desc):
        self.op = op
        self.data_desc = data_desc
        self.notify_list = []
        #self.redis = get_redis_session()

    def add_notify_descriptor(self, data_desc, mode="flush_cache"):
        import copy
        self.notify_list.append((copy.deepcopy(data_desc), mode))

    def processQuery(self):
        #print "base request handler process query function"
        pass
    def mProcessQuery(self):
        #print "base request handler multiple process query function"
        pass

    def processUpdate(self):
        #print "base request handler process update function"
        pass

    def processInsert(self):
        #print "base request handler process insert function"
        pass

    def processCount(self):
        #print "base requst handler process count function"
        pass

    def processDelete(self):
        #print "base request handler process delete function"
        pass

    def cleanup(self):
        #print "base request hanlder cleanup function"
        pass

def database_status_monitor(fun, cleanup_func=None):
    ''' only used for wrap db_handler class functions'''
    def decorator(*args, **kwargs):
        if db_handler.connection_down_timestamp > 0:
            delta = time.time() - db_handler.connection_down_timestamp
            if delta < db_handler.reconnect_timer:
                raise Exception("DATABASE DOWN OPERATION FORBIDEN FOR %s, "
                                "%s SECONDS LEFT"\
                                %(fun.__name__,
                                  int(db_handler.reconnect_timer - delta)))
        try:
            ret = fun(*args, **kwargs)
            # a problem is if  the fun has no db related operation, the success
            # of fun cannot stand for DB connection restored
            if db_handler.connection_down_timestamp != 0:
                logger.warn("MYSQL CONNECTION RECORVERED proved by %s"%fun.__name__)
                db_handler.connection_down_timestamp = 0
            return ret
        except OperationalError, e:
            if cleanup_func is not None:
                cleanup_func()
            logger.error("DATABASE CONNECTION DOWN FOR OPERATIONALERROR")
            db_handler.connection_down_timestamp = time.time()
            raise e

    return decorator


class db_handler(request_handler):
    reconnect_timer = 5 # second
    connection_down_timestamp = 0
    def __init__(self,op, data_desc, session=None):
        super(db_handler, self).__init__(op, data_desc)
        self.session = session if session is not None else create_session()
        self.db_prepare()

    def db_prepare(self):
        ''' add DB status check for all the db related operation '''

        if hasattr(self, "cleanup"):
            if not callable(getattr(self, "cleanup")):
                logger.debug("db_handler has no cleanup function, cannot wrap")
                return
        cleanup_fun = getattr(self, "cleanup")
        for func in ["processQuery", "processUpdate", "processInsert",
                     "processCount", "processDelete", "mProcessQuery"]:
            if not hasattr(self, func):
                continue
            if not callable(getattr(self, func)):
                continue
            #eval("self.{0} = database_status_monitor(self.{0})".format(func))
            setattr(self, func, database_status_monitor(getattr(self, func),
                                                        cleanup_fun))
        
    def processQuery(self):
        #print "base db request handlder process query function"
        pass

    def mProcessQuery(self):
        #print "base db request handlder multiple process query function"
        pass
    
    def processUpdate(self):
        #print "base db request handler process update function"
        pass

    def processInsert(self):
        #print "base db request handler process insert function"
        pass

    def processCount(self):
        #print "base db request handler process count function"
        pass

    def processDelete(self):
        #print "base db request handler process delete function"
        pass

    def cleanup(self):
        #try:
        #    self.session.commit()
        #    #self.session.expunge_all()
        #finally:
        #    self.session.close()
        self.session.close()
