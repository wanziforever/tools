#!/usr/bin/env python

from mymessage import MyMessage
from msgtype import MsgType
from eventype import EVENTYPE

class MsgTestTimer(MyMessage):
    def __init__(self, msgtype=MsgType.NORMAL_TEXT):
        MyMessage.__init__(self, evtype=EVENTYPE.TIMEREXPIRE, msgtype=msgtype)
        
    def set_text(self, txt):
        self.body = txt
