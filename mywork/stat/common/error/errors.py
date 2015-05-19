#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Oct 14, 2011

@author: mengchen
'''
import doctest

class CodedError(Exception):
    def __init__(self, code, msg=None, **kw):
        super(CodedError, self).__init__(msg)
        self.code = code
        self.__dict__.update(kw)
        
    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError, k:
            raise AttributeError(k)
    
    def __setattr__(self, key, value): 
        self.__dict__[key] = value
        
    def __json__(self):
        '''
        >>> CodedError('TEST_ERROR', 'Test error occured.').__json__()
        {'message': 'Test error occured.', 'error': 'TEST_ERROR'}
        >>> CodedError('TEST_ERROR', 'Test error occured.', param='myparam').__json__()
        {'message': 'Test error occured.', 'param': 'myparam', 'error': 'TEST_ERROR'}
        '''
        d = { 'error' : self.code, 'message' : self.message }
        d.update(self._get_extra_fields())
        return d
    
    def __str__(self):
        '''
        >>> str(CodedError('AUTH_ERROR', 'Auth failed.'))
        '[AUTH_ERROR] Auth failed.'
        
        >>> str(CodedError('AUTH_ERROR', 'Auth failed.', param='id'))
        '[AUTH_ERROR] Auth failed. (param="id")'
        
        >>> str(CodedError('AUTH_ERROR', 'Auth failed.', param='id', method='user.foo'))
        '[AUTH_ERROR] Auth failed. (method="user.foo", param="id")'
        '''
        s = '[%s] %s' % (self.code, self.message)
        fields = self._get_extra_fields()
        if len(fields) != 0:
            fields = ['%s="%s"' % (k, v) for k, v in fields.items()]
            fields = ', '.join(fields)
            s += ' (%s)' % fields
        return s
    
    def _get_extra_fields(self):
        '''
        >>> e = CodedError('AUTH_ERROR', 'Auth failed.', param='id', method='user.foo')
        >>> e._get_extra_fields()
        {'method': 'user.foo', 'param': 'id'}
        '''
        fields = dict(self.__dict__)
        del fields['code']
        return fields
    
class ArgError(CodedError):
    def __init__(self, code, message, param=None):
        super(ArgError, self).__init__(code, message, param=param)
        
class ArgMissingError(ArgError):
    def __init__(self, name):
        super(ArgMissingError, self).__init__('ARG_MISSING', '"%s" is required.' % name, name)

class AuthError(CodedError):
    def __init__(self, msg='Authentication failed.'):
        super(AuthError, self).__init__('AUTH_FAILED', msg)
        
class BadArgTypeError(ArgError):
    def __init__(self, name, actual_type, supported_types):
        if isinstance(supported_types, type):
            type_names  = supported_types.__name__
        elif isinstance(supported_types, tuple):
            type_names = '[' + ', '.join([t.__name__ for t in supported_types]) + ']'
        else:
            type_names = str(supported_types)
        msg = '"%s" requires type %s, but a %s is passed.' % (name, type_names, actual_type.__name__)
        super(BadArgTypeError, self).__init__('INVALID_ARG_TYPE', msg, name)
        
class BadArgValueError(ArgError):
    def __init__(self, name, value=None, msg=None):
        '''
        msg is specified, should use the specified msg
        >>> BadArgValueError('id', 123, 'user defined message.').message
        'user defined message.'
        
        msg is not specified, but value is specified
        >>> BadArgValueError('id', 123).message
        'Invalid value "123" for parameter id.'
        
        neither msg nor value is specified
        >>> BadArgValueError('id').message
        'Invalid value for parameter id.'
        '''
        if msg is None:
            if value is None:
                msg = 'Invalid value for parameter %s.' % name
            else:
                msg = 'Invalid value "%s" for parameter %s.' % (str(value), name)
        super(BadArgValueError, self).__init__('INVALID_ARG_VALUE', msg, name)
        
class BadFileError(BadArgValueError):
    def __init__(self, name, type):
        '''
        >>> BadFileError('file', 'video').message
        'File for parameter file is not a valid video file.'
        '''
        msg = 'File for parameter %s is not a valid %s file.' % (name, type)
        super(BadFileError, self).__init__(name, None, msg)
        
class CastTypeError(CodedError):
    def __init__(self, value, to_type):
        super(CastTypeError, self).__init__('CAST_TYPE_ERROR', 'Failed to cast value "%s" from type %s to type %s.' \
                % (value, type(value).__name__, to_type.__name__))
        
class DecodeError(CodedError):
    def __init__(self, name, value):
        super(DecodeError, self).__init__('DECODE_ERROR', 'Failed to decode arg with name=%s and value=%s.' % (name, value))
        
class DuplicatedError(CodedError):
    def __init__(self, resource_type, key):
        '''
        if resource_type is string
        >>> e = DuplicatedError('USER', '123')
        >>> e.code
        'DUPLICATED_USER'
        >>> e.message
        'USER with key=123 already exists.'
        
        if resource_type is type
        >>> from datetime import datetime
        >>> e = DuplicatedError(datetime, '123')
        >>> e.code
        'DUPLICATED_DATETIME'
        >>> e.message
        'DATETIME with key=123 already exists.'
        '''
        if isinstance(resource_type, type):
            typename = resource_type.__name__.upper()
        else:
            typename = resource_type.upper()
        super(DuplicatedError, self).__init__('DUPLICATED_%s' % typename, '%s with key=%s already exists.' % (typename, key))
        
class LoginError(CodedError):
    def __init__(self, msg='Invalid user name or password.'):
        super(LoginError, self).__init__('LOGIN_FAILED', msg)
        
class PermissionDeniedError(CodedError):
    def __init__(self, type, key=None):
        if key is None:
            msg = 'Permission is denied on %s' % type
        else:
            msg = 'Permission is denied on %s %s' % (type, key)
        super(PermissionDeniedError, self).__init__('PERMISSION_DENIED', msg)
        
class S3OperateError(CodedError):
    def __init__(self, problem,reason):        
      super(S3OperateError, self).__init__('%s' % problem,'%s'%reason)



        
class ResourceNotFoundError(CodedError):
    def __init__(self, resource_type, key):
        '''
        if resource_type is string
        >>> e = ResourceNotFoundError('api', 'threads.create')
        >>> e.code
        'API_NOT_FOUND'
        >>> e.message
        'API threads.create cannot be found.'
        
        if resource_type is type
        >>> from datetime import datetime
        >>> e = ResourceNotFoundError(datetime, 'threads.create')
        >>> e.code
        'DATETIME_NOT_FOUND'
        >>> e.message
        'DATETIME threads.create cannot be found.'
        '''
        if isinstance(resource_type, type):
            typename = resource_type.__name__.upper()
        else:
            typename = resource_type.upper()
        super(ResourceNotFoundError, self).__init__('%s_NOT_FOUND' % typename, '%s %s cannot be found.' % (typename, key))
        
class ModNotFoundError(ResourceNotFoundError):
    def __init__(self, modname):
        super(ModNotFoundError, self).__init__('MODULE', modname)

class PageNotFoundError(ResourceNotFoundError):
    def __init__(self, page):
        super(PageNotFoundError, self).__init__('PAGE', page)
        
class UnknownError(CodedError):
    def __init__(self, msg='Unknown error occured.'):
        super(UnknownError, self).__init__('UNKNOWN_ERROR', msg)
        
if __name__ == '__main__':
    doctest.testmod()
    