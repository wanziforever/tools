#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Dec 16, 2011

@author: mengchen
'''
from common.util import modutil
import doctest
import sys

class ActionExecutor(object):
    def __init__(self, actions):
        self._actions = actions
        
    def execute(self, args):
        '''
        >>> r = ActionExecutor({'echo':lambda x: x})
        >>> r.execute(['echo', 'abc'])
        'abc'
        '''
        f = self._get_func(args[0])
        return self._run_action(f, args[1:])
    
    def _get_func(self, action_name):
        '''
        >>> r = ActionExecutor({'echo':lambda: 'echo'})
        >>> f = r._get_func('echo')
        >>> f()
        'echo'
        
        >>> r._get_func('not_exist')
        Traceback (most recent call last):
        ...
        Exception: Action not_exist not found.
        '''
        try:
            return self._actions[action_name]
        except KeyError:
            raise Exception('Action %s not found.' % action_name)
        
    def _run_action(self, action, args):
        '''
        >>> r = ActionExecutor(None)
        >>> f = lambda x: x
        >>> r._run_action(f, ['abc'])
        'abc'
        '''
        return action(*args)
    
def run_job(modname, args=None):
    m = modutil.import_module(modname)
    if args is None:
        args = sys.argv[1:]
    actions = {}
    for k in dir(m):
        actions[k] = getattr(m, k)
    return ActionExecutor(actions).execute(args)
    
if __name__ == '__main__':
    doctest.testmod()
    