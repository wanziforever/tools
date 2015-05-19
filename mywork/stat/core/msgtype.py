#!/usr/bin/env python
''' define the message type base enum values, each application who
want to define its own message, should declare in this file '''

def enum(start=0, *sequential):
    enums = dict(zip(sequential, range(start, len(sequential)+start)))
    return type('Enum', (), enums)

class MsgTypeBase(object):
    INVALID = 0
    NORMAL_TEXT = 1
    TIMEREXP = 2

    COMMON = 10000
    STAT_ACTIVE_USER = 20000
    STAT_PLAY_USER = 21000
    STAT_PLAY_TIME = 22000
    STAT_TOP_MEDIAS = 23000
    STAT_ACCESS_USER = 24000
    STAT_ACCESS_FREQ = 25000

