#!/usr/bin/env python

import os
from mhprocess import MyProcess
from ehandler import EHandler
from msgh import MsghMgr
from mytimer_tags import TMTAGS
from eventype import EVENTYPE
from mymsgs import MsgTestTimer
import datetime

class MysProcess(MyProcess):
    def __init__(self, msgh_mgr, msghname):
        MyProcess.__init__(self, msgh_mgr, msghname)
        self.eh = EHandler()
        self.eh.set_queue(self.queue)
        self.rqueue = None

    def _process(self):
        self.eh.register_timer(1000, TMTAGS.TEST, True)
        qid = self.msgh_mgr.findQueue("test_receive_process")
        self.rqueue = self.msgh_mgr.getQueue(qid)
        while True:
            msg = self.eh.getEvent()
            evtype = msg.get_eventype()
            msgtype = msg.get_msgtype()
            #print "------get message with evtype %s, msgtype %s, %s"%\
            #      (evtype, msgtype, os.getpid())
            if evtype == EVENTYPE.TIMEREXPIRE:
                self._send_timer_event()
            elif evtype == EVENTYPE.NORMALMSG:
                self._process_msg(msg)
            
    def _send_timer_event(self):
        #print "MysProcess::_send_timer_event"
        msg = MsgTestTimer()
        msg.set_text("denny is doing a test for timer" + \
                     str(datetime.datetime.now()))
        self.queue.send(self.rqueue, msg)

    def _process_msg(self, msg):
        msgtype = msg.get_type()
        if msgtype == MsgType.NORMAL_TEXT:
            print "got the response message", msg.get_body()
        else:
            print "MyTest::process_msg unsupport message"


class MyrProcess(MyProcess):
    def __init__(self, msgh_mgr, msghname):
        MyProcess.__init__(self, msgh_mgr, msghname)
        self.eh = EHandler()
        self.eh.set_queue(self.queue)

    def _process(self):
        while True:
            msg = self.eh.getEvent()
            self._process_msg(msg)

    def _process_msg(self, msg):
        print "got message", msg.get_body(), os.getpid()

if __name__ == "__main__":
    msgh_mgr = MsghMgr()
    sprocess = MysProcess(msgh_mgr, "test_send_process")
    rprocess = MyrProcess(msgh_mgr, "test_receive_process")
    
    sprocess.start()
    rprocess.start()
    
