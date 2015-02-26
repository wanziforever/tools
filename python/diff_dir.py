#!/usr/bin/env python

import os
import re
import sys
import difflib

d = difflib.Differ()

pwd = os.getcwd()
filesA = {}
dirsA = {}

filesB = {}
dirsB = {}

files_missing_A = [] # files in A, but not in B
files_missing_B = [] # files in B, but not in A

dirs_missing_A = []
dirs_missing_B = []

fail_to_diff = []

git_re = re.compile(r"\.git")

def collect_files(path, filesA, dirsA):
    for root, dirs, files in os.walk(path):
        subpath = root[len(path)+1:]
        m = git_re.search(root)
        if m:
            continue
        for f in files:
            if f.endswith(".pyc"):
                continue
            p = os.path.join(subpath, f)
            filesA[p] = False
        dirsA[subpath] = False

def diff_dict(dictA, dictB):
    consist = []
    not_consistA = []
    not_consistB = []
    for f in dictA.keys():
        dictA[f] = True
        if dictB.has_key(f) is True:
            dictB[f] = True
            consist.append(f)
        else:
            not_consistA.append(f)
    for f, stat in dictB.items():
        if stat is False:
            not_consistB.append(f)

    return consist, not_consistA, not_consistB

def call_diff(pathA, pathB):
    global files_to_diff, files_missing_A, files_missing_B
    global dirs_missing_A, dirs_missing_B
    collect_files(pathA, filesA, dirsA)
    collect_files(pathB, filesB, dirsB)
    files_to_diff = []

    files_to_diff, files_missing_A, files_missing_B = diff_dict(filesA, filesB)
    _, dirs_missing_A, dirs_missing_B = diff_dict(dirsA, dirsB)

    for f in files_to_diff:
        print "compare ", f, 
        a = os.path.join(pathA, f)
        b = os.path.join(pathB, f)
        ret = os.system("diff %s %s>/dev/null"%(a, b))
        if ret != 0:
            fail_to_diff.append(f)
            print " FAIl"
        else:
            print "SUCC"
            
def report():
    print "----- the following file exist in former directory, but not in later -----"
    print files_missing_A
    print
    print "----- the following dir exist in former directory, but not in later -----"
    print dirs_missing_A
    print
    
    print "----- the following file exist in later directory, but not in former -----"
    print files_missing_B
    print
    print "----- the following file exist in later directory, but not in former -----"
    print dirs_missing_B
    print
    
    print "----- the following files has different content ------"
    print fail_to_diff

def usage():
    print "%s <pathA> <pathB>"%sys.argv[0]
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(1)
    pathA = sys.argv[1]
    pathB = sys.argv[2]
    
    call_diff(pathA, pathB)
    report()
    
