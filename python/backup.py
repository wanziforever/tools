#!/usr/bin/env python

import os
import sys
import subprocess
import shlex
import glob
from datetime import datetime

target_d = "/home/denny/.platform.bak"
backup_t = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
target_f = "platform_%s.zip"%(backup_t)
project_d = "/root/platform"
signature = ".signature"

def log(string):
    print string

def examine():
    if not os.path.isdir(target_d):
        log("target directory is not a dir or not exist: %s"%target_d)
        exit()
    try:
        filehandle = open(target_d + "/.test.txt", 'w')
    except IOError:
        sys.exit("Unable to write to %s"%target_d)

def call_backup():
    log("[ %s ] BACKUP %s --> %s/%s"%(backup_t, project_d, target_d, target_f))
    if not os.path.exists(project_d):
        log("project directory %s not found"%project_d)
        exit()
    os.chdir(project_d)
    tmp = glob.glob("*")
    files = ""
    for f in tmp:
        files += "./%s "%f
    if os.path.exists("%s/%s"%(project_d, signature)):
        files += "./%s"%signature

    # add signature
    time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    f = open("%s/%s"%(project_d, signature), "a")
    f.write("[%s]\n"
            "backup to %s/%s\n\n"%(time, target_d, target_f))
    f.close()
    
    cmd = "zip %s/%s -r %s"%(target_d, target_f, files)
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = p.communicate()

if __name__ == "__main__":
    examine()
    call_backup()

