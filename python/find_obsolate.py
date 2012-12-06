#!/usr/bin/env python
"""
tool for finding out the different record, which are existed in A file,
but not in B file. for the record format in the two files, there is no
restriction, but the format pattern should be provided, which is used
to capture valid part of data from given record, below are one example:
The tool will require following two input files:
1) the path of the file dfs_list.txt (file A)
   example format
   /media/2121110000
   /media/2121110001
   ...
   the PATTERN of file A can be "\/\w+\/(\w+)", which can capture digit
2) the path of the file oss_list.txt (file B)
   2121110000
   2121110001
   ...
   the pattern of file B can be "(.+)"
   
the above example is to find out the the contentid exist in DFS, but not
in OSS

How the tool work:
putting all the captured record in file B to the HASH array, and use
captured record in file A to lookup the HASH array, if it can be found,
it means the file exist both in file A and file B; if not, it means
the file only exist in file A. and will be reported to screen at last.

NOTE!! The tool cannot do opposite that finding out the record exist in
       B, but not in A.
"""

import sys
import re

# following to regular expression are used to capture valid data from
# file A and file B, the regular expression should contain only one
# group, and program will only capture the first captured group.
re_for_file_A = re.compile(r"\/\w+\/(\w+)");
#re_for_file_A = re.compile(r"(.+)");
re_for_file_B = re.compile(r"(.+)");

# flag to control the output that whether to only print the valid data
# which was captured by regular expression, if it set to no, will print
# initial data.
only_print_valid_data = False

to_dict = {}
to_list = []
diff_list = []

class entry:
    def __init__(self, initial_input, expression):
        self.initial_data = initial_input
        self.valid_data = captureData(self.initial_data, expression)
    def getInitialData(self):
        return self.initial_data
    def getValidData(self):
        return self.valid_data
    

def log(string):
    # sys.stdout.write(string)
    print string

def open_file(file_name):
    """ open file, return None if fail, capture the system exception,
    and handle open file fail by self """
    try:
        fp = open(file_name, "r")
        return fp
    except:
        return None
        
def usage():
    log("***********************************************************\n"
        "script used to find the record in file_A, but not in file_B\n"
        "Usage: %s <file_A> <file_B>\n"
        "************************************************************"
        %sys.argv[0])

def isIgnored(line):
    """ ignore the blank line """
    blankRe = re.compile(r'\s*[\r|\n]$')
    m = blankRe.match(line)
    if m:
        return True
    return False

def validateData(record, expression):
    """ the record should be in a given valid format, which can satisfy
    a given regular expression
    example:
        /media/201212030050010 can satisfy "\/\w+\/(\w+)"
    """
    m = expression.match(record)
    if m:
        return True
    log("validation fail for path %s"%record)
    return False
    
def captureData(line, expression):
    """ parse the input line in the file_X, and return the captured
    data which is considered a valid data for comparation
    the regular expression should contain only one group, and program
    will only capture the first captured group.
      example:
        record    /media/201212030050010
        re        "\/\w+\/(\w+)"
        captured  201212030050010
      Argument:
        line initial data of the record
        re_for_file_X regular expression for file X
      Return:   valid captured data 
    """
    m = expression.match(line)
    if not m:
        return None
    try:
        ret = m.group(1)
    except:
        log("fail to capture data for: %s, check your regular expression"%line)
        exit()
    return ret

def putRecordToHash(file_name, expression, to_dict):
    """ read the content id from OSS input file, and put it into
    the hash table """
    fp = open_file(file_name)
    if not fp:
        log("fail to open file %s"%file_name)
        exit()
    while True:
        line = fp.readline()
        if not line:
            break
        if isIgnored(line):
            continue
        line = line.strip()
        hash_entry = entry(line, expression)
        if not hash_entry.getValidData():
            continue
        to_dict[hash_entry.getValidData()] = hash_entry
    fp.close()

def putRecordToList(file_name, expression, to_list):
    """ parse the file path to get the content id, and put it to
    the list """
    fp = open_file(file_name)
    if not fp:
        log("fail to open file %s"%file_name)
        exit()
    while True:
        line = fp.readline()
        if not line:
            break
        if isIgnored(line):
            continue
        line = line.strip()
        list_entry = entry(line, expression)
        if not list_entry.getValidData():
            continue
        to_list.append(list_entry)
    fp.close()

def LookupListInDict(slist, sdict, dlist):
    """ loop the source list entry, and check whether the entry
    exist in the dictionary, if not exist, add it to the missing
    list 
    argument:
    slist source list from file A
    sdict  source dictionary from file B
    dlist different record list
    """
    if len(slist) == 0:
        log("there is no valid contentID in DFS")
        exit()
    for record in slist:
        if record.getValidData() in sdict:
            continue
        else:
            dlist.append(record)

def reportDiff(issue_record_list):
    log("got the following content was obsolate in DFS\n"
        "(content exist in HDF, but not in OSS):")
    for record in issue_record_list:
        if only_print_valid_data:
            log("%s"%record.getValidData())
        else:
            log("%s"%record.getInitialData())
    
def call_diff(file_A, expression_A, file_B, expression_B):
    global to_dict, to_list, diff_list
    putRecordToHash(file_B, expression_B, to_dict)
    putRecordToList(file_A, expression_A, to_list)
    LookupListInDict(to_list, to_dict, diff_list)
    reportDiff(diff_list)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit()
    fileA = sys.argv[1]
    fileB = sys.argv[2]
    call_diff(fileA, re_for_file_A, fileB, re_for_file_B)
