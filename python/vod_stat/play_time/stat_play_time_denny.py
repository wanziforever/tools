#!/usr/bin/env python

import sys
import time
import datetime
import json
from msgh import MyProcess, MyMessage, MsghMgr
from msgh_def import MsgType
from stat_time import StateTime

from pymongo import MongoClient
from bson.objectid import ObjectId


mongo_host = "127.0.0.1"
mongo_port = 27017

report_file = "stat_report.txt"

source_info_dict = {
    '1001':'SOHU',
    '1002':'IQIYI',
    '1003':'KU6',
    '1004':'CNTV',
    '1005':'LEKAN',
    '1006':'PPTV',
    '1007':'YOUKU',
    '1008':'VOOLE',
    '1009':'LETV',
    '1011':'TENCENT',
    '1012':'IFENG',
    '1013':'MANGGUO',
    '1014':'RAINBOW',
    '1021':'VTX'
    }

#---- code to calc days -----
def mkDateTime(dateString,strFormat="%Y-%m-%d"):
    # Expects "YYYY-MM-DD" string
    # returns a datetime object
    eSeconds = time.mktime(time.strptime(dateString,strFormat))
    return datetime.datetime.fromtimestamp(eSeconds)

def formatDate(dtDateTime,strFormat="%Y-%m-%d"):
    # format a datetime object as YYYY-MM-DD string and return
    return dtDateTime.strftime(strFormat)

def mkFirstOfMonth2(dtDateTime):
    #what is the first day of the current month
    ddays = int(dtDateTime.strftime("%d"))-1 #days to subtract to get to the 1st
    delta = datetime.timedelta(days= ddays)  #create a delta datetime object
    return dtDateTime - delta                #Subtract delta and return

def mkFirstOfMonth(dtDateTime):
    #what is the first day of the current month
    #format the year and month + 01 for the current datetime, then form it back
    #into a datetime object
    return mkDateTime(formatDate(dtDateTime,"%Y-%m-01"))

def mkLastOfMonth(dtDateTime):
    dYear = dtDateTime.strftime("%Y")        #get the year
    dMonth = str(int(dtDateTime.strftime("%m"))%12+1)#get next month, watch rollover
    dDay = "1"                               #first day of next month
    nextMonth = mkDateTime("%s-%s-%s"%(dYear,dMonth,dDay))#make a datetime obj for 1st of next month
    delta = datetime.timedelta(seconds=1)    #create a delta of 1 second
    return nextMonth - delta                 #subtract from nextMonth and return

#---- end of code to calc days

class MsgPlayTimeProcessStart(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, MsgType.MsgPlayTimeProcessStart)
        self.count = 0
        self.queue_names = []

    def set_count(self, count):
        self.count = count

    def addQueue(self, qname):
        self.queue_names.append(qname)

    def getQueues(self):
        return self.queue_names

    def build_msg(self):
        self.body = "::".join(self.queue_names)

    def extract_msg(self):
        self.queue_names = self.body.split("::")

class MsgPlayTimeCalc(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, MsgType.MsgPlayTimeCalc)
        self.user_id = ""
        self.ts = ""
        self.vender = ""

    def set_userid(self, userid):
        self.user_id = userid

    def set_timestamp(self, ts):
        self.ts = ts

    def set_vender(self, vender):
        self.vender = vender

    def get_userid(self):
        return self.user_id

    def get_timestamp(self):
        return self.ts

    def get_vender(self):
        return self.vender

    def build_msg(self):
        self.body = "{0}::{1}::{2}".format(self.user_id,
                                           self.ts,
                                           self.vender)
    def extract_msg(self):
        self.user_id, self.ts, self.vender = self.body.split("::")

