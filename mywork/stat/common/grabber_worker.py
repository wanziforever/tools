#!/usr/bin/env python

import os
import time
import threading
import datetime
from core.mhprocess import MyProcess
from common.echo import echo, debug, warn, err
from tmtags import TMtagsComm
from core.eventype import EVENTYPE
from messages import *

class GrabberWorker(MyProcess):
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
        self.alive_chk_intvl = 1
        self.thr = None
        self.calc_queues = []
        self.rrobin = -1

    class GrabberThread(threading.Thread):
        def __init__(self, name, grab_func):
            threading.Thread.__init__(self, name=name)
            self.func = grab_func

        def run(self):
            self.func()

    def next_rrobin(self):
        if self.rrobin + 1 == len(self.calc_queues):
            self.rrobin = 0
        else:    
            self.rrobin += 1
        return self.rrobin
        
    def attach_calcs(self, qnames):
        for name in qnames:
            qid = self.msgh.findQueue(name.strip())
            queue = self.msgh.getQueue(qid)
            self.calc_queues.append(queue)

    def set_config(self, config):
        self.config = config

    def _process(self):
        debug("GraberWorker::_process() enter")
        self._init_timers()
        self.thr = GrabberWorker.GrabberThread(
            self.msgh_name+"_thread", self._grab)
        self.thr.start()

        while self.finish is False:
            msg = self.eh.getEvent()
            if msg is None:
                debug("no message got, continue")
                continue
            evtype = msg.get_eventype()
            if evtype == EVENTYPE.TIMEREXPIRE:
                self._process_timer(msg)
            elif evtype == EVENTYPE.NORMALMSG:
                self._process_msg(msg)
        

    def _final(self):
        debug("GrabberWorker [%s] _final() "%os.getpid())
        self._report_status()
        wq_msg = MsgWorkerQuit()
        self.queue.send(self.mgrq, wq_msg)

    def _grab(self):
        debug("GrabberWorker [%s] _grab() start"%os.getpid())
        self.count = 70
        while True:
            self.current += 1
            time.sleep(0.1)
            if self.current > self.count:
                break
            tmsg = MsgTest()
            tmsg.set_text("a test message send from %s at %s"%\
                          (self.msgh_name, str(datetime.datetime.now())))
            i = self.next_rrobin()
            self.queue.send(self.calc_queues[i], tmsg)
            
            
        debug("GrabberWorker [%s] _grab() finish"%os.getpid())

    def _init_timers(self):
        debug("GrabberWorker [%s] _init_timers()"%os.getpid())
        self.eh.register_timer(self.report_intvl * 1000,
                               TMtagsComm.REPORT_STATUS,
                               True)
        self.eh.register_timer(self.alive_chk_intvl * 1000,
                               TMtagsComm.GRABBER_ALIVE,
                               True)
        self.eh.register_timer(self.rate_intvl * 1000,
                               TMtagsComm.PROCESS_RATE,
                               True)

    def _process_msg(self, msg):
        debug("GrabberWorker [%s] _process_msg"%os.getpid())

    def _process_timer(self, msg):
        #print "GrabberWorker [%s] _process_timer"%os.getpid()
        tag = msg.get_tag()
        if tag == TMtagsComm.REPORT_STATUS:
            self._report_status()
        elif tag == TMtagsComm.GRABBER_ALIVE:
            if self._check_grabber_alive() is not True:
                self.finish = True
        elif tag == TMtagsComm.PROCESS_RATE:
            self._process_rate()

    def _process_rate(self):
        self.rate = (self.current - self.recent_current) / self.rate_intvl
        self.recent_current = self.current
        
    def _report_status(self):
        #print "GrabberWorker [%s] _report_status()"%os.getpid()
        msg = MsgProgressReport()
        msg.set_current(self.current)
        msg.set_rate(self.rate)
        msg.set_total(self.count)
        self.queue.send(self.mgrq, msg)
        

    def _check_grabber_alive(self):
        #echo("GrabberWorker [%s] _check_grabber_alive working thread "
        #     "alive(%s)"%(os.getpid(), str(self.thr.is_alive())))
        return self.thr.is_alive()
