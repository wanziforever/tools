#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Nov 16, 2011

@author: mengchen
'''
import doctest
import os
import sys

def get_python_path():
    '''
    if PYTHONPATH variable is set, should return this variable
    >>> os.environ = { 'PYTHONPATH' : '/srv/transcode/latest' }
    >>> get_python_path()
    '/srv/transcode/latest'
    
    if PYTHONPATH variable is not set, should return the current working directory
    >>> os.environ = {}
    >>> get_python_path() is not None
    True
    '''
    return os.getenv('PYTHONPATH', os.path.dirname(sys.argv[0]))

if __name__ == '__main__':
    doctest.testmod()
    