#!/usr/bin/env python
''' define all the event type, currently only timer and socket
message event were supported '''

class EVENTYPE(object):
    INVALID = 0
    TIMEREXPIRE = 1
    NORMALMSG = 2
