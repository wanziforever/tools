#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Sep 15, 2011

@author: mengchen
'''
from common.log import log_enter, log_return
import doctest
import subprocess

class Wrapper(object):
    def __init__(self, cmd, error_class=Exception):
        self.cmd = cmd
        self.input = None
        self.error_class = error_class
        
    @log_enter('Executing {self.cmd} ...')
    @log_return('[DEBUG] Execution succeeded.', 'ret == 0')
    @log_return('[WARN] Execution failed. Return code is {self.retcode}. Stderr is:\n{self.stderr}', 'ret != 0 and self.error_class is not None')
    def run(self):
        '''
        execute successfully
        >>> w = Wrapper('python --version')
        >>> w.run()
        0
        
        execute failed but raise_error is false
        >>> w = Wrapper('abc', None)
        >>> w.run()
        127
        
        execute failed and raise_error is true
        >>> w = Wrapper('abc', Exception)
        >>> w.run()
        Traceback (most recent call last):
        ...
        Exception: Failed to execute "abc", return code is 127.
        >>> w.retcode
        127
        '''
        p = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout, self.stderr = p.communicate(self.input)
        self.retcode = p.returncode
        if self.retcode != 0:
            self.stdout = unicode(self.stdout, errors='ignore')
            self.stderr = unicode(self.stderr, errors='ignore')
            if self.error_class is not None:
                raise self.error_class('Failed to execute "%s", return code is %d.' % (self.cmd, self.retcode))
        return self.retcode
    
if __name__ == '__main__':
    doctest.testmod()
    