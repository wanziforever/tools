#!/usr/bin/env python
"""
tool used to find the duplicated record in a given file, and also
support the regular expression to capture valid data from given
record, the regular expression can be configured
"""

import sys
import re

# following to regular expression are used to capture valid data from
# file the regular expression should contain only one group, and program
# will only capture the first captured group.
re_for_file = re.compile(r"(.+)");

to_dict = {}
dup_list = []

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
        "script used to find the duplicated record in file"
        "Usage: %s <file>"
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

def reportDiff(dup_record_list):
    global to_dict
    log("got the following content was duplicated(times):")
    if len(dup_record_list) == 0:
        log("there is no duplicated record")
        return
    for record in dup_record_list:
        log("%s(%d)"%(record, to_dict[record]))
    
def call_dup(file_name, expression):
    global to_dict, dup_list
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
        record = captureData(line, expression)
        if not record:
            continue
        if record in to_dict:
           to_dict[record] += 1
           # for not add multiple times
           if to_dict[record] == 2:
               dup_list.append(record)
           continue
        to_dict[record] = 1
    fp.close()
    reportDiff(dup_list)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit()

    call_dup(sys.argv[1], re_for_file)
