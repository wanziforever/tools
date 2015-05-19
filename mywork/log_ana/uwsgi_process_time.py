#!/usr/bin/env python

logfile = "uwsgi.log-20150222"
threshold = 100

def is_valid_line(line):
    ''' only treat the with first chars as "[pid:" as valid '''
    if len(line) < 5:
        return False
    
    if line[:5] == "[pid:":
        return True
    return False

def capture_duration(line):
    tokens = line.split()
    duration = 0
    try:
        duration = int(tokens[23])
    except:
        duration = -1
    return duration

def examine(duration):
    if duration > threshold:
        return False
    return True
        
def call_ana():
    fd = open(logfile, "r")
    for line in fd:
        line = line.strip()
        if not is_valid_line(line):
            continue
        duration = capture_duration(line)
        if duration == -1:
            print "invalid duration", line
        if not examine(duration):
            print duration, line
        

if __name__ == "__main__":
    call_ana()
