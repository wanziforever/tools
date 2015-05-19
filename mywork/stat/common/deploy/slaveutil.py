#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Nov 3, 2011

@author: mengchen
'''
from common.types import Dict
from common.util import httputil
import doctest

def execute(host, cmd):
    url = 'http://%s:8082/exec' % host
    resp = httputil.curl(url, {'cmd' : cmd})
    return _parse_response(resp.splitlines())

def _parse_response(lines):
    '''
    >>> r = _parse_response(['exitcode:', '0', 'stdout:', 'output1\\noutput2', 'stderr:', 'error1\\nerror2'])
    >>> r.exitcode
    0
    >>> r.stdout
    'output1\\noutput2'
    >>> r.stderr
    'error1\\nerror2'
    
    >>> r = _parse_response(['exitcode:', '0', 'stdout:', 'stderr:'])
    >>> r.stdout
    ''
    >>> r.stderr
    ''
    '''
    r = Dict()
    stdout_index = lines.index('stdout:')
    stderr_index = lines.index('stderr:')
    r.exitcode = int(lines[1])
    r.stdout = '\n'.join(lines[stdout_index + 1 : stderr_index])
    r.stderr = '\n'.join(lines[stderr_index + 1 :])
    return r

def upload(host, src, dest):
    url = 'http://%s:8082/upload' % host
    httputil.upload(url, src, { 'dest' : dest })

if __name__ == '__main__':
    doctest.testmod()
    