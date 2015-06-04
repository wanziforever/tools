#!/usr/bin/env python

import pycurl
import StringIO
import json
import time

recom_refresh_url = '''http://api.wasuvod.hismarttv.com/recom/api/develop/multirecom?start={start}&rows={rows}&outtime={timeout}'''
start = 0
end = 0 # rows currently represent end
timeout = 100
rows = 40

data_num = 0
success_num = 0
exception_num = 0

retry_sleep = 3

end_retry_count = 8
retry_count = 0

def set_delta():
    global start, rows, end
    start = end
    end += rows
    
def is_end():
    global success_num, exception_num, end, data_num
    global end_retry_count, retry_count
    if exception_num > 5:
        print "too many exceptions"
        return True
    #if end > success_num + exception_num:
    #    print "end detect for end=%s, success_num=%s,  exception_num=%s"\
    #          %(end, success_num, exception_num)
    #    return True
    # need a double confirm way, the first time we notice
    # success_num is 0, we just guess it will be finished
    # if we got next one is still the same, it is just end
    if start != 0 and data_num == 0  and exception_num == 0:
        if retry_count >= end_retry_count:
            return True
    return False
        
def init():
    global start, end, timeout, success_num, exception_num
    start = 0
    end = 0
    timeout = 100
    success_num = 0
    exception_num = 0

def send(url, retry=3):
    global retry_count
    # here retry is for the network level retry
    network_retry_count = 0
    if retry_count > 0:
        print "RETRY access url %s"%url
    else:
        print "access url %s"%url
    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    while network_retry_count < retry:
        try:
            c.perform()
            data = b.getvalue()
            return data
        except Exception,e:
            print "Meet exception when access url %s"%url
            network_retry_count += 1
            time.sleep(1)
            continue
    return None

def need_retry():
    global exception_num, data_num, retry_count
    if data_num == 0 :
        retry_count += 1
        return True
    retry_count = 0
    return False

def call_trigger():
    global success_num, exception_num, data_num, rows
    if start >= end:
        print "start(%s) >= end(%s), just return"%(start, end)
        return
    url = recom_refresh_url.format(
        start=start, rows=end, timeout=timeout)
    start_ts = int(time.time() * 1000)
    data = send(url)
    if len(data) == 0:
        print "err: empty data received"
        exit(0)
    end_ts = int(time.time() * 1000)
    duration = end_ts - start_ts
    try:
        j = json.loads(data)
    except:
        return
    success_num = int(j['success_num'])
    exception_num = int(j['except_num'])
    no_data_num = int(j['no_data_num'])
    data_num = int(j['data_num'])
    delta = end - start
    print "send %s request, %s succeed, exception: %s, no_data: %s, "\
          "total_send=%s, duration=%smsec"\
          %(delta, data_num, exception_num, no_data_num, end, duration)
    if data_num == 0 or exception_num > 0:
        print "erro meet: ", str(j)
    

if __name__ == "__main__":
    init()
    start_ts = int(time.time() * 1000)
    set_delta()
    retry_sleep_time_add = 0
    while (True):
        call_trigger()
        if not need_retry():
            # here the retry means the data returned is 0, need to retry
            # and conform
            set_delta()
            retry_sleep_time_add = 0
        else:
            # retry sleep time need more time very continued retry
            t = retry_sleep + retry_sleep_time_add
            print "sleep %s seconds for retry"%t
            time.sleep(t)
            retry_sleep_time_add += 4
            
        if is_end():
            end_ts = int(time.time() * 1000)
            delta = end_ts - start_ts
            print "--------reinit and start from the beginning, last execution take %s sec-----"%(delta/1000)
            init()
            set_delta()
            #time.sleep(30)
            start_ts = int(time.time() * 1000)
