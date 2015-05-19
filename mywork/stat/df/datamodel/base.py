#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, SmallInteger, BigInteger, func
from common.types import Dict
import time

def get_cur_time():
    return long(time.time())

class Base(object):
    @declared_attr
    def __tablename__( self ):
        return self.__name__
    __table_args__ = {'mysql_engine': 'InnoDB',
                     'mysql_charset': 'utf8'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(BigInteger, primary_key=True)
    customer_id = Column(BigInteger, nullable=True, index=True)
    #version = Column(BigInteger, nullable=False, default=1)
    created_time = Column(Integer, nullable=False, default=get_cur_time)
    modified_time = Column(Integer, nullable=False, default=get_cur_time, onupdate=get_cur_time, index=True)
    deleted = Column(SmallInteger, nullable=False, default=False, index=True)

    def dict(self):
        return Dict([(k, v) for (k, v) in self.__dict__.items()
                     if not k.startswith('_')])

    def set_attr(self, info_dict, ignore_attr_list=None):
        for (k, v) in info_dict.items():
            if not ignore_attr_list or (ignore_attr_list and
                                        k not in ignore_attr_list):
                setattr(self, k, v)

    def __json__(self):
        return self.dict()

    def __repr(self):
        return str(self.__json__())

Base = declarative_base(cls=Base)

if __name__ == "__main__":
    b = Base()
