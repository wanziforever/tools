#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Currently the top media reuse the design for play users, and
treat the mediaid as the userid '''

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


import sys
reload(sys)
sys.setdefaultencoding('utf8')

def default_encoder(obj):
    return obj.__json__()

class TopMediasGrabber(GrabberWorker):
    def __init__(self, msgh, mgrq, myname, config):
        GrabberWorker.__init__(self, msgh, mgrq, myname, config)
        self.log_path = '/data/logs/source/'
        self.work_dir = '/data/logs/work/'
        #self.log_path = '/data/testlogs/'
        #self.work_dir = '/data/testlogs/work/'
        self.mediacount = 0

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
                if code != '5010':
                    continue
                
                self._handle_record(record)
                self.current += 1
            fd.close()
            #os.system('cd %s; gzip %s'%(dirname, input_file))
            #print "mediacount is ", self.mediacount

    def _handle_record(self, raw):
        e = gen_entry(raw)
        if e.parse() is False:
            return

        msg = MsgTopMediasCalc()
        #msg.set_userid(e.get_userid())
        msg.set_userid(e.get_mediaid())
        msg.set_timestamp(e.get_ts())
        msg.set_vender(e.get_vender())
        i = self.next_rrobin()
        self.queue.send(self.calc_queues[i], msg)

def call_convert(ts):
    dd = datetime.datetime.fromtimestamp(ts)
    return str(dd)

class TopMediasCalc(CalcWorker):
    def __init__(self, msgh, mgrq, myname, config):
        CalcWorker.__init__(self, msgh, mgrq, myname, config)
        self.report_intvl = 4
        self.report_threshold= 100
        self.report_counter = 0
        self.stat_user = StatUser(self.config['start'], self.config['end'])

    def _process_msg(self, msg):
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgTopMediasCalc:
            calc_msg = MsgTopMediasCalc()
            calc_msg.cast(msg)
            calc_msg.parse()
            ts = calc_msg.get_timestamp()
            user = calc_msg.get_userid()

            ff = open("fff", "a")
            try:
                cts = call_convert(float(ts)/1000)
            except:
                return
            aa = "media(%s), ts(%s)\n"%(user, cts)
            ff.write(aa)
            ff.close()
            
            vender = calc_msg.get_vender()
            if vender in vender_dict:
                vender = vender_dict[vender]
            if ts.find('.') != -1 or ts.isdigit() is False:
                warn("invalid timestamp %s for user %s"%(ts, user))
                return
            self.stat_user.mark(user, ts, vender)
            #print "after mark ", self.stat_user.show_user_info()
            
            if self.report_counter > self.report_threshold:
                self.report_counter = 0
                self._send_report()
            self.current += 1
            self.report_counter += 1
        else:
            super(TopMediasCalc, self)._process_msg(msg)

    def _process_timer(self, msg):
        tag = msg.get_tag()
        if tag == TMTAGS.SEND_REPORT:
            self._send_report()
        else:
            super(TopMediasCalc, self)._process_timer(msg)

    def _send_report(self):
        ptr_msg = MsgTopMediasReport()
        ptr_msg.set_report_info(
            self.stat_user.show_user_info())
        #print "--send_report--", ptr_msg.get_body()
        self.queue.send(self.mgrq, ptr_msg)
        self.stat_user.clear_data()

    def _final(self):
        self._send_report()
        super(TopMediasCalc, self)._final()
        
class TopMediasCalcMgr(CalcManager):
    def __init__(self, msgh, config):
        CalcManager.__init__(self, msgh)
        self.report_fd = None
        self.config = config
        self.stat_user = StatUser(config['start'], config['end'])
        self.rpt_print_intvl = 40
        self.category_count = {1001: 0, # play
                               1002: 0, # zongyi
                               1003: 0, 
                               1004: 0, # movie
                               1005: 0, # catoon
                               1006: 0,
                               1007: 0, # sport
                               1008: 0,
                               1009: 0,
                               1010: 0,
                               1011: 0,
                               1012: 0, # child
                               1013: 0,
                               1014: 0,
                               1015: 0,
                               1016: 0,
                               1017: 0,
                               1100: 0
                               }
        self.country_count = {}

        #self.eh.register_timer(self.rpt_print_intvl * 1000,
        #                       TMTAGS.PRINT_REPORT, True)
        self.db = Mydb()
        self.db.connect('report')

    def set_config(self, config):
        self.config = config

    def _process_msg(self, msg):
        debug("TopMediasCalcMgr::_process_msg() enter")
        msgtype = msg.get_msgtype()
        if msgtype == MsgType.MsgTopMediasReport:
            debug("TopMediasCalcMgr::_process_msg() got "
                  "report message %s"%msg.get_body())
            ptr_msg = MsgTopMediasReport()
            ptr_msg.cast(msg)
            data = json.loads(ptr_msg.get_report_info())
            for user, play_info in data.items():
                self.stat_user.merge_user_info(user, play_info)

        else:
            super(TopMediasCalcMgr, self)._process_msg(msg)

    def _process_timer(self, msg):
        #tag = msg.get_tag()
        #if tag == TMTAGS.PRINT_REPORT:
        #    self._print_report()
        #else:
        #    super(TopMediasCalcMgr, self)._process_timer(msg)
        super(TopMediasCalcMgr, self)._process_timer(msg)

    def _print_report(self):
        self._top_medias()
        self._top_media_type()
        self._top_country()
        self._category_times()

    def _final(self):
        echo("going to generate final report ...")
        self._print_report()
        echo("report generation completed")
        super(TopMediasCalcMgr, self)._final()

    def _count_medias_for_category(self, cid):
        if cid not in self.category_count:
            return
        self.category_count[cid] += 1

    def _count_media_for_country(self, country, count):
        if country in self.country_count:
            self.country_count[country] += count
        else:
            self.country_count[country] = count

    def _top_medias(self):
        top_list = self.stat_user.gen_stat_tops()
        echo("there are totaly %s top medias"%len(top_list))
        self.dbsession = self.db.open('play_top_medias')
        data = {"seq": "",
                'date':'%s_%s'%(self.config['start'],
                                self.config['end']),
                'mediaid': "",
                'media_name':'',
                'count': 0}
        i = 0
        from common.fetch_media_data import VodMedia
        for mediaid, count in top_list:
            data['seq'] = i
            data['mediaid'] = mediaid
            media = VodMedia(mediaid)
            title = media.get_title()
            print "id: %s, cid: %s, title: %s"%\
                  (mediaid, media.get_category_id(), title)
            #print "%s(%s) -- %s"%(title, mediaid, media.get_category_id())
            data['media_name'] = title
            data['count'] = count
            self.dbsession.insert(data)
            i += 1
        self.dbsession.commit()
        self.dbsession.close()
        
        
    def _top_media_type(self):
        from common.media_type import media_types
        from common.fetch_media_data import VodMedia
        self.dbsession = self.db.open('play_top_media_types_times')

        data = {"seq": "",
                'date':'%s_%s'%(self.config['start'],
                                self.config['end']),
                'categoryid': "",
                'category_name':'',
                'count': 0}
        media_type_count = {}
        for mediaid, play_info in self.stat_user.users_info.users.items():
            infos = play_info.count_with_index()
            total = 0
            for index, count in infos.items():
                total += count
            media = VodMedia(mediaid)
            title = media.get_title()
            print "id: %s, cid: %s, title: %s"%\
                  (mediaid, media.get_category_id(), unicode(title, 'utf-8'))
            cid = media.get_category_id()
            if cid is None:
                continue

            country = media.get_country()

            self._count_medias_for_category(int(cid))
            self._count_media_for_country(country, total)
            
            # count the media play times
            if cid in media_type_count:
                media_type_count[cid] += total
            else:
                media_type_count[cid] = total
                
        sorted_types = sorted(media_type_count.items(), key=lambda d: d[1], reverse=True)
        for i in range(len(sorted_types)):
            data['seq'] = i
            category_id = sorted_types[i][0]
            data['categoryid'] = category_id
            if category_id in media_types:
                data['category_name'] = media_types[category_id]
            else:
                data['category_name'] = category_id
            data['count'] = sorted_types[i][1]
            self.dbsession.insert(data)
        self.dbsession.commit()
        self.dbsession.close()

    def _category_times(self):
        print "### most popular categories play info ###"
        from common.media_type import media_types
        for cid, count in self.category_count.items():
            print "%s : %s"%(media_types[cid], count)
        
    def _top_country(self):
        print "### most popular country play info ###"
        for country, count in self.country_count.items():
            print "%s : %s"%(country, count)
