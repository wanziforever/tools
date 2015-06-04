#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Mar 1, 2012

@author: cooledcoffee
'''
from common.error.errors import ModNotFoundError
from common.types import Dict
from common.util import modutil, timeutil
import datetime

if modutil.exists('sqlalchemy'):
    class ModelBase(object):
        def dict(self):
            return Dict([(k, v) for k, v in self.__dict__.items() if not k.startswith('_')])
        
        def __json__(self):
            json = self.dict()
            for k, v in json.items():
                if isinstance(v, datetime.datetime):
                    json[k] = timeutil.datetime2timestamp(v)
            return json
    from sqlalchemy.ext.declarative import declarative_base
    Model = declarative_base(cls=ModelBase)
else:
    class Model(object):
        def __init__(self):
            raise ModNotFoundError('sqlalchemy')
        