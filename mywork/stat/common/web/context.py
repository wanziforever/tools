#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2011-12-17

@author: mengchen
'''
from common.error.errors import CodedError
from common.types import Dict
import doctest
import threading

_data = threading.local()
    
class Context(Dict):
    def __init__(self, **kw):
        self.request_headers = {}
        self.request_cookies = {}
        self.response_headers = {}
        self.response_cookies = {}
        super(Context, self).__init__(**kw)
        self._post_actions = []
        
    @staticmethod
    def curctx():
        try:
            return _data.context
        except AttributeError:
            raise CodedError('CONTEXT_NOT_SET', 'Context should be set first.')
        
    def __enter__(self):
        self.set_as_cur_ctx()
        return self
    
    def __exit__(self, *args):
        for action in self._post_actions:
            action()
        del _data.context
        
    def cookie(self, key, value=None):
        '''
        >>> ctx = Context(request_cookies={'c1':'v1'})
        
        get request header
        >>> ctx.cookie('c1')
        'v1'
        
        set response header
        >>> ctx.cookie('c2', 'v2')
        >>> ctx.response_cookies['c2']
        'v2'
        '''
        if value is None:
            return self.request_cookies.get(key)
        else:
            self.response_cookies[key] = value
        
    def header(self, key, value=None):
        '''
        >>> ctx = Context(request_headers={'h1':'v1'})
        
        get request header
        >>> ctx.header('h1')
        'v1'
        
        set response header
        >>> ctx.header('h2', 'v2')
        >>> ctx.response_headers['h2']
        'v2'
        '''
        if value is None:
            return self.request_headers.get(key)
        else:
            self.response_headers[key] = value
        
    def register_post_action(self, action):
        self._post_actions.append(action)
        
    def set_as_cur_ctx(self):
        _data.context = self
    
if __name__ == '__main__':
    doctest.testmod()
    