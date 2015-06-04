#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Nov 18, 2011

@author: mengchen
'''
from common.types import Dict
from common.util import fileutil
import subprocess
import logging
import os

log = logging.getLogger(__name__)

def list_processes(cmd, match_end=True):
    p = subprocess.Popen('ps ax -o pid,cmd|grep "%s"' % cmd,
            shell=True, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate() #@UnusedVariable
    log.info(u'ps ax out: %s, err: %s' % (stdout, stderr))
    processes = []
    for line in stdout.splitlines():
        pid, command = line.strip().split(' ', 1)
        if match_end:
            if command != cmd:
                continue
        else:
            if not command.startswith(cmd):
                continue 
        processes.append(Dict(pid=int(pid), cmd=command))
    p = subprocess.Popen('id', shell=True, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    log.info(u'id out: %s, err: %s' % (stdout, stderr))
    return processes

def parse_etc_hosts():
    lines = fileutil.readlines('/etc/hosts')
    hosts = {}
    for l in lines:
        l = l.strip()
        if len(l) == 0 or l[0] == '#':
            continue
        parts = l.split()
        ip = parts[0]
        for h in parts[1:]:
            hosts[h] = ip
    return hosts

def kill_processes(pids):
    if not pids:
        return
    p = subprocess.Popen('kill -9 %s' % ' '.join(map(str, pids)), shell=True, 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        log.info('failed to kill processes: %s. Error message: %s' % (' '.join(map(str, pids)), stderr))
    
    
    
    