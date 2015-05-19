#!/usr/bin/env python

import datetime
from core.mhprocess import MyProcess
from common.echo import echo, debug, warn
from msgtype import MsgType
from core.eventype import EVENTYPE
from messages import *
from tmtags import TMtagsComm

class GrabberManager(MyProcess):
    def __init__(self, msgh):
        MyProcess.__init__(self, msgh, "GrabberManager")
        self.config = None
        self.workers_data = {}
        self.report_intvl = 5

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
        debug("GrabberManager::_start_worker() starting workers")
        for worker, data in self.workers_data.items():
            wc = data['cl'](self.msgh, self.queue, worker, data['config'])
            wc.attach_calcs(self.calc_names)
            wc.start()
            if wc.is_alive():
                data['status'] = True

    def _init_timers(self):
        self.eh.register_timer(self.report_intvl * 1000,
                               TMtagsComm.REPORT_STATUS,
                               True)

    def _stop_workers(self):
        pass

    def _final(self):
        self._notice_calc_finish()

    def _process(self):
        self._init_timers()
        while self.finish is False:
            msg = self.eh.getEvent()
            evtype = msg.get_eventype()
            if evtype == EVENTYPE.TIMEREXPIRE:
                self._process_timer(msg)
            elif evtype == EVENTYPE.NORMALMSG:
                self._process_msg(msg)

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgCalcStart:
            echo("GrabberManager::calculation workers are ready")
            cs_msg = MsgCalcStart()
            cs_msg.cast(msg)
            cs_msg.parse()
            self.calc_names = cs_msg.getQueues()
            echo("GrabberManager::total %s calculation workers"%len(self.calc_names))
            self._start_workers()

        elif msgtype == MsgType.MsgWorkerQuit:
            process_name = msg.get_header().get_sender()
            echo("GrabberManager::Notice worker \"%s\" quit"%process_name)
            if process_name in self.workers_data:
                self.workers_data[process_name]['status'] = False

            all_quit = True
            for pname, data in self.workers_data.items():
                if data['status'] is True:
                    all_quit = False
                    break
            if all_quit is True:
                echo("GrabberManager::All grabber workers quit")
                echo("GrabberManager::i quit")
                self.finish = True

        elif msgtype == MsgType.MsgProgressReport:
            self._handle_report_msg(msg)

    def _handle_report_msg(self, msg):
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
        

    def _report_progress(self):
        s = ""
        for name, data in self.workers_data.items():
            completed = 0.0
            if int(data['total']) == 0:
                completed = 0.0
            else:
                completed = int(float(data['current']) / float(data['total']) * 100)
            status = ''
            if data['status'] is False:
                status = '[QUIT]'
            s = "{7}{0} --> cur: {1}, total: {2}, left: {3}({6}%), rate: {4}, "\
                    "exp: {5}".format(
                    name, data['current'], data['total'],
                    data['left'],data['rate'],
                    datetime.timedelta(seconds=int(data['exp_time'])),
                    completed, status)
            echo(s)
            

    def _notice_calc_finish(self):
        echo("GrabberManager::notice to calculation processes "
             "the work has been finished")
        gq_msg = MsgGrabberQuit()
        qid = self.msgh.findQueue("CalcManager")
        queue = self.msgh.getQueue(qid)
        if queue is None:
            warn("GrabberManager::_notice_calc_finish() cann not find queue"
                 "with name calcManager")
            return 
        self.queue.send(queue, gq_msg)
        

    def _process_timer(self, msg):
        #echo("GrabberManager::_process_timer() enter")
        tag = msg.get_tag()
        if tag == TMtagsComm.REPORT_STATUS:
            self._report_progress()
