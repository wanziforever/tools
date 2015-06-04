#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from core.settings import settings

class _Session(Session):

    def __init__(self, *args, **kwargs):
        super(_Session, self).__init__(*args, **kwargs)

    def flush(self, objects=None):
        for entity in self.dirty:
            now = long(time.time())
            if hasattr(entity, 'modified_time'):
                entity.modified_time = now
            if hasattr(entity, 'version'):
                if entity.version is None:
                    entity.version = 1
                else:
                    entity.version += 1
        for entity in self.new:
            now = long(time.time())
            if hasattr(entity, 'created_time'):
                entity.created_time = now
            if hasattr(entity, 'modified_time'):
                entity.modified_time = now
            if hasattr(entity, 'version'):
                entity.version = 1
        super(_Session, self).flush(objects)

if settings.DB_UNITTEST_URL and len(settings.DB_UNITTEST_URL) > 0:
    conn_str = settings.DB_UNITTEST_URL
else:
    conn_str = 'mysql://{username}:{password}@{host}/{dbname}?charset=utf8'.format(
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        dbname=settings.DB_NAME)

engine = create_engine(conn_str, pool_recycle=3600, echo_pool=False,
                       echo=settings.DB_ECHO)
Session = scoped_session(sessionmaker(engine, autoflush=False))


def create_session():
    # return _Session(bind=engine, autoflush=False)
    return Session()
