#!/usr/bin/env python

class InvalidKeyException(Exception):
    def __init__(self, handler_name, key_name):
        self.handler_name = handler_name
        self.key_name = key_name

    def __str__(self):
        return "%s has no set key for %s"%(self.handler_name, self.key_name)
    def __repr__(self):
        return self.str()
        
class DataDesc(object):
    def __init__(self, schema=None, data_type=None):
        self.results = []
        self.keys = {}
        self.schema = schema
        self.data_type = data_type
        self.modifier = {}
        #self.row_num = 0
        self.retcode = 0
        self.session = None
        self.page = [0,0]
        self.isBulkKey = False
        self.mkeys = []
        self.cache_only = False

    def reset(self):
        self.results = []
        self.keys = {}
        self.modifier = {}
        self.retcode = 0
        self.page = [0,0]
        self.isBulkKey = False
        self.cache_only = False

    def setBulkKeys(self, keys=[]):
        '''Maybe this should be deprecated for data_function.make_cached_key'''
        ''' will override the setKey '''
        self.keys = keys
        #TODO: Maybe this should be self.isBulkKey
        isBulkKey = True

    def setCached(self, cached, time=0):
        '''just a virtual cache function, all the cache implemetation was moved out'''
        return
        
    def getNumOfEntry(self):
        return len(self.results)
    def setNumOfEntry(self, num):
        self.row_num = num

    def getResult(self):
        return self.results

    def setPageStart(self, start):
        self.page[0] = start
    def setPageAmount(self, amount):
        self.page[1] = amount

    def setPageInfo(self, start, amount):
        self.page = [start, amount]

    def getPageInfo(self):
        return self.page

    def setKey(self, index, value):
        self.keys[index] = value

    def getKey(self, index):
        return self.keys[index]

    def getKeys(self):
        return self.keys
    
    def getmKey(self):
        return self.mkeys

    def setSchema(self, schema):
        self.schema = schema

    def getSchema(self):
        return self.schema

    def setDataType(self, data_type):
        self.data_type = data_type

    def getDataType(self):
        return self.data_type

    def setSession(self, session):
        self.session = session
        
    def setModifier(self, name, value):
        self.modifier[name] = value

    def getModifier(self, name):
        if name in self.modifier:
            return self.modifier[name]
        return None

    def getNumOfModifiers(self):
        return len(self.modifier.keys())

    def setCacheOnly(self, v=True):
        self.cache_only = v

    def isCacheOnly(self):
        return self.cache_only

    def setModifierDict(self, info_dict, only=None):
        for (k, v) in info_dict.items():
            if k!=only:
                self.setModifier(k, v)
