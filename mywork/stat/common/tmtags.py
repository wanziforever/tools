#!/usr/bin/env python

def enum(start=0, *sequential):
    enums = dict(zip(sequential, range(start, len(sequential)+start)))
    return type('Enum', (), enums)

class TMtagsComm(object):
    INVALID = 0
    REPORT_STATUS = 1
    GRABBER_ALIVE = 2
    PROCESS_RATE = 3
    TEST = 4

    STAT_PLAY_TIMES = 10000
