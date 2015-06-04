#!/usr/bin/env python

import json
from msgtype import MsgType
from core.mymessage import MyMessage
from core.eventype import EVENTYPE
import zlib

def default_encoder(obj):
    return obj.__json__()

class MsgActiveUserCalc(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgActiveUserCalc)
        self.user_id = ""
        self.ts = ""
        self.vender = ""

    def set_userid(self, userid):
        self.user_id = userid

    def set_timestamp(self, ts):
        self.ts = ts

    def set_vender(self, vender):
        self.vender = vender

    def get_userid(self):
        return self.user_id

    def get_timestamp(self):
        return self.ts

    def get_vender(self):
        return self.vender

    def build(self):
        self.body = "{0}::{1}::{2}".format(self.user_id,
                                           self.ts,
                                           self.vender)
    def parse(self):
        self.user_id, self.ts, self.vender = self.body.split("::")


class MsgActiveUserReport(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgActiveUserReport)
    def set_report_info(self, data):
        #self.body = zlib.compress(
        #    json.dumps(data, default=default_encoder)
        #    )
        #self.body = json.dumps(data, default=default_encoder)
        self.body = data

    def get_report_info(self):
        #return json.loads(zlib.decompress(self.body, zlib.MAX_WBITS|32))
        #return json.loads(self.body)
        return self.body
