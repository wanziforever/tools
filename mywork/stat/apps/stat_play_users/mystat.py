#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.grabber_manager import GrabberManager
from common.grabber_worker import GrabberWorker
from common.calc_manager import CalcManager
from common.calc_worker import CalcWorker
from common.echo import echo, debug, warn, err
from tmtags import TMTAGS
from msgtype import MsgType
from pymongo import MongoClient
from bson.objectid import ObjectId
from messages import *
from common.vender_info import vender_dict
from common.stat_time import StatTime
from common.stat_user import UsersInfo, StatUser
from core.mydb import Mydb
from common.log_entry_def import *
from common.nginx_log_entry_def import *
import datetime
import json
import os
import time

mongo_host = "127.0.0.1"
mongo_port = 27017

def default_encoder(obj):
    return obj.__json__()

class PlayUserGrabber(GrabberWorker):
    def __init__(self, msgh, mgrq, myname, config):
        GrabberWorker.__init__(self, msgh, mgrq, myname, config)
        self.log_path = '/data/logs/source'
        self.work_dir = '/data/logs/work/'

    def _grab_files(self):
        spos = int(str(self.config['log_start_ts']))
        epos = int(str(self.config['log_end_ts']))
        ret = []
        dates = []
        for f in os.listdir(self.log_path):
            if f[0:4] != 'vod_' or f[-7:] != '.log.gz':
                continue
            date = f[4:18]
            try:
                ts = int(time.mktime(time.strptime(date, "%Y%m%d%H%M%S")) * 1000)
            except Exception, e:
                continue
            #print ts, spos, epos, datetime.datetime.fromtimestamp(ts/1000), datetime.datetime.fromtimestamp(spos/1000), datetime.datetime.fromtimestamp(epos/1000)
            if ts >= spos and ts < epos:
                dates.append(f)
            dates = sorted(dates)
        return [os.path.join(self.log_path, f) for f in dates]
                
    def _grab(self):
        for log_gz_file in self._grab_files():
            echo("processing %s"%log_gz_file)
            dirname = os.path.dirname(log_gz_file)
            input_file = log_gz_file
            input_file_base_name = os.path.basename(input_file)
            new_input_file = \
                os.path.join(self.work_dir, input_file_base_name[:-3])
            
            if not os.path.exists(new_input_file):
                print 'cp %s %s'%(log_gz_file, self.work_dir)
                os.system('cp %s %s'%(log_gz_file, self.work_dir))
                print 'cd %s;gunzip %s'%(self.work_dir, input_file_base_name)
                os.system('cd %s;gunzip %s'%(self.work_dir, input_file_base_name))
            fd = open(new_input_file, "r")
            for record in fd:
                code = record[4:8]
                if code != '5010':
                    continue
                
                self._handle_record(record)
                self.current += 1
            fd.close()
            #os.system('cd %s; gzip %s'%(dirname, input_file))

    def _handle_record(self, raw):
        e = gen_entry(raw)
        if e.parse() is False:
            return
        msg = MsgPlayUserCalc()
        msg.set_userid(e.get_userid())
        msg.set_timestamp(e.get_ts())
        msg.set_vender(e.get_vender())
        i = self.next_rrobin()
        self.queue.send(self.calc_queues[i], msg)

