#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Dec 2, 2011

@author: mengchen
'''
from common import json2
from common.error.errors import ResourceNotFoundError, UnknownError, \
    CodedError
from common.types import Function
from common.web import resps
from common.web.context import Context
from common.web.resps import Response
import doctest
import logging

_handlers = {}

def add_handler(path, handler):
    _handlers[path] = handler
    
def get_handler(path):
    try:
        return _handlers[path]
    except KeyError:
        logging.warn('Handler for path %s cannot be found.' % path)
        raise ResourceNotFoundError('URL', path)

class handler(Function):
    def __init__(self, func):
        super(handler, self).__init__(func)
        self._path = self._calc_path(self._func.__module__, self._func.__name__)
        self._add_handler()
        
    def handle(self, d):
        try:
            args = self._convert_to_arg_list(d)
            rslt = self._call_func(args)
            body = self._translate_result_body(rslt)
            ctx = Context.curctx()
            return Response(resps.STATUS_200, body, ctx.response_headers, ctx.response_cookies)
        except Response, r:
            return r
        except Exception, e:
            logging.warn('Failed to handle.', exc_info=True)
            code = self._translate_error_code(e)
            body = self._translate_error_body(e)
            return Response(code, body)
        
    def _add_handler(self):
        add_handler(self._path, self)
        
    def _calc_path(self, modname, handlername):
        '''
        >>> def foo():
        ...     pass
        >>> foo.__module__ = 'fakemod.handlers'
        >>> h = handler(foo)
        
        normal situation
        >>> h._calc_path('fakemod.handlers', 'foo')
        '/fakemod/foo'
        
        raises error if handler not placed within a handlers module
        >>> h._calc_path('fakemod', 'foo')
        Traceback (most recent call last):
        ...
        UnknownError: [UNKNOWN_ERROR] Handler foo should be placed in a handlers module, but is placed in module fakemod.
        '''
        if not modname.endswith('handlers'):
            raise UnknownError('Handler %s should be placed in a handlers module, but is placed in module %s.' % (handlername, modname))
        return '/' + modname[:-len('handlers')].replace('.', '/') + handlername
    
    def _call_func(self, args):
        return self._func(*args)
    
    def _translate_result_body(self, result):
        return result
    
    def _translate_error_code(self, e):
        if isinstance(e, CodedError):
            if isinstance(e, UnknownError):
                code = resps.STATUS_500
            elif isinstance(e, ResourceNotFoundError):
                code = resps.STATUS_404
            else:
                code = resps.STATUS_400
        else:
            code = resps.STATUS_500
        return code
    
    def _translate_error_body(self, e):
        return e.message
    
class json_handler(handler):
    def get_content_type(self):
        return 
        
    def handle(self, d):
        Context.curctx().header('Content-Type', 'application/json; charset=utf-8')
        for k in d:
            d[k] = json2.loads(d[k])
        return super(json_handler, self).handle(d)
    
    def _translate_result_body(self, result):
        return json2.dumps(result)
    
    def _translate_error_body(self, e):
        return error2json(e)
        
    def _convert_error_type_name(self, err_type):
        pass
    
def error2json(e):
    '''
    >>> error2json(UnknownError())
    '{"message": "Unknown error occured.", "error": "UNKNOWN_ERROR"}'
    
    >>> error2json(AttributeError('id'))
    '{"message": "id", "error": "AttributeError"}'
    '''
    if isinstance(e, CodedError):
        return json2.dumps(e)
    else:
        e = { 'error' : type(e).__name__,
              'message' : unicode(e) }
        return json2.dumps(e)
    
if __name__ == '__main__':
    doctest.testmod()
    