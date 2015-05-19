#!/usr/bin/env python

import sys
import copy
import time
import datetime
from core.msgh import MsghMgr
from mystat import TopMediasGrabber
from mystat import TopMediasCalc, TopMediasCalcMgr
from common.grabber_manager import GrabberManager
from common.grabber_worker import GrabberWorker

from common.calc_manager import CalcManager
from common.calc_worker import CalcWorker

from common.echo import echo, debug, warn, err

msgh = MsghMgr()
program_start_time = datetime.datetime.now()
program_finish_time = 0
START_DESC = '''
 +-------------------------------------------------------------
   Statistical Analysis for TOP MEDIAS
   Search criteria is DATE From {0} to {1}
   START FROM: {2}
   
 --------------------------------------------------------------+
'''

FINISH_DESC = '''
 +------------------------------------------------------------
   Statistical Analysis for TOP MEDIAS
   Search criteria is DATE From {0} to {1}
   start from: {2},  FINISH AT: {3}
   Duration: {4}
   
 -------------------------------------------------------------+
'''

def usage():
    print "%s <start_day> <end_day>\n" \
          "-- day should be written like 2014-5-1"%sys.argv[0]

def calc_eage_days():
    start = sys.argv[1]
    end = sys.argv[2]

    try:
        time.strptime(start, "%Y-%m-%d")
        time.strptime(end, "%Y-%m-%d")
    except:
        usage()
        exit(0)

    return start, end

def wait_dot(seconds):
    for i in range(seconds):
        time.sleep(1)
        print ".",
        sys.stdout.flush()
    time.sleep(1)
    print

def slice_ts(start_ts, end_ts, num):
        ''' divide the ts into parties,
        return [(start, end), (start, end), ...]'''
        delta = end_ts - start_ts
        avg_delta = delta / num + 1
        ret = []
        s = start_ts
        i = 0
        while s < end_ts:
            e = s + avg_delta
            ret.append([s, e])
            s = e
        return ret

grabber_num = 3
calc_num = 4
def calc():
    start_day, end_day = calc_eage_days()
    print START_DESC.format(start_day, end_day, str(program_start_time)[:19])
    start_ts = int(time.mktime(
            time.strptime(start_day, "%Y-%m-%d")) * 1000)
    end_ts = int(time.mktime(
            time.strptime(end_day, "%Y-%m-%d")) * 1000 -1)
    ts_calc_list = slice_ts(start_ts, end_ts, grabber_num)
    ts_list = copy.deepcopy(ts_calc_list)

    # get some former time and newer time logs
    reserve = 6 # reserve hours former and newer
    first_ts = ts_list[0][0]
    end_ts = ts_list[-1][1]
    first_ts = first_ts - (60 * 60 * reserve) * 1000
    end_ts = end_ts + (60 * 60 * reserve) * 1000
    ts_list[0][0] = first_ts
    ts_list[-1][1] = end_ts

    gmgr = GrabberManager(msgh)
    for i in range(grabber_num):
        name = 'TopMediasGrabber' + str(i)
        config = {'start':ts_calc_list[i][0], 'end':ts_calc_list[i][1],
                  'log_start_ts': ts_list[i][0], 'log_end_ts': ts_list[i][1]}
        gmgr.set_worker(name, TopMediasGrabber, config)

    config = {'start':start_day, 'end':end_day}
    cmgr = TopMediasCalcMgr(msgh, config)
    for i in range(calc_num):
        name = 'TopMediasCalc' + str(i)
        cmgr.set_worker(name, TopMediasCalc, config)

    gmgr.start()
    cmgr.start()

    gmgr.join()
    cmgr.join()
    
    program_finish_time = datetime.datetime.now()
    
    print FINISH_DESC.format(start_day, end_day, str(program_start_time)[:19],
                             str(program_finish_time)[:19],
                             str(program_finish_time - program_start_time)[:19])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(0)
    calc()
