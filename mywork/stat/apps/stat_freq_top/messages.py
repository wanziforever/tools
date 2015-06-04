#!/usr/bin/env python

import json
from msgtype import MsgType
from core.mymessage import MyMessage
from core.eventype import EVENTYPE
import zlib

def default_encoder(obj):
    return obj.__json__()

class MsgAccessFreqCalc(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgAccessFreqCalc)
        self.api = 0
        self.ts = ""

    def set_api(self, api):
        self.api = api

    def set_timestamp(self, ts):
        self.ts = ts

    def get_api(self):
        return self.api

    def get_timestamp(self):
        return self.ts

    def build(self):
        self.body = "{0}::{1}".format(self.api, self.ts)
    def parse(self):
        self.user_id, self.ts = self.body.split("::")


class MsgAccessFreqReport(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgAccessFreqReport)
        self.freq_info = []

    def add_freq_info(self, ts, count):
        self.freq_info.append([str(ts), str(count)])

    def build(self):
        self.body = '|'.join(['%s::%s'%(ts.strip(), count.strip()) \
                              for ts, count in self.freq_info])

    def parse(self):
        self.freq_info = []
        for info in self.body.split('|'):
            info = info.strip()
            if len(info) == 0:
                continue
            self.freq_info.append(info.split('::'))

    def get_freq_info(self):
        return self.freq_info

    def reset(self):
        self.body = ""
        self.freq_info = []
