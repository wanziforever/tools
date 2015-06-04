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

mongo_host = "127.0.0.1"
mongo_port = 27017

def default_encoder(obj):
    return obj.__json__()

class ActiveUserNginxGrabber(GrabberWorker):
    def __init__(self, msgh, mgrq, myname, config):
        GrabberWorker.__init__(self, msgh, mgrq, myname, config)
        self.log_path = '/data/logs/source/'
        self.work_dir = '/data/logs/work/'
        self.ip_mapping = {}

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
            #while True:
            #    lines = fd.readlines(100000)
            #    if lines is None:
            #        break
            #    for line in lines:
            #        self._handle_record(line)
            #        self.current += 1
            fd.close()
            #os.system('cd %s; gzip %s'%(dirname, input_file))

    def _handle_record(self, raw):
        e = NginxEntry(raw)
        if e.parse() is False:
            return
        userid = ""
        if e.get_apicode() == CallAPI.FRONTPAGE:
            devid = e.get_param('device_id')
            if devid is None:
                return
            self.ip_mapping[e.get_ip()] = devid
            return
        else:
            if e.get_ip() not in self.ip_mapping:
                return
            userid = self.ip_mapping[e.get_ip()]
        msg = MsgActiveUserCalc()
        msg.set_userid(userid)
        msg.set_timestamp(e.get_ts())
        msg.set_vender(e.get_vender())
        i = self.next_rrobin()
        self.queue.send(self.calc_queues[i], msg)

class ActiveUserGrabber(GrabberWorker):
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
            date = f[4:12]
            try:
                ts = int(time.mktime(time.strptime(date, "%Y%m%d")) * 1000)
            except Exception, e:
                continue
            if ts >= spos and ts < epos:
                dates.append(f)
            dates = sorted(dates)
        return [os.path.join(self.log_path, f) for f in dates]
                
    def _grab(self):
        for log_gz_file in self._grab_files():
            echo("processing %s"%log_gz_file)
            dirname = os.path.dirname(log_gz_file)
            input_file = log_gz_file[:-3]
            input_file_base_name = os.path.basename(input_file)
            new_input_file = \
                os.path.join(self.work_dir, input_file_base_name)
            
            if not os.path.exists(new_input_file):
                #print 'cp %s %s'%(log_gz_file, self.work_dir)
                os.system('cp %s %s'%(log_gz_file, self.work_dir))
                #print 'cd %s;gunzip %s'%(self.work_dir, input_file_base_name)
                os.system('cd %s;gunzip %s'%(self.work_dir, input_file_base_name))
            fd = open(new_input_file, "r")
            for record in fd:
                code = record[4:8]
                if code != "5010" and code != "5049" and \
                       code != "5054" and code != "5001":
                    continue
                
                self._handle_record(record)
                self.current += 1
            fd.close()
            #os.system('cd %s; gzip %s'%(dirname, input_file))

    def _handle_record(self, raw):
        e = gen_entry(raw)
        if e.parse() is False:
            return
        msg = MsgActiveUserCalc()
        msg.set_userid(e.get_userid())
        msg.set_timestamp(e.get_ts())
        msg.set_vender(e.get_vender())
        i = self.next_rrobin()
        self.queue.send(self.calc_queues[i], msg)

class ActiveUserCalc(CalcWorker):
    def __init__(self, msgh, mgrq, myname, config):
        CalcWorker.__init__(self, msgh, mgrq, myname, config)
        self.report_intvl = 4
        self.report_threshold = 50
        self.stat_user = StatUser(self.config['start'], self.config['end'])

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgActiveUserCalc:
            calc_msg = MsgActiveUserCalc()
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
            super(ActiveUserCalc, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.SEND_REPORT:
            self._send_report()
        else:
            super(ActiveUserCalc, self)._process_timer(msg)

    def _send_report(self):
        ptr_msg = MsgActiveUserReport()
        ptr_msg.set_report_info(
            self.stat_user.show_user_info())
        self.queue.send(self.mgrq, ptr_msg)
        self.stat_user.clear_data()

    def _final(self):
        self._send_report()
        super(ActiveUserCalc, self)._final()
        
class ActiveUserCalcMgr(CalcManager):
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
        debug("ActiveUserCalcMgr::_process_msg() enter")
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgActiveUserReport:
            debug("ActiveUserCalcMgr::_process_msg() got "
                  "report message %s"%msg.get_body())
            ptr_msg = MsgActiveUserReport()
            ptr_msg.cast(msg)
            data = json.loads(ptr_msg.get_report_info())
            for user, play_info in data.items():
                self.stat_user.merge_user_info(user, play_info)

        else:
            super(ActiveUserCalcMgr, self)._process_msg(msg)

    def _process_timer(self, msg):
        #tag = msg.get_tag()
        #if tag == TMTAGS.PRINT_REPORT:
        #    self._print_report()
        #else:
        #    super(ActiveUserCalcMgr, self)._process_timer(msg)
        super(ActiveUserCalcMgr, self)._process_timer(msg)

    def _print_report(self):
        self._user_report_total()
        self._user_report_day()

    def _final(self):
        echo("going to generate final report ...")
        self._print_report()
        echo("report generation completed")
        super(ActiveUserCalcMgr, self)._final()

    def _user_report_total(self):
        models = self.stat_user.gen_stat_users_by_model()
        self.dbsession = self.db.open('active_users_total')
        from common.models_list import models_hash
        data = {"model": "",
                'date': '%s_%s'%(self.config['start'],
                                 self.config['end']),
                'count': 0}
        for model, count in models.items():
            if model in models_hash:
                data['model'] = models_hash[model]
                data['count'] = count
            else:
                #print "%s --> %s"%(model, count)
                data['model'] = model
                data['count'] = count
            self.dbsession.insert(data)
        self.dbsession.commit()
        
        data['model'] = "HISENSE"
        data['count'] = self.stat_user.count_user()
        self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()
        
    def _user_report_day(self):
        models = self.stat_user.gen_stat_users_by_model_per_day()
        from common.models_list import models_hash
        self.dbsession = self.db.open('active_users_day')
        data = {"model": "",
                'date': "",
                'count': 0}
        for m, stat_time in models.items():
            infos = stat_time.show_info()
            model = ""
            if m in models_hash:
                model = models_hash[m]
            else:
                model = m
            data['model'] = model
            for day, count in infos.items():
                data['date'] = day
                data['count'] = count
                self.dbsession.insert(data)
            self.dbsession.commit()

        infos = self.stat_user.gen_stat_users().show_info()
        data['model'] = 'HISENSE'
        for day, count in infos.items():
            data['date'] = day
            data['count'] = count
            self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()

