#!/usr/bin/env python

# NOTE: only support one buffer read thread, only used for hisense NGB project

import sys
import re
import copy

class logTime:
    """ timestamp for each log entry, only have max as hour, no day
    or biger concept here """
    def __init__(self):
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.msec = 0

    def set(self, hour, min, sec, msec):
        self.hour = int(hour)
        self.min = int(min)
        self.sec = int(sec)
        self.msec = int(msec)

    def getMsec(self):
        """ convert to msec """
        msec = 0
        msec += self.hour * 60 * 60 * 1000000
        msec += self.min * 60 * 1000000
        msec += self.sec * 1000000
        msec += self.msec
        return msec

#### global variables ##############
g_current_read_start_time = logTime()
g_current_read_end_time = logTime()

g_prev_read_start_time = logTime()
g_prev_read_end_time = logTime()

g_report_start_lag = 20000
g_report_read_lag = 20000

# some regular expressions
blankRe = re.compile(r'/n[/s| ]*/r')
startOfreadRe = re.compile(
    r".*For blocksize algined, use direct access instead!")
endOfreadRe = re.compile(r".*Finish IO sysfd")

def log(string):
    # sys.stdout.write(string)
    print string
    
def usage():
    log("%s <file_name>"%sys.argv[0]);

def parseLog(file):
    """parse log file one line by one"""
    fp = open(file, "r")
    line = fp.readline()
    while line:
        analysisLine(line)
        line = fp.readline()
    fp.close()


def isIgnored(line):
    """ ignore the blank and comments line """
    m = blankRe.match(line)
    if m:
        return True

def getTime(timeStr):
    """ parse the time from a time string, return hour, min, msec
    example:
    121109-14:40:48:170556-500049680, return 14, 40, 48, 117783
    NOTE: the function will fail if the input line has less than
          two '-' characters
    """
    date, time, thread = timeStr.split('-')
    return time.split(':')
    
    
def isLineOfStartToRead(line):
    """ tell whether this line is the start of reading buffer """
    m = startOfreadRe.match(line)
    if m:
        return True
    return False

def isLineOfEndOfRead(line):
    """ tell whether this line is the end of reading buffer """
    m = endOfreadRe.match(line)
    if m:
        return True
    return False

def analysisLine(line):
    """ if the current line is the start of a read operation, print
    the line with ** prefix; if the line is the end of a read operation,
    print the with some indent; if the start is some later than previous
    start, report the lag; if the read use some longer time, report the
    lag """
    global g_current_read_start_time, g_current_read_end_time
    global g_prev_read_start_time, g_prev_read_end_time
    global g_report_start_lag, g_report_read_lag
    if isIgnored(line):
        return
    timeStr = line.split(' ', 1)
    hour, min, sec, msec = getTime(timeStr[0])
    if isLineOfStartToRead(line):
        print("** " + line),
        g_prev_read_start_time = copy.copy(g_current_read_start_time)
        g_current_read_start_time.set(hour, min, sec, msec)
        lagTime = reportLag(g_prev_read_start_time,
                            g_current_read_start_time,
                            g_report_start_lag)
        if (lagTime > 0):
            log("!!!!start to read too late for %d!!!!"%lagTime)
    elif isLineOfEndOfRead(line):
        print("   " + line),
        g_prev_read_end_time = copy.copy(g_current_read_end_time)
        g_current_read_end_time.set(hour, min, sec, msec)
        lagTime = reportLag(g_current_read_start_time,
                            g_current_read_end_time,
                            g_report_read_lag)
        if (lagTime > 0):
            log("   !!!!system read lag too much time for %d!!!!"%lagTime)
    else:
        pass


def reportLag(prev, current, maxLag):
    """comput the lag time for two given time, if the delta is bigger
    than than given max delta, return the delta, if not, return 0"""
    prevMsec = prev.getMsec()
    currMsec = current.getMsec()
    delta = currMsec - prevMsec
    if (delta > maxLag):
        return delta
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit()
    fileName = sys.argv[1]
    parseLog(fileName)
    
