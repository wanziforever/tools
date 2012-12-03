#!/usr/bin/env python
"""
tool for finding out the obsolate files , which are existed in DFS,
but not in OSS.
The tool will require following two input files:
1) file path for each file in the DFS system
   example format
   /media/2121110000
   /media/2121110001
   ...
2) content id list in OSS system
   2121110000
   2121110001
   ...

the procedure to implement the work is putting all the OSS contend id
to the HASH array, and parse the file path in DFS file to get content
id, and lookup it in OSS contend id HASH, if it can be found, it means
the file exist both in DFS and OSS; if not, it means the file only exist
in DFS. the obsolate file in DFS will be report to screen at last.

NOTE!! The tool cannot do opposite that finding out the file exist in
       OSS, but not in DFS.

"""

from __future__ import with_statement
import sys
import re

oss_dict = {}
dfs_list = []
missing_list = []
        
def log(string):
    # sys.stdout.write(string)
    print string

def open_file(file_name):
    """ open file, return None if fail, capture the system exception,
    and handle open file fail by self """
    try:
        with open(file_name, "r") as fp:
            return fp
    except:
        return None
        
def usage():
    log("%s <dfs_file_list> <oss_file_list>"%sys.argv[0])

def isIgnored(line):
    """ ignore the blank and comments line """
    blankRe = re.compile(r'/n[/s| ]*/r')
    m = blankRe.match(line)
    if m:
        return True

def validatePath(line):
    """ the file path should have the following format in DFS
    input file:
        /xx/xxxxx  (example /media/201212030050010)
    """
    pathRe = re.compile(r"^\/\w+\/\w+")
    m = pathRe.match(line)
    if m:
        return True
    log("validation fail for path %s"%line)
    return False
    
def parseDFSPath(line):
    """ parse the input line in the dfs_file_list, and return
        the media type and content id
        example: /media/201212030050010,
                 return (media, 201212030050010)
        Argument: line input path string
        Return:   type and contentID pair
    """
    if not validatePath(line):
        return (None, None)
    _, media_type , contentID = line.split('/', 2)
    return (media_type, contentID)

def getOSSContentId(line):
    """ get contentid from line of string in OSS file, the
    implementation depend on the input file format of OSS
    content list file.
    """
    # currently simply return the whole line, suppose the OSS
    # input file only have one contendID one line
    return line
    
def putContentIdToHash(oss_file_name, oss_dict):
    """ read the content id from OSS input file, and put it into
    the hash table """
    fp = open_file(oss_file_name)
    if not fp:
        log("fail to open file %s"%oss_file_name)
        exit()
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if isIgnored(line):
            continue
        cid = getOSSContentId(line)
        if not cid:
            continue
        oss_dict[cid] = cid
    fp.close()

def putContentIdToList(dfs_file_name, dfs_list):
    """ parse the file path to get the content id, and put it to
    the list """
    fp = open_file(dfs_file_name)
    if not fp:
        log("fail to open file %s"%dfs_file_name)
        exit()
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if isIgnored(line):
            continue
        media_type, content_id = parseDFSPath(line)
        if not content_id:
            continue
        dfs_list.append(content_id)
    fp.close()

def LookupListInDict(slist, sdict, mlist):
    """ loop the source list entry, and check whether the entry
    exist in the dictionary, if not exist, add it to the missing
    list 
    argument:
    slist source contentID list in dfs
    sdict  source contentID dict in OSS
    mlist missing contentID list
    """
    if len(slist) == 0:
        log("there is no valid contentID in DFS")
        exit()
    for cid in slist:
        if cid in sdict:
            continue
        else:
            mlist.append(cid)


def reportDiff():
    global missing_list
    log("got the following content was obsolate in DFS\n"
        "(content exist in HDF, but not in OSS):")
    for cid in missing_list:
        log("%s"%cid)
    
def call_diff(dfs_file_name, oss_file_name):
    global oss_dict, dfs_list, missing_list
    putContentIdToHash(oss_file_name, oss_dict)
    putContentIdToList(dfs_file_name, dfs_list)
    LookupListInDict(dfs_list, oss_dict, missing_list)
    reportDiff()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit()
    call_diff(sys.argv[1], sys.argv[2])
    
