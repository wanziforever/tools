#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Dec 28, 2011

@author: mengchen
'''
from common.error.errors import BadArgValueError, ModNotFoundError
from common.util import modutil
if modutil.exists('sqlalchemy'):
    from sqlalchemy.engine import create_engine
    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm.session import sessionmaker
    
    class SqlAlchemyDao(object):
        def __init__(self, host, user, passwd, db):
            conn_str = 'mysql://%s:%s@%s/%s?charset=utf8' % (user, passwd, host, db)
            self._engine = create_engine(conn_str, pool_recycle=3600, echo=False)
            class _Session(sessionmaker(bind=self._engine)):
                def __enter__(self):
                    return self
                
                def __exit__(self, type, value, traceback):
                    if value is None:
                        self.commit()
                    else:
                        self.rollback()
            self._Session = _Session
            self._ScopedSession = scoped_session(_Session)
            
        def create_scoped_session(self):
            return self._ScopedSession()
            
        def create_session(self):
            return self._Session()
            
        def execute(self, sql):
            conn = self._engine.connect()
            try:
                return conn.execute(sql)
            finally:
                conn.close()
            
        def query_for_value(self, sql):
            results = list(self.execute(sql))
            if len(results) != 1:
                raise BadArgValueError('sql', sql, 'Sql is expected to return 1 row, but %d rows are returned.' % len(results))
            return results[0][0]
else:
    class SqlAlchemyDao(object):
        def __init__(self, *args, **kw):
            raise ModNotFoundError('sqlalchemy')
        
        def create_session(self):
            raise ModNotFoundError('sqlalchemy')
        
        def create_scoped_session(self):
            raise ModNotFoundError('sqlalchemy')