class PlayerStartupGrabber(MyProcess):
    def __init__(self, msgh_mgr, qname):
        MyProcess.__init__(self, msgh_mgr, qname)
        self.count = 0
        self.current = 0
        self.mongocli = MongoClient(mongo_host, mongo_port)
        self.logdb = self.mongocli.vodlog
        self.player_startup = self.logdb.player_startup
        self.calc_queue_names = []
        self.calc_queues = []
        self.current_q_index = 0
        self.start_pos = ""
        self.end_pos = ""

    def set_calc_queues(self, queue_names):
        self.calc_queue_names = queue_names
        #print "PlayerStartupGrabber get %s calc queues"%\
        #      len(self.calc_queue_names), self.calc_queue_names
        for name in self.calc_queue_names:
            peerqid = self.msgh_mgr.findQueue(name)
            if peerqid == -1:
                print "cannot find queue name with %s"%(name)
                return
            self.calc_queues.append(self.msgh_mgr.getQueue(peerqid))

    def set_start(self, start):
        self.start_pos = str(start)

    def set_end(self, end):
        self.end_pos = str(end)

    def _get_userid(self, doc):
        if 'deviceId' in doc:
            return doc['deviceId']
        else:
            return None

    def _get_vender(self, doc):
        if 'sourceId' in doc:
            return doc['sourceId']
        else:
            return None

    def _get_ts(self, doc):
        if 'ts' in doc:
            return doc['ts']
        else:
            return None

    def _process(self):
        print "process [%s] going to find records betwen %s and %s"%\
              (self.pid, self.start_pos, self.end_pos)
        cursor = self.player_startup.find(
            {'ts': {'$gt': self.start_pos, '$lte': self.end_pos}})
        self.count = cursor.count()
        print "process [%s] %s record has been found"%(self.pid, self.count)
        for record in cursor:
            self._handle_record(record)
        print "DataProducer process [%s] exit"%self.pid

    def _handle_record(self, doc):
        userid, vender, ts = \
                self._get_userid(doc), self._get_vender(doc), self._get_ts(doc)
        msg = MsgPlayTimeCalc()
        msg.set_userid(userid)
        msg.set_timestamp(ts)
        msg.set_vender(vender)
        msg.build_msg()
        self.queue.send(self.calc_queues[self.current_q_index], msg)
        if self.current_q_index + 1 >= len(self.calc_queues):
            self.current_q_index = 0
        else:
            self.current_q_index += 1
        #time.sleep(2)
        
class PlayerStartupGrabberMgr(MyProcess):
    def __init__(self, msgh_mgr):
        MyProcess.__init__(self, msgh_mgr, "PlayerStartupGrabberMgr")
        self.process_num = 1
        self.start_day = ""
        self.end_day = ""

    def set_start(self, day):
        self.start_day = day

    def set_end(self, day):
        self.end_day

    def _process(self):
        # calc the first ts and last ts for 9th month
        #year, month, day = '2014', '9', '2'
        #d = mkDateTime("%s-%s-%s"%(year, month, day))
        #start_ts = int(time.mktime(mkFirstOfMonth(d).timetuple()) * 1000)
        #end_ts = int(time.mktime(mkLastOfMonth(d).timetuple()) * 1000 + 999)

        start_ts = \
            int(time.mktime(time.strptime(start_day, "%Y-%m-%d")) * 1000)
        end_ts = \
            int(time.mktime(time.strptime(end_day, "%Y-%m-%d")) * 1000 -1)

        # wait for calc process ready and get the calc process queues
        calc_queue_names = []
        while True:
            msg = self.queue.receive()
            msg_type = msg.get_header().get_type()
            if msg_type == MsgType.MsgPlayTimeProcessStart:
                print "PlayerStartupGrabberMgr::Notice the MsgPlayTimeProcessStart message"
                ptps_msg = MsgPlayTimeProcessStart()
                ptps_msg.cast(msg)
                ptps_msg.extract_msg()
                calc_queue_names = ptps_msg.getQueues()
                print "PlayerStartupGrabberMgr::total %s calc queues found"%\
                      len(calc_queue_names)
                #print calc_queue_names
                break
            
        for i in range(self.process_num):
            psg = PlayerStartupGrabber(self.msgh_mgr, "PlayerStartupGrabber"+str(i))
            psg.set_start(start_ts)
            psg.set_end(end_ts)
            psg.set_calc_queues(calc_queue_names)
            psg.start()

        while True:
            time.sleep(5)

