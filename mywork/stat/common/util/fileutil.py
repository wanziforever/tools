#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Oct 31, 2011

@author: mengchen
'''
import doctest
import os
import re
import shutil
import logging

log = logging.getLogger(__name__)

class _TempObject(object):
    def __init__(self, delete_on_success=True, delete_on_error=True):
        self._delete_on_success = delete_on_success
        self._delete_on_error = delete_on_error
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        if value is None:
            if self._delete_on_success:
                self._delete()
        else:
            if self._delete_on_error:
                self._delete()
        
class TempFile(_TempObject):
    def __init__(self, path, delete_on_success=True, delete_on_error=True):
        super(TempFile, self).__init__(delete_on_success, delete_on_error)
        self._path = path
        
    def _delete(self):
        safe_remove(self._path)
        
class TempDir(_TempObject):
    def __init__(self, dir, delete_on_success=True, delete_on_error=True):
        super(TempDir, self).__init__(delete_on_success, delete_on_error)
        self._dir = dir
        
    def _delete(self):
        if os.path.exists(self._dir):
            shutil.rmtree(self._dir)
        
def calc_dir_size(dir, included_pattern=None, excluded_pattern=None):
    files = list_files(dir, recursive=True)
    if included_pattern:
        p = re.compile(included_pattern)
        files = [f for f in files if p.match(f)]
    if excluded_pattern:
        p = re.compile(excluded_pattern)
        files = [f for f in files if not p.match(f)]
    log.info("files: " + str(files))
    sizes = [long(os.path.getsize(f)) for f in files]
    return sum(sizes)

def create_dir_if_not_exist(dir):
    try:
        os.makedirs(dir)
    except OSError, e:
        msg = unicode(e)
        if msg.startswith('[Errno 17] File exists: '): 
            pass # for linux: ignore if already exist
        elif msg.startswith('[Error 183] : '):
            pass # for windows: ignore if already exist
        else:
            raise
        
def create_parent_dir_if_not_exist(path):
    parent_dir = os.path.dirname(path)
    create_dir_if_not_exist(parent_dir)
        
def empty_dir(dir):
    for dir, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(dir, name))
        for name in dirs:
            os.rmdir(os.path.join(dir, name))
        
def list_files(dir, pattern='.*', recursive=False):
    p = re.compile(pattern)
    pathes = [(name, os.path.join(dir, name)) for name in os.listdir(dir)]
    files = [path for name, path in pathes if os.path.isfile(path) and p.match(name)]
    files.sort()
    if recursive:
        for name, path in pathes:
            if os.path.isdir(path):
                files.extend(list_files(path, pattern, True))
    return files

def make_empty_dir(dir):
    if os.path.exists(dir):
        empty_dir(dir)
    else:
        os.makedirs(dir)
        
def readfile(path):
    with open(path, 'r') as f:
        return f.read()
    
def readlines(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    return [l.rstrip('\r\n') for l in lines]

def safe_remove(path):
    try:
        os.remove(path)
    except OSError:
        pass

def touch(path):
    if os.path.exists(path):
        return
    f = open(path, 'w')
    f.close()
    
def writefile(path, s):
    with open(path, 'w') as f:
        f.write(s)
        
def writelines(path, lines):
    writefile(path, os.linesep.join(lines))
    
if __name__ == '__main__':
    doctest.testmod()
    