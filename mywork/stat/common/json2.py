#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2011-10-15

@author: mengchen
'''
from common.types import Dict
from json.decoder import WHITESPACE
import datetime
import doctest
import json
import re

class JsonAdapter(object):
    def default(self, obj):
        return obj
    
    def decode(self, s):
        return s
    
class DatetimeJsonApater(JsonAdapter):
    def default(self, obj):
        return obj.strftime('#%Y-%m-%d %H:%M:%S#')
    
    def decode(self, s):
        m = re.match('#(\\d{4})-(\\d{2})-(\\d{2}) (\\d{2}):(\\d{2}):(\\d{2})#', s)
        if m is None:
            return None
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        hour = int(m.group(4))
        minute = int(m.group(5))
        second = int(m.group(6))
        return datetime.datetime(year, month, day, hour, minute, second)

_ADAPTERS = {}
def extend(type, adapter):
    _ADAPTERS[type] = adapter
    
class CompositeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return getattr(obj, '__json__')()
        adapter = _ADAPTERS.get(type(obj))
        if adapter is not None:
            return adapter.default(obj)
        return obj
    
class CompositeDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        obj = super(CompositeDecoder, self).decode(s, _w)
        if isinstance(s, str) and isinstance(obj, unicode):
            obj = str(obj)
        if not isinstance(obj, (str, unicode)):
            return obj
        for adapter in _ADAPTERS.values():
            o = adapter.decode(obj)
            if o is not None:
                return o
        else:
            return obj
    
def dumps(obj):
    '''
    dump normal object:
    >>> dumps(1)
    '1'
    
    dump None
    >>> dumps(None)
    'null'
    
    dump datetime:
    >>> extend(datetime.datetime, DatetimeJsonApater())
    >>> dumps(datetime.datetime(2011, 1, 1, 12, 30, 40))
    '"#2011-01-01 12:30:40#"'
    >>> dumps({ 'time' : datetime.datetime(2011, 1, 1, 12, 30, 40) })
    '{"time": "#2011-01-01 12:30:40#"}'
    '''
    return json.dumps(obj, cls=CompositeEncoder)
    
def loads(s):
    '''
    load normal jsons:
    >>> loads('1')
    1
    >>> loads('"abc"')
    'abc'
    >>> loads(u'"abc"')
    u'abc'
    
    load object
    >>> o = loads('{"a":1, "b":"c"}')
    >>> o.a
    1
    >>> o.b
    'c'
    
    load datetime:
    >>> extend(datetime.datetime, DatetimeJsonApater())
    >>> loads('"#2011-01-01 12:30:40#"')
    datetime.datetime(2011, 1, 1, 12, 30, 40)
    '''
    is_str = isinstance(s, str)
    def _hook(d):
        o = Dict()
        for k, v in d.items():
            if is_str and isinstance(v, unicode):
                v = str(v)
            o[str(k)] = v
        return o
    return json.loads(s, encoding='ascii', cls=CompositeDecoder, object_hook=_hook)

if __name__ == '__main__':
    doctest.testmod()
    