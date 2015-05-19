#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import doctest
import os
import re
import shutil
import logging
import zipfile

log = logging.getLogger(__name__)

class _TempObject(object):
    def __init__(self, delete_on_success=True, delete_on_error=True):
        self._delete_on_success = delete_on_success
        self._delete_on_error = delete_on_error
        
    def _delete(self):
        pass
        
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
    def __init__(self, dir_path, delete_on_success=True, delete_on_error=True):
        super(TempDir, self).__init__(delete_on_success, delete_on_error)
        self._dir = dir_path
        
    def _delete(self):
        if os.path.exists(self._dir):
            shutil.rmtree(self._dir)
        
def calc_dir_size(dir_path, included_pattern=None, excluded_pattern=None):
    files = list_files(dir_path, recursive=True)
    if included_pattern:
        p = re.compile(included_pattern)
        files = [f for f in files if p.match(f)]
    if excluded_pattern:
        p = re.compile(excluded_pattern)
        files = [f for f in files if not p.match(f)]
    log.info("files: " + str(files))
    sizes = [long(os.path.getsize(f)) for f in files]
    return sum(sizes)

def create_dir_if_not_exist(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError, e:
        msg = unicode(e)
        if msg.find('File exists') > -1: 
            pass # for linux: ignore if already exist
        elif msg.startswith('[Error 183] : '):
            pass # for windows: ignore if already exist
        else:
            raise
        
def create_parent_dir_if_not_exist(path):
    parent_dir = os.path.dirname(path)
    create_dir_if_not_exist(parent_dir)
        
def empty_dir(dir_path):
    for dir_path, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(dir_path, name))
        for name in dirs:
            os.rmdir(os.path.join(dir_path, name))
        
def list_files(dir_path, pattern='.*', recursive=False):
    p = re.compile(pattern)
    pathes = [(name, os.path.join(dir_path, name)) for name in os.listdir(dir_path)]
    files = [path for name, path in pathes if os.path.isfile(path) and p.match(name)]
    files.sort()
    if recursive:
        for name, path in pathes:
            if os.path.isdir(path):
                files.extend(list_files(path, pattern, True))
    return files

def make_empty_dir(dir_path):
    if os.path.exists(dir_path):
        empty_dir(dir_path)
    else:
        os.makedirs(dir_path)
        
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
    
def backup_file(backup_path, backup_name, file_path):
    create_dir_if_not_exist(backup_path)
    zipFile = zipfile.ZipFile(os.path.join(backup_path, backup_name), 'w')
    zipFile.write(file_path, os.path.basename(file_path), zipfile.ZIP_DEFLATED)  
    zipFile.close()
    
def get_readable_size(size_in_byte):
    unit_size = 1
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_byte / (unit_size * 1024) < 1 or unit == 'TB':
            return '{0:.2f}{1}'.format((size_in_byte * 1.0) / unit_size, unit)
        unit_size *= 1024
    
if __name__ == '__main__':
    doctest.testmod()
    