class MsgPlayTimeReport(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, MsgType.MsgPlayTimeReport)

    def setReportInfo(self, data):
        self.body = json.dumps(data)

    def getReportInfo(self):
        try:
            return json.loads(self.body)
        except:
            return None


class PlayTimeCollector(object):
    def __init__(self, vender, start_day, end_day):
        self.vender = vender
        self.stat_time = StateTime(start_day, end_day)

    def get_vender(self):
        return self.vender

    def __repr__(self):
        s = "vender: %s, info: %s"%(self.vender, repr(self.stat_time))
        return s

class PlayTimeCalc(MyProcess):
    def __init__(self, msgh_mgr, calc_mgr_queue, qname):
        MyProcess.__init__(self, msgh_mgr, qname)
        self.count = 0
        self.interval_send_report = 5 #seconds
        self.send_report_ts = 0
        self.calc_mgr_queue = calc_mgr_queue
        self.play_time_collectors = {}
        

        self.start_day = ""
        self.end_day = ""

    def set_start(self, start):
        self.start_day = start

    def set_end(self, end):
        self.end_day = end

    def show_info(self):
        s = ""
        for k, collector in self.play_time_collectors.items():
            s += repr(collector) + "\n"
        return s

    def _process(self):
        for i, k in source_info_dict.items():
            self.play_time_collectors[k] = \
                      PlayTimeCollector(k, self.start_day, self.end_day)
        self.send_report_ts = time.time()
        while True:
            msg = self.queue.receive()
            #print "PlayTimeCalc::process receive msg ", msg.get_body()
            calc_msg = MsgPlayTimeCalc()
            calc_msg.cast(msg)
            calc_msg.extract_msg()
            ts = calc_msg.get_timestamp()
            vender = calc_msg.get_vender()
            if vender in source_info_dict:
                vender = source_info_dict[vender]
            if not vender in self.play_time_collectors:
                continue
            collector = self.play_time_collectors[vender]
            collector.stat_time.stat_count(int(ts))

            now = time.time()
            delta = now - self.send_report_ts
            if delta > self.interval_send_report:
                self.send_report()
                self.send_report_ts = time.time()
                
    def send_report(self):
        for vender, collector in self.play_time_collectors.items():
            if collector.stat_time.empty():
                continue
            ptr_msg = MsgPlayTimeReport()
            data = {collector.get_vender(): collector.stat_time.get_days_count()}
            ptr_msg.setReportInfo(data)
            self.queue.send(self.calc_mgr_queue, ptr_msg)
            collector.stat_time.clear_count()
            
        
