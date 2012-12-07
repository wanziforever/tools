#!/usr/bin/env python

# tool used to summary the input data list by a given configured pattern
# currently only support single key summary, combined key summary will
# be supported later base request

import os
import sys
import re

# following to regular expression are used to capture valid data from
# file, the regular expression should contain only one group, and program
# will only capture the first captured group.
#captureRe = re.compile(r"\/\w+\/(\w+)"); # capture digit part of /media/12345345
#captureRe = re.compile(r"(.+)");  # capture whole line
captureRe = re.compile(r"(\/\w+\/\w+\s*\d+).*")

# group index for regular expression match, the data for this index is the
# considered as the key, 0 means the first group
key_index = 0 

# how many entries will be processed
how_many_entries_to_process = 0

class Entry:
    def __init__(self, initial_data, reglr):
        self.data = []
        self.data = captureData(initial_data, reglr)

    def getKey(self, index):
        if index >= len(self.data):
            return None
        return self.data[index]

class Summary:
    def __init__(self):
        self.key_dict = {}
        self.key_list = []

    def addCount(self, key):
        if key is None:
            return
        if key in self.key_dict:
            self.key_dict[key] += 1
        else:
            self.key_list.append(key)
            self.key_dict[key] = 1

    def report(self):
        """ print a formated report for all keys summary"""
        if len(self.key_list) == 0:
            log("there is no key provided")
            return
        for key in self.key_list:
            log("%s(%d)"%(key, self.key_dict[key]))

def log(string):
    # sys.stdout.write(string)
    print string

def logFile(text):
    global log_file
    ISOTIMEFORMAT='%Y-%m-%d %X'
    current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
    os.system("echo \"%s\n%s\" >> %s"%(current_time, text, log_file))

def open_file(file_name, mode="r"):
    """ open file, return None if fail, capture the system exception,
    and handle open file fail by self """
    try:
        fp = open(file_name, mode)
        return fp
    except:
        return None
        
def usage():
    log("***********************************************************\n"
        "script used to do summary on a given pattern on a list of entries\n"
        "Usage: %s <file_of_list_entries> \n"
        "************************************************************"
        %sys.argv[0])

def isCommented(line):
    """ check if the current line is commented out """
    commentRe = re.compile(r'\s*#.*')
    if commentRe.match(line):
        return True
    return False

def isBlank(line):
    """ check if the current line is a blank line """
    blankRe = re.compile(r'\s*[\r|\n]$')
    if blankRe.match(line):
        return True
    return False

def isIgnored(line):
    """ ignore the blank line and comment line """
    return isCommented(line) or isBlank(line)

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
    
def captureData(line, reglr):
    """ parse the input line in the file, and return the captured
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
    m = reglr.match(line)
    if not m:
        log("no match" + line)
        return []
    try:
        items = m.groups()
    except:
        log("fail to capture data for: %s, check your regular expression"%line)
        exit()
    return items


def call_summary(file_name, reglr, index, summary):
    global how_many_entries_to_process
    fp = open_file(file_name)
    if not fp:
        log("fail to open file %s"%file_name)
        exit()
    count = 0
    limited = True
    # if the number to process set to 0, means no limitation
    if how_many_entries_to_process == 0:
        limited = False
    while (not limited) or count < how_many_entries_to_process:
        line = fp.readline()
        if not line:
            break
        if isIgnored(line):
            continue
        count += 1
        line = line.strip()
        key = Entry(line, reglr).getKey(index)
        if key is None:
            continue
        summary.addCount(key)
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit()
    summary = Summary()
    file_name = sys.argv[1]
    call_summary(file_name, captureRe, key_index, summary)
    summary.report()
