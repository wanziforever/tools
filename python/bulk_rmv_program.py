#!/usr/bin/env python
"""
tool used to do operation on a list of entrys, and these entrys were
defined in a given file

NOTE: the tool do not support shell buildin command, the command should
      exist as a file 
"""

import sys
import re
import subprocess
import os

# command which used to operate on entries, %s was used to be replace by
# entry
command_file = "/usr/local/fountain/utils/del_files"
command_argument = "-h 127.0.0.1 -p 8888 -f"
# following to regular expression are used to capture valid data from
# file, the regular expression should contain only one group, and program
# will only capture the first captured group.
#captureRe = re.compile(r"\/\w+\/(\w+)");
captureRe = re.compile(r"(.+)");

entry_list = []

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
        "script used to do some operation on a given list of entries"
        "Usage: %s <file_of_list_entries>\n"
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

def commandOnEntries(slist, command):
    """ operate the command on each entry """
    for entry in slist:
        full_command = command + " " + entry.getValidData()
        print full_command
        subprocess.call(command, shell=True)

def checkCommandFileExist(path):
    if os.path.exists(path):
        return True
    return False
    
def call_rmv(file_name, expression, command_file, argument):
    global entry_list
    putRecordToList(file_name, expression, entry_list)
    command = command_file + " " +  argument
    commandOnEntries(entry_list, command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit()

    if not checkCommandFileExist(command_file):
        log("command file not exist: %s"%command_file)
        exit()
    file_of_list_entries = sys.argv[1]
    
    call_rmv(file_of_list_entries, captureRe, command_file, command_argument)


