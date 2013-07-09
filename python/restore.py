#!/usr/bin/env python

import os
import sys
import subprocess
import shlex
import re
import shutil
from datetime import datetime

target_d = "/home/denny/.platform.bak"
project_d = "/root/platform"
m_all_packages = {}
signature = ".signature"

packageRe = re.compile(r"platform_\d{4,4}-\d{2,2}-\d{2,2}_\d{2,2}"
                       "_\d{2,2}_\d{2,2}.zip")

def log(string):
    # sys.stdout.write(string)
    print string

def examine():
    if not os.path.isdir(target_d):
        log("target directory is not a dir or not exist: %s"%target_d)
        exit()
    try:
        filehandle = open(target_d + "/.test.txt", 'w')
    except IOError:
        sys.exit("Unable to write to %s"%target_d)

def get_files_with_index(dir, m_files):
    if not os.path.isdir(dir):
        log("%s is not a directory"%dir)
        exit()
    index = 1
    for f in os.listdir(dir):
        m = packageRe.match(f)
        if not m:
            continue
        m_files[index] = f
        index += 1

def print_all_package_with_index(packages):
    for index in sorted(packages.keys()):
        if index < 10:
            log("[ %d] %s"%(index, packages[index]))
        elif index > 10:
            log("[%d] %s"%(index, package[index]))
    
def call_restore():
    log("restore platform package:")
    get_files_with_index(target_d, m_all_packages)
    print_all_package_with_index(m_all_packages)
    selected = raw_input("select the package to restore: ")
    if int(selected) not in m_all_packages:
        log("invalid input, exit")
        exit()
    log("")
    do_restore(int(selected))
    
def check_and_backup_old(dir):
    if not os.path.exists(dir):
        return
    dir_bak = dir + ".bak"
    log("existing project found, move it to %s"%dir_bak)
    if os.path.exists(dir_bak):
        shutil.rmtree(dir_bak)
    shutil.move(dir, dir_bak)
    
def clear_project(dir):
    if not os.path.exists(dir):
        return
    log("clear the existing project %s"%dir)
    os.rmdir(dir)
    
def do_restore(index):
    check_and_backup_old(project_d)
    clear_project(project_d)
    if not os.path.exists(project_d):
        os.mkdir(project_d)
    restoreFrom = "%s/%s"%(target_d, m_all_packages[index])
    log("restore %s to %s"%(restoreFrom, project_d))
    os.chdir(project_d)
    cmd = "unzip %s/%s"%(target_d, m_all_packages[index])
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    out, err = p.communicate()
    # touch a signature file after restoration
    time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    f = open("%s/%s"%(project_d, signature), "a")
    f.write("[%s]\n"
            "restore from %s\n\n"%(time, restoreFrom))
    f.close()
    
if __name__ == "__main__":
    examine()
    call_restore()

