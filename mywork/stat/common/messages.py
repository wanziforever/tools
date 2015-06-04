import json
import time
from msgtype import MsgType
from core.mymessage import MyMessage
from core.eventype import EVENTYPE

class MsgCalcStart(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgCalcStart)
        self.count = 0
        self.queue_names = []

    def set_count(self, count):
        self.count = count

    def addQueue(self, qname):
        self.queue_names.append(qname)

    def getQueues(self):
        return self.queue_names

    def build(self):
        self.body = "::".join(self.queue_names)

    def parse(self):
        self.queue_names = self.body.split("::")


class MsgProgressReport(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgProgressReport)
        self.rate = 0
        self.current = 0
        self.total = 0
        self.left = 0
        self.expected_time = 0
        self.ts = 0

    def set_rate(self, rate):
        self.rate = rate

    def get_rate(self):
        return self.rate

    def set_current(self, c):
        self.current = c

    def get_current(self):
        return self.current

    def set_total(self, total):
        self.total = total

    def get_total(self):
        return self.total

    #def set_left(self, left):
    #    self.left = left
    #
    def get_left(self):
        return self.left

    def get_expected_time(self):
        return self.expected_time

    def get_ts(self):
        return self.ts

    def build(self):
        if self.total == 0:
            self.left = 0
        else:
            self.left = self.total - self.current
            
        if self.rate == 0 :
            self.expected_time = 9999999
        else:
            self.expected_time = int(self.left / self.rate)

        self.ts = int(time.time())
        
        self.body = "::".join([str(self.current), str(self.rate),
                               str(self.total), str(self.left),
                               str(self.expected_time), str(self.ts)])

    def parse(self):
        current, rate, total, left, expected_time, ts \
                 = self.body.split("::")
        self.current, self.rate = int(current), int(rate)
        self.total, self.left = int(total), int(left)
        self.expected_time, self.ts = int(expected_time), int(ts)

class MsgGrabberQuit(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgGrabberQuit)

class MsgWorkerQuit(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgWorkerQuit)

class MsgTest(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, evtype=EVENTYPE.NORMALMSG,
                           msgtype=MsgType.MsgTest)
    def set_text(self, txt):
        self.body = txt

    def get_text(self):
        return self.body
