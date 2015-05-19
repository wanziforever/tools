#!/usr/bin/env python

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

def default_encoder(obj):
    return obj.__json__()

class AccessUserNginxGrabber(GrabberWorker):
    def __init__(self, msgh, mgrq, myname, config):
        GrabberWorker.__init__(self, msgh, mgrq, myname, config)
        self.log_path = '/data/logs/source'
        self.work_dir = '/data/logs/work/'

    def _grab_files(self):
        nginx_files = []
        spos = int(str(self.config['log_start_ts']))
        epos = int(str(self.config['log_end_ts']))
        for f in os.listdir(self.log_path):
            if f[0:7] != 'api.vod':
                continue
            date = f[-14:-4]
            try:
                ts = int(time.mktime(time.strptime(date, "%Y%m%d%H")) * 1000)
            except Exception, e:
                continue
            if ts >= spos and ts < epos:
                nginx_files.append(f)
            nginx_files = sorted(nginx_files)
        
        return [os.path.join(self.log_path, f) for f in nginx_files]
                
    def _grab(self):
        for log_gz_file in self._grab_files():
            echo("processing %s"%log_gz_file)
            dirname = os.path.dirname(log_gz_file)
            input_file = log_gz_file
            input_file_base_name = os.path.basename(input_file)
            new_input_file = \
                os.path.join(self.work_dir, input_file_base_name[:-4])
            
            if not os.path.exists(new_input_file):
                #print 'cp %s %s'%(log_gz_file, self.work_dir)
                os.system('cp %s %s'%(log_gz_file, self.work_dir))
                #print 'cd %s;gunzip %s'%(self.work_dir, input_file_base_name)
                os.system('cd %s;bunzip2 %s'%(self.work_dir, input_file_base_name))
            fd = open(new_input_file, "r")
            for record in fd:
                self._handle_record(record)
                self.current += 1
            fd.close()

    def _handle_record(self, raw):
        e = NginxEntry(raw)
        if e.parse() is False:
            return
        if e.get_apicode() != CallAPI.FRONTPAGE:
            return
        userid = e.get_param('device_id')
        if userid is None:
            userid = e.get_param('devid')
        if userid is None:
            return
        if userid.endswith('0000'):
            mac = e.get_param('mac')
            if mac is None or mac == "null":
                return
            mac = mac.replace('%3A', '')
            userid = userid[:-8] + mac[-8:]
        msg = MsgAccessUserCalc()
        msg.set_userid(userid)
        msg.set_timestamp(e.get_ts())
        i = self.next_rrobin()
        self.queue.send(self.calc_queues[i], msg)

class AccessUserCalc(CalcWorker):
    def __init__(self, msgh, mgrq, myname, config):
        CalcWorker.__init__(self, msgh, mgrq, myname, config)
        self.report_intvl = 10
        self.user_repo = {}
        self.eh.register_timer(self.report_intvl * 1000,
                               TMTAGS.SEND_REPORT, True)

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgAccessUserCalc:
            calc_msg = MsgAccessUserCalc()
            calc_msg.cast(msg)
            calc_msg.parse()
            ts = calc_msg.get_timestamp()
            user = calc_msg.get_userid().strip()
            if user in self.user_repo:
                if ts < self.user_repo[user]:
                    self.user_repo[user] = ts
            else:
                self.user_repo[user] = ts

            self.current += 1
        else:
            super(AccessUserCalc, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.SEND_REPORT:
            self._send_report()
        else:
            super(AccessUserCalc, self)._process_timer(msg)

    def _send_report(self):
        ptr_msg = MsgAccessUserReport()
        num = 50
        i = 0
        for user, ts in self.user_repo.items():
            ptr_msg.add_user_info(user, ts)
            i += 1
            if i == num:
                self.queue.send(self.mgrq, ptr_msg)
                ptr_msg.reset()
                i = 0
        self.user_repo = {}
        self.queue.send(self.mgrq, ptr_msg)

    def _final(self):
        self._send_report()
        super(AccessUserCalc, self)._final()
        
class AccessUserCalcMgr(CalcManager):
    def __init__(self, msgh, config):
        CalcManager.__init__(self, msgh)
        self.report_fd = None
        self.collectors = {}
        self.config = config
        self.stat_user = StatUser(config['start'], config['end'])
        self.analysis_time = StatTime(config['start_analysis'],
                                      config['end_analysis'])
        self.rpt_print_intvl = 40
        self.commit_intvl = 30
        self.eh.register_timer(self.commit_intvl * 1000,
                               TMTAGS.DB_COMMIT, True)
        self.db = Mydb()
        self.db.connect('repository')
        self.dbsession = self.db.open('all_users')

    def set_config(self, config):
        self.config = config

    def _process_msg(self, msg):
        debug("AccessUserCalcMgr::_process_msg() enter")
        msgtype = msg.get_msgtype()
        #print "--------------process msg", datetime.datetime.now()
        if msgtype == MsgType.MsgAccessUserReport:
            debug("AccessUserCalcMgr::_process_msg() got "
                  "report message %s"%msg.get_body())
            ptr_msg = MsgAccessUserReport()
            ptr_msg.cast(msg)
            ptr_msg.parse()
            #print ptr_msg.get_users_info()
            for user, ts in ptr_msg.get_users_info():
                entry = self.dbsession.select({'user': user})
                if entry is None:
                    self.dbsession.insert({'user': user, 'timestamp': ts})
                else:
                    #print "entry----", entry
                    exist_ts = entry[1][1]
                    if ts < exist_ts:
                        #print "ts < exists", ts, exist_ts
                        self.dbsession.update({'user':user, 'ts': ts})
            
        else:
            super(AccessUserCalcMgr, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.DB_COMMIT:
            self.dbsession.commit()
        else:
            super(AccessUserCalcMgr, self)._process_timer(msg)
        #super(AccessUserCalcMgr, self)._process_timer(msg)

    def _print_report(self):
        entries = self.dbsession.select("*")
        for key, entry in entries:
            userid = entry[0]
            ts = entry[1]
            self.analysis_time.stat_count(int(ts))
        infos = self.analysis_time.show_info()
        days_map = sorted(infos.items(), key=lambda info:info[0], reverse=False) 
        total = 0
        ret = []
        for day, count in days_map:
            total += count
            ret.append([day, total])
        print ret

    def _final(self):
        echo("going to generate final report ...")
        self._print_report()
        self.dbsession.close()
        echo("report generation completed")
        super(AccessUserCalcMgr, self)._final()

    
