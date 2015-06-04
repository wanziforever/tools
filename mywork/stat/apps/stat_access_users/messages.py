#!/usr/bin/env python

import json
from msgtype import MsgType
from core.mymessage import MyMessage
from core.eventype import EVENTYPE
import zlib

def default_encoder(obj):
    return obj.__json__()

class MsgAccessUserCalc(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgAccessUserCalc)
        self.user_id = ""
        self.ts = ""

    def set_userid(self, userid):
        self.user_id = userid

    def set_timestamp(self, ts):
        self.ts = ts

    def get_userid(self):
        return self.user_id

    def get_timestamp(self):
        return self.ts

    def build(self):
        self.body = "{0}::{1}".format(self.user_id,
                                           self.ts)
    def parse(self):
        self.user_id, self.ts = self.body.split("::")


class MsgAccessUserReport(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgAccessUserReport)
        self.users_info = []
    def add_user_info(self, user, ts):
        self.users_info.append([user, ts])

    def build(self):
        self.body = '|'.join(['%s::%s'%(user.strip(), ts.strip()) \
                              for user, ts in self.users_info])

    def parse(self):
        self.users_info = []
        for info in self.body.split('|'):
            info = info.strip()
            if len(info) == 0:
                continue
            self.users_info.append(info.strip().split('::'))

    def get_users_info(self):
        return self.users_info

    def reset(self):
        self.body = ""
        self.users_info = []