class PlayUserCalc(CalcWorker):
    def __init__(self, msgh, mgrq, myname, config):
        CalcWorker.__init__(self, msgh, mgrq, myname, config)
        self.report_intvl = 4
        self.report_threshold = 50
        self.stat_user = StatUser(self.config['start'], self.config['end'])

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgPlayUserCalc:
            calc_msg = MsgPlayUserCalc()
            calc_msg.cast(msg)
            calc_msg.parse()
            ts = calc_msg.get_timestamp()
            user = calc_msg.get_userid()
            vender = calc_msg.get_vender()
            if vender in vender_dict:
                vender = vender_dict[vender]
            if ts.find('.') != -1 or ts.isdigit() is False:
                warn("invalid timestamp %s for user %s"%(ts, user))
                return
            self.stat_user.mark(user, ts, vender)
            
            if self.stat_user.count_user() > self.report_threshold:
                self._send_report()
            self.current += 1
        else:
            super(PlayUserCalc, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.SEND_REPORT:
            self._send_report()
        else:
            super(PlayUserCalc, self)._process_timer(msg)

    def _send_report(self):
        ptr_msg = MsgPlayUserReport()
        ptr_msg.set_report_info(
            self.stat_user.show_user_info())
        self.queue.send(self.mgrq, ptr_msg)
        self.stat_user.clear_data()

    def _final(self):
        self._send_report()
        super(PlayUserCalc, self)._final()
        
class PlayUserCalcMgr(CalcManager):
    def __init__(self, msgh, config):
        CalcManager.__init__(self, msgh)
        self.report_fd = None
        self.collectors = {}
        self.config = config
        self.stat_user = StatUser(config['start'], config['end'])
        self.rpt_print_intvl = 40
        #self.eh.register_timer(self.rpt_print_intvl * 1000,
        #                       TMTAGS.PRINT_REPORT, True)
        self.db = Mydb()
        self.db.connect('report')

    def set_config(self, config):
        self.config = config

    def _process_msg(self, msg):
        debug("PlayUserCalcMgr::_process_msg() enter")
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgPlayUserReport:
            debug("PlayUserCalcMgr::_process_msg() got "
                  "report message %s"%msg.get_body())
            ptr_msg = MsgPlayUserReport()
            ptr_msg.cast(msg)
            data = json.loads(ptr_msg.get_report_info())
            for user, play_info in data.items():
                self.stat_user.merge_user_info(user, play_info)

        else:
            super(PlayUserCalcMgr, self)._process_msg(msg)

    def _process_timer(self, msg):
        #tag = msg.get_tag()
        #if tag == TMTAGS.PRINT_REPORT:
        #    self._print_report()
        #else:
        #    super(PlayUserCalcMgr, self)._process_timer(msg)
        super(PlayUserCalcMgr, self)._process_timer(msg)

    def _print_report(self):
        self._user_report_total()
        self._user_report_day()
        self._times_report_total()
        self._times_report_day()

    def _final(self):
        echo("going to generate final report ...")
        self._print_report()
        echo("report generation completed")
        super(PlayUserCalcMgr, self)._final()

    def _user_report_total(self):
        venders = self.stat_user.gen_stat_users_by_vender()
        self.dbsession = self.db.open('play_users_total')
        data = {"vender": "",
                'date': '%s_%s'%(self.config['start'],
                                 self.config['end']),
                'count': 0}
        for vender, count in venders.items():
            data['vender'] = vender
            data['count'] = count
            self.dbsession.insert(data)
        self.dbsession.commit()
        
        data['vender'] = "HISENSE"
        data['count'] = self.stat_user.count_user()
        self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()
        
    def _user_report_day(self):
        venders = self.stat_user.gen_stat_users_by_vender_per_day()
        self.dbsession = self.db.open('play_users_day')
        data = {"vender": "",
                'date': "",
                'count': 0}
        for vender, stat_time in venders.items():
            infos = stat_time.show_info()
            data['vender'] = vender
            for day, count in infos.items():
                data['date'] = day
                data['count'] = count
                self.dbsession.insert(data)
        self.dbsession.commit()

        infos = self.stat_user.gen_stat_users().show_info()
        data['vender'] = 'HISENSE'
        for day, count in infos.items():
            data['date'] = day
            data['count'] = count
            self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()

    def _times_report_total(self):
        venders = self.stat_user.gen_stat_count_by_vender()
        self.dbsession = self.db.open('play_times_total')
        data = {"vender": "",
                'date': '%s_%s'%(self.config['start'],
                                 self.config['end']),
                'count': 0}
        for vender, count in venders.items():
            data['vender'] = vender
            data['count'] = count
            self.dbsession.insert(data)
        self.dbsession.commit()

        data['vender'] = "HISENSE"
        data['count'] = self.stat_user.gen_stat_count()
        self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()

    def _times_report_day(self):
        venders = self.stat_user.gen_stat_count_by_vender_per_day()
        self.dbsession = self.db.open('play_times_day')
        data = {"vender": "",
                'date': "",
                'count': 0}
        for vender, stat_time in venders.items():
            infos = stat_time.show_info()
            data['vender'] = vender
            for day, count in infos.items():
                data['date'] = day
                data['count'] = count
                self.dbsession.insert(data)
        self.dbsession.commit()

        infos = self.stat_user.gen_stat_times().show_info()
        data['vender'] = 'HISENSE'
        for day, count in infos.items():
            data['date'] = day
            data['count'] = count
            self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()
