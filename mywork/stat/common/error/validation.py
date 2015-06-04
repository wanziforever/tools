#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jan 16, 2012

@author: mengchen
'''
from common.error.errors import ArgError, ArgMissingError, BadArgTypeError, \
    BadArgValueError, ResourceNotFoundError
from common.types import Dict, Function
import doctest
import os
        
class Validator(Function):
    def __init__(self, expression):
        super(Validator, self).__init__()
        self._expression = expression
        
    def _call(self, *args, **kw):
        d = self._convert_to_arg_dict(*args, **kw)
        try:
            self._validate(d)
        except Exception, e:
            e.method = self.__module__ + ':' + self.__name__
            raise e
        return super(Validator, self)._call(*args, **kw)

    def _validate_value(self, value):
        pass
    
    def _validate(self, d):
        d = Dict(d)
        try:
            value = eval(self._expression, d)
        except KeyError:
            raise ArgMissingError(self._expression)
        except AttributeError:
            raise ArgMissingError(self._expression)
        except:
            raise ArgError('VALIDATION_FAILED', 'Failed to evaluate expression "%s".' % self._expression)
        self._validate_value(value)

class choices(Validator):
    def __init__(self, expression, options):
        super(choices, self).__init__(expression)
        self._options = options
        
    def _validate_value(self, value):
        validate_arg_within_choices(self._expression, value, self._options)
        
class exists(Validator):
    def _validate_value(self, value):
        # need to do nothing
        pass
        
class file_exists(Validator):
    def _validate_value(self, value):
        if not os.path.exists(value):
            raise ResourceNotFoundError('FILE', value)

class oftype(Validator):
    def __init__(self, expression, supported_types):
        super(oftype, self).__init__(expression)
        self._supported_types = supported_types
        
    def _validate_value(self, value):
        validate_arg_type(self._expression, value, self._supported_types)

class required(Validator):
    def _validate_value(self, value):
        validate_arg_not_empty(self._expression, value)
        
def validate_arg_not_null(name, value):
    '''
    >>> validate_arg_not_null('key', 123)
    >>> validate_arg_not_null('key', None)
    Traceback (most recent call last):
    ...
    ArgMissingError: [ARG_MISSING] "key" is required. (param="key")
    '''
    if value is None:
        raise ArgMissingError(name)
    
def validate_arg_not_empty(name, value):
    '''
    >>> validate_arg_not_empty('key', '123')
    
    >>> validate_arg_not_empty('key', None)
    Traceback (most recent call last):
    ...
    ArgMissingError: [ARG_MISSING] "key" is required. (param="key")
    
    >>> validate_arg_not_empty('key', '')
    Traceback (most recent call last):
    ...
    ArgMissingError: [ARG_MISSING] "key" is required. (param="key")
    '''
    if value is None or value == '':
        raise ArgMissingError(name)
    
def validate_arg_type(name, value, supported_types):
    '''
    validation succeed
    >>> validate_arg_type('key', '123', str)
    
    support single type
    >>> validate_arg_type('key', 123, str)
    Traceback (most recent call last):
    ...
    BadArgTypeError: [INVALID_ARG_TYPE] "key" requires type str, but a int is passed. (param="key")
    
    support multi types
    >>> validate_arg_type('key', 123, (str, unicode))
    Traceback (most recent call last):
    ...
    BadArgTypeError: [INVALID_ARG_TYPE] "key" requires type [str, unicode], but a int is passed. (param="key")
    '''
    if not isinstance(value, supported_types):
        raise BadArgTypeError(name, type(value), supported_types)

def validate_arg_within_choices(name, value, choices):
    '''
    should pass if value is in allowed values
    >>> validate_arg_within_choices('type', 'DAY', ['DAY', 'WEEK', 'MONTH'])
    
    should fail if value is not in allowed values
    >>> validate_arg_within_choices('type', 'YEAR', ['DAY', 'WEEK', 'MONTH'])
    Traceback (most recent call last):
    ...
    BadArgValueError: [INVALID_ARG_VALUE] Invalid arg value "YEAR" for parameter type. Allowed values are ['DAY', 'WEEK', 'MONTH']. (param="type")
    '''
    if value not in choices:
        msg = 'Invalid arg value "%s" for parameter %s. Allowed values are %s.' % (value, name, choices)
        raise BadArgValueError(name, value, msg)
    
def validate_resource_found(resource, resource_type, resource_key):
    if resource is None:
        raise ResourceNotFoundError(resource_type, resource_key)
    
if __name__ == '__main__':
    doctest.testmod()
    