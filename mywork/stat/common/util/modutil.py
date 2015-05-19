#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Oct 27, 2011

@author: mengchen
'''
from common.error.errors import UnknownError, ModNotFoundError
import doctest
import sys

def exists(modname):
    '''
    >>> exists('common.util')
    True
    >>> exists('fakepackage.fakemod')
    False
    '''
    try:
        import_module(modname)
        return True
    except:
        return False

def import_module(modname):
    '''
    >>> m = import_module('common.error.errors')
    >>> m.__name__
    'common.error.errors'
    
    >>> import_module('not.exist.module')
    Traceback (most recent call last):
    ...
    ModNotFoundError: [MODULE_NOT_FOUND] MODULE not.exist.module cannot be found.
    '''
    if sys.version_info >= (2, 7):
        import importlib
        try:
            return importlib.import_module(modname)
        except Exception, e:
            if unicode(e) == u'No module named %s' % modname:
                raise ModNotFoundError(modname)
            else:
                raise UnknownError('Failed to import module %s.' % modname)
    else:
        try:
            levels = modname.split('.')
            m = _import(levels[0])
            for i in range(1, len(levels) + 1):
                current = '.'.join(levels[:i])
                parent = '.'.join(levels[:i-1])
                m = _import(current, parent)
            return m
        except ModNotFoundError:
            raise ModNotFoundError(modname)
        except UnknownError:
            raise UnknownError('Failed to import module %s.' % modname)

def _import(modname, parent=None):
    try:
        if parent is None:
            return __import__(modname)
        else:
            return __import__(modname, fromlist=[parent])
    except Exception, e:
        if unicode(e) == u'No module named %s' % modname:
            raise ModNotFoundError(modname)
        else:
            raise UnknownError('Failed to import module %s.' % modname)
    
if __name__ == '__main__':
    doctest.testmod()
    