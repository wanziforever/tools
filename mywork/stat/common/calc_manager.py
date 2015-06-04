#!/usr/bin/env python

import datetime
from core.mhprocess import MyProcess
from common.echo import echo, debug
from messages import *
from tmtags import TMtagsComm
from core.eventype import EVENTYPE
from msgtype import MsgType

class CalcManager(MyProcess):
    def __init__(self, msgh):
        MyProcess.__init__(self, msgh, "CalcManager")
        self.config = None
        self.report_intvl = 5
        self.workers_data = {}
        self._init_timers()

    def set_config(self, config):
        self.config = config
        
    def set_worker(self, name, cl, config):
        self.workers_data[name] = {'cl': cl,
                                   "config": config,
                                   'status': False,
                                   'total': 0,
                                   'current': 0,
                                   'rate': 0,
                                   'left': 0,
                                   'exp_time': 0,
                                   'ts': 0}

    def _start_workers(self):
        for worker, data in self.workers_data.items():
            wc = data['cl'](self.msgh, self.queue, worker, data['config'])
            wc.start()
            if wc.is_alive():
                data['status'] = True

        return True

    def _stop_workers(self):
        wq_msg = MsgWorkerQuit()
        for qname, status in self.workers_data.items():
            if status is False:
                continue
            qid = self.msgh.findQueue(qname)
            queue = self.msgh.getQueue(qid)
            self.queue.send(queue, wq_msg)

    def notice_grabber_start(self):
        debug("CalcManage::notice_grabber_start()")
        cs_msg = MsgCalcStart()
        for qname, data in self.workers_data.items():
            if data['status'] is False:
                continue
            cs_msg.addQueue(qname)
                
        qid = self.msgh.findQueue("GrabberManager")
        grabber_mgr_q = self.msgh.getQueue(qid)
        self.queue.send(grabber_mgr_q, cs_msg)

    def _process(self):
        if self._start_workers() is False:
            return False

        self.notice_grabber_start()
        while self.finish is False:
            msg = self.eh.getEvent()
            evtype = msg.get_eventype()
            if evtype == EVENTYPE.TIMEREXPIRE:
                self._process_timer(msg)
            elif evtype == EVENTYPE.NORMALMSG:
                self._process_msg(msg)

    def _init_timers(self):
        self.eh.register_timer(self.report_intvl * 1000,
                               TMtagsComm.REPORT_STATUS,
                               True)
    
    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgGrabberQuit:
            self._stop_workers()
        elif msgtype == MsgType.MsgWorkerQuit:
            process_name = msg.get_header().get_sender()
            echo("CalcManager::Notice worker \"%s\" quit"%process_name)
            if process_name in self.workers_data:
                self.workers_data[process_name]['status'] = False

            all_quit = True
            for pname, data in self.workers_data.items():
                if data['status'] is True:
                    all_quit = False
                    break
            if all_quit is True:
                echo("CalcManager::All calculation workers quit")
                echo("CalcManager::i quit")
                self.finish = True
        elif msgtype == MsgType.MsgProgressReport:
            self._handle_progress_msg(msg)
            
    def _handle_progress_msg(self, msg):
        sr_msg = MsgProgressReport()
        sr_msg.cast(msg)
        sr_msg.parse()
        current = sr_msg.get_current()
        rate = sr_msg.get_rate()
        total = sr_msg.get_total()
        left = sr_msg.get_left()
        ts = sr_msg.get_ts()
        expect_time = sr_msg.get_expected_time()
        name = sr_msg.get_header().get_sender().strip()
        data = self.workers_data[name]
        data['total'], data['rate'], data['left'] = total, rate, left
        data['exp_time'], data['ts'] = expect_time, ts
        data['current'] = current

    def _process_timer(self, msg):
        #debug("calc_manager::_process_timer()")
        tag = msg.get_tag()
        if tag == TMtagsComm.REPORT_STATUS:
            self._report_progress()

    def _report_progress(self):
        s = ""
        for name, data in self.workers_data.items():
            s = "{0} --> cur: {1}, total: {2}, left: {3}, rate: {4}, "\
                 "exp: {5}".format(
                name, data['current'], data['total'],
                data['left'],data['rate'],
                datetime.timedelta(seconds=int(data['exp_time'])))
            echo(s)
