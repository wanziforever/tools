#!/usr/bin/env python

import os
import sys
import time
import threading
from core.mhprocess import MyProcess
from common.echo import echo, debug
from tmtags import TMtagsComm
from core.eventype import EVENTYPE
from messages import *

class CalcWorker(MyProcess):
    def __init__(self, msgh, mgrq, myname, config):
        MyProcess.__init__(self, msgh, myname)
        self.mgrq = mgrq
        self.count = 0
        self.current = 0
        self.recent_current = 0
        self.rate_intvl = 1
        self.rate = 0
        self.config = config
        self.calc_queues = []
        self.report_intvl = 5
        self.thr = None

    def _process(self):
        self._init_timers()
        while self.finish is False:
            msg = self.eh.getEvent()
            if msg is None:
                debug("no message not, continue")
            evtype = msg.get_eventype()
            if evtype == EVENTYPE.TIMEREXPIRE:
                self._process_timer(msg)
            elif evtype == EVENTYPE.NORMALMSG:
                self._process_msg(msg)

    def _final(self):
        self._notify_manager_quit()

    def set_config(self, config):
        self.config = config

    def _init_timers(self):
        self.eh.register_timer(self.report_intvl * 1000,
                               TMtagsComm.REPORT_STATUS,
                               True)
        self.eh.register_timer(self.rate_intvl * 1000,
                               TMtagsComm.PROCESS_RATE,
                               True)
        

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMtagsComm.REPORT_STATUS:
            self._report_progress()
        elif tag == TMtagsComm.PROCESS_RATE:
            self._process_rate()

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgWorkerQuit:
            self._report_progress()
            self.finish = True

    def _notify_manager_quit(self):
        msg = MsgWorkerQuit()
        self.queue.send(self.mgrq, msg)

    def _calc(self, msg):
        #print "CalcWorker test message"
        tmsg = MsgTest()
        tmsg.cast(msg)
        text = tmsg.get_text()
        print "%s got a message: %s"%(self.msgh_name, text)
        self.current += 1

    def _process_rate(self):
        self.rate = (self.current - self.recent_current) / self.rate_intvl
        self.recent_current = self.current

    def _report_progress(self):
        #debug("GrabberWorker [%s] _report_status()"%os.getpid())
        msg = MsgProgressReport()
        msg.set_current(self.current)
        msg.set_rate(self.rate)
        msg.set_total(self.count)
        msg.set_current(self.current)
        msg.build()
        self.queue.send(self.mgrq, msg)
        
