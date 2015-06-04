#!/usr/bin/env python

import time
import datetime
import multiprocessing


#def msecond_one_day():
#    mseconds_start = \
#         int(time.mktime(time.strptime("2014-5-1", "%Y-%m-%d")) * 1000)
#    mseconds_end = \
#         int(time.mktime(time.strptime("2014-5-2", "%Y-%m-%d")) * 1000)
#    return mseconds_end - mseconds_start

def msecond_one_day():
    return 3600 * 24 * 1000

class StatTime(object):
    def __init__(self, start_day, end_day):
        self.mseconds_start = \
                int(time.mktime(time.strptime(start_day, "%Y-%m-%d")) * 1000)
        self.mseconds_end = \
                int(time.mktime(time.strptime(end_day, "%Y-%m-%d")) * 1000 -1)
        self.delta = self.mseconds_end - self.mseconds_start
        self.num_days = self.delta / msecond_one_day() + 1
        self.days_count = []
        for i in range(self.num_days):
            self.days_count.append(0)
        self.is_empty = True
        self.lock = multiprocessing.Lock()
        self.print_zero_entry = False

    def set_print_zero_entry(self, flag):
        self.print_zero_entry = flag

    def delta(self):
        return self.delta

    def __repr__(self):
        s = "start_ts: %s, end_ts: %s\n"%(str(self.mseconds_start),
                                        str(self.mseconds_end))
        s += "day count array: \n%s"%self.days_count
        return s

    def stat_count(self, ts, count=1):
        ''' add a count to the slot for input ts, and return current count '''
        if ts < self.mseconds_start or ts > self.mseconds_end:
            return
        self.lock.acquire()
        delta_ts = ts - self.mseconds_start
        delta_day = delta_ts / msecond_one_day()
        self.days_count[delta_day] += count
        if self.is_empty is True:
            self.is_empty = False
        self.lock.release()
        return self.days_count[delta_day]

    def get_count_by_idx(self, idx):
        if idx < 0 or idx > self.num_days:
            return -1
        return self.days_count[idx]

    def get_count_by_ts(self, ts):
        if ts < self.mseconds_start or ts > self.mseconds_end:
            return -1
        self.lock.acquire()
        delta_ts = ts - self.mseconds_start
        delta_day = delta_ts / msecond_one_day()
        return self.days_count[delta_day]

    def get_days_count(self):
        return self.days_count

    def clear_count(self):
        self.lock.acquire()
        for i in range(len(self.days_count)):
            self.days_count[i] = 0
        self.is_empty = True
        self.lock.release()
            
    def empty(self):
        return self.is_empty

    def merge(self, other):
        length = 0
        if len(self.days_count) <= len(other):
            length = len(self.days_count)
        else:
            length = len(other)

        for i in range(length):
            self.days_count[i] += other[i]

    def show_info(self):
        #print "StatTime::show_info enter"
        info = "{0}: <{1}>, "
        s = ""
        #print "StatTime::show_info  length of day count is", len(self.days_count)
        start_day = datetime.datetime.fromtimestamp(self.mseconds_start/1000)
        #print "StatTime::show_info start_day", start_day
        for i in range(len(self.days_count)):
            day = start_day + datetime.timedelta(days=i)
            #print "StatTime::show_info current working day", day
            #print info.format(day.strftime("%Y-%m-%d"), self.days_count[i])
            if self.print_zero_entry is False and self.days_count[i] == 0:
                continue
            s += info.format(day.strftime("%Y-%m-%d"), self.days_count[i])
        #print "StatTime::show_info exit"
        return s[:-2]

if __name__ == "__main__":
    t = StateTime("2014-5-1", "2014-6-1")
    print repr(t)

    t.stat_count(1398873600001)

    print repr(t)
