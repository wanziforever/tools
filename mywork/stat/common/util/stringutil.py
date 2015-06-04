#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2011-11-6

@author: mengchen
'''
from common.error.errors import BadArgTypeError
import doctest

def decapitalize(s):
    '''
    >>> decapitalize('Abc')
    'abc'
    >>> decapitalize('abc')
    'abc'
    '''
    return s[0].lower() + s[1:]

def u2s(s):
    u'''
    >>> u2s('abc')
    'abc'
    >>> u2s(u'abc')
    'abc'
    >>> u2s(None) is None
    True
    >>> u2s(1)
    Traceback (most recent call last):
    ...
    BadArgTypeError: [INVALID_ARG_TYPE] "s" requires type [<type 'str'>, <type 'unicode'>], but a int is passed. (param="s")
    '''
    if s is None:
        return None
    elif isinstance(s, str):
        return s
    elif isinstance(s, unicode):
        return str(s)
    else:
        raise BadArgTypeError('s', type(s), [str, unicode])

if __name__ == '__main__':
    doctest.testmod()
    