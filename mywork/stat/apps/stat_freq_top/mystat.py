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

api = 0
dbname_dict = {
    CallAPI().FRONTPAGE: "frontpage2",
    CallAPI().CATEGORY: "category",
    CallAPI().MEDIA_DETAIL: "media_detail",
    CallAPI().TOP_SEARCH: "top_search",
    CallAPI().ALL_WATCHING: "all_watching",
    CallAPI().NEW7DAYS: "new7days",
    CallAPI().HOT_LIST: "host_list",
    CallAPI().TOPIC: "topic_detail",
    CallAPI().TOPIC_LIST: "topic_list",
    CallAPI().RELATED_MEDIAS: "related_medias",
    CallAPI().SEARCH_RESULT: "search_result",
    CallAPI().HISTORY: "history"
    }

def determine_api(type_str):
    global api
    for i, tstr in dbname_dict.items():
        if tstr == type_str:
            api = i
            return True
    return False

def default_encoder(obj):
    return obj.__json__()

class AccessFreqNginxGrabber(GrabberWorker):
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
                print f, date, " wrong date"
                continue
            if ts >= spos and ts < epos:
                nginx_files.append(f)
            #else:
            #    print "%s with date %d not in range (%d, %d)"%(f, ts, spos, epos)
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
        if e.get_apicode() != api:
            return

        msg = MsgAccessFreqCalc()
        msg.set_api(api)
        msg.set_timestamp(e.get_ts())
        i = self.next_rrobin()
        self.queue.send(self.calc_queues[i], msg)

class AccessFreqCalc(CalcWorker):
    def __init__(self, msgh, mgrq, myname, config):
        CalcWorker.__init__(self, msgh, mgrq, myname, config)
        self.report_intvl = 10
        self.eh.register_timer(self.report_intvl * 1000,
                               TMTAGS.SEND_REPORT, True)
        self.data = {}

    def mark(self, timestamp):
        if timestamp not in self.data:
            self.data[timestamp] = 1
        else:
            self.data[timestamp] += 1

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgAccessFreqCalc:
            calc_msg = MsgAccessFreqCalc()
            calc_msg.cast(msg)
            calc_msg.parse()
            ts = calc_msg.get_timestamp()
            api = calc_msg.get_api()
            self.mark(ts)
            self.current += 1
        else:
            super(AccessFreqCalc, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.SEND_REPORT:
            self._send_report()
        else:
            super(AccessFreqCalc, self)._process_timer(msg)

    def _send_report(self):
        ptr_msg = MsgAccessFreqReport()
        bulk_num = 500
        c = 0
        for ts, count in self.data.items():
            ptr_msg.add_freq_info(ts, count)
            c += 1
            if c >= bulk_num:
                self.queue.send(self.mgrq, ptr_msg)
                c = 0
                ptr_msg.reset()

    def _final(self):
        self._send_report()
        super(AccessFreqCalc, self)._final()
        
class AccessFreqCalcMgr(CalcManager):
    def __init__(self, msgh, config):
        CalcManager.__init__(self, msgh)
        self.report_fd = None
        self.collectors = {}
        self.config = config
        self.db = Mydb()
        self.db.connect('report')
        dbname = "freq_trends_" + dbname_dict[api]
        self.dbsession = self.db.open(dbname)
        self.data = {}
        self.trends_data = {}
        self.top_data = {}

    def set_config(self, config):
        self.config = config

    def mark(self, ts, count):
        # convert to seconds from mseconds
        ts = str(int(ts) / 1000)
        if ts not in self.data:
            self.data[ts] = count
        else:
            self.data[ts] += count
        
        h = int(ts) / 3600000
        if int(ts) % 3600000 == 0:
            self.trends_data[ts] = 

    def _process_msg(self, msg):
        debug("AccessFreqCalcMgr::_process_msg() enter")
        msgtype = msg.get_msgtype()
        #print "--------------process msg", datetime.datetime.now()
        if msgtype == MsgType.MsgAccessFreqReport:
            debug("AccessFreqCalcMgr::_process_msg() got "
                  "report message %s"%msg.get_body())
            ptr_msg = MsgAccessFreqReport()
            ptr_msg.cast(msg)
            ptr_msg.parse()
            #print "------------", ptr_msg.body
            info = ptr_msg.get_freq_info()
            for ts, count in info:
                self.mark(ts, int(count))
        else:
            super(AccessFreqCalcMgr, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.DB_COMMIT:
            #self.dbsession.commit()
            pass
        else:
            super(AccessFreqCalcMgr, self)._process_timer(msg)

    def _print_report(self):
        print "going to generate report file"
        d = {'timestamp': "",
             'count': ''}
        mmax = 0
        mmax_ts = ''
        for ts, count in self.data.items():
            d['timestamp'] = ts
            d['count'] = count
            if count > mmax:
                mmax = count
                mmax_ts = ts
            self.dbsession.insert(d)
        self.dbsession.commit()
        echo("report generation completed, max value is %d, related ts is %s"\
             %(mmax, mmax_ts))

    def _final(self):
        self._print_report()
        self.dbsession.close()
        super(AccessFreqCalcMgr, self)._final()