class PlayTimeCalcMgr(MyProcess):
    def __init__(self, msgh_mgr):
        MyProcess.__init__(self, msgh_mgr, "PlayTimeCalcMgr")
        self.process_num = 1
        self.play_time_collectors = {}
        self.count = 0
        self.rpt_fd = None
        self.start_day = ""
        self.end_day = ""

    def set_start(self, start):
        self.start_day = start

    def set_end(self, end):
        self.end_day = end

    def _process(self):
        for i, k in source_info_dict.items():
            self.play_time_collectors[k] = \
                      PlayTimeCollector(k, self.start_day, self.end_day)
            
        ptps_msg = MsgPlayTimeProcessStart()
        for i in range(self.process_num):
            qname = "PlayTimeCalc"+ str(i)
            ptc = PlayTimeCalc(self.msgh_mgr, self.queue, qname)
            ptc.set_start(self.start_day)
            ptc.set_end(self.end_day)
            ptc.start()
            ptps_msg.addQueue(qname)
            
        qid = self.msgh_mgr.findQueue("PlayerStartupGrabberMgr")
        psgr_mgr_queue = self.msgh_mgr.getQueue(qid)
        ptps_msg.build_msg()
        #print "PlayTimeCalcMgr going to send PlayerStartupGrabberMgr"
        self.queue.send(psgr_mgr_queue, ptps_msg)

        while True:
            #print "PlayTimeCalcMgr receive queue message for queue", self.queue.name.value
            msg = self.queue.receive()
            if msg is not None:
                self._process_msg(msg)

    def _process_msg(self, msg):
        msg_type = msg.get_header().get_type()
        #print "PlayTimeCalcMgr::_process_msg enter with", msg_type
        if msg_type == MsgType.MsgPlayTimeReport:
            self._process_report_msg(msg)
        elif msg_type == MsgType.MsgPrintReport:
            self._print_report()
        else:
            print "PlayTimeCalcMgr no support message received ", msg_type

        #print "PlayTimeCalcMgr::_process_msg exit"
        

    def _process_report_msg(self, msg):
        #print "PlayTimeCalcMgr::_process_report_msg enter"
        ptr_msg = MsgPlayTimeReport()
        ptr_msg.cast(msg)
        data = ptr_msg.getReportInfo()
        for vender, counts in data.items():
            self.play_time_collectors[vender].stat_time.merge(counts)
        #print "PlayTimeCalcMgr::_process_report_msg exit "

    def _print_report(self):
        #print "PlayTimeCalcMgr::_print_report enter"
        if self.rpt_fd is None:
            self.rpt_fd = open(report_file, "w")

        w = "\n+---------- %s --------------+\n"%(datetime.datetime.now())
        for vender, collector in self.play_time_collectors.items():
            collector_info = collector.stat_time.show_info()
            if len(collector_info.strip()) == 0:
                continue
            w += "{0}-> {1}\n".format(vender, collector_info)
        self.rpt_fd.write(w)
        self.rpt_fd.flush()

        #print "PlayTimeCalcMgr::_print_report exit"
            
class MsgPrintReport(MyMessage):
    def __init__(self):
        MyMessage.__init__(self, MsgType.MsgPrintReport)
        self.body = "MsgPrintReport message"
        

DESC = '''
+--------------------------------------------
 Statistical Analysis From {0} to {1}
--------------------------------------------+
'''
def calc():
    print DESC.format(start_day, end_day)
    msgh_mgr = MsghMgr()
    ptcmgr = PlayTimeCalcMgr(msgh_mgr)
    psgmgr = PlayerStartupGrabberMgr(msgh_mgr)

    psgmgr.set_start(start_day)
    psgmgr.set_end(end_day)
    
    ptcmgr.set_start(start_day)
    ptcmgr.set_end(end_day)
    
    ptcmgr.start()
    psgmgr.start()

    while True:
        #print "+---------------- QUEUE STATUS --------------------------------"
        #msgh_mgr.show_all_info()
        #print "---------------------------------------------------------------+"
        #print
        pr_msg = MsgPrintReport()
        qid = msgh_mgr.findQueue("PlayTimeCalcMgr")
        calc_mgr_queue = msgh_mgr.getQueue(qid)
        # just a workaround for calc queue send message to itself
        calc_mgr_queue.send(calc_mgr_queue, pr_msg)
        time.sleep(10)


def usage():
    print "%s <start_day> <end_day>\n" \
          "-- day should be written like 2014-5-1"%sys.argv[0]

start_day = ""
end_day = ""
def calc_eage_days():
    global start_day, end_day
    start_day = sys.argv[1]
    end_day = sys.argv[2]

    try:
        time.strptime(start_day, "%Y-%m-%d")
        time.strptime(end_day, "%Y-%m-%d")
    except:
        usage()
        exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(0)
    calc_eage_days()
    calc()
    
