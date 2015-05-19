#!/usr/bin/env python

import pycurl
import StringIO
import json
import time

recom_refresh_url = """http://api.wasuvod.hismarttv.com/recom/api/develop/multirecom?start={start}&rows={rows}&outtime={timeout}"""
start = 0
end = 0 # rows currently represent end
timeout = 60
rows = 20

success_num = 0
exception_num = 0

def set_delta():
    global start, rows, end
    start = end
    end += rows
    
def is_end():
    global success_num, exception_num, end
    if exception_num > 5:
        print "too many exceptions"
        return True
    if end > success_num + exception_num:
        print "end detect for end=%s, success_num=%s,  exception_num=%s"\
              %(end, success_num, exception_num)
        return True
    return False
        
def init():
    global start, end, timeout, success_num, exception_num
    start = 0
    end = 0
    timeout = 60
    success_num = 0
    exception_num = 0

def send(url):
    print "access url %s"%url
    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    start = int(time.time() * 1000)
    c.perform()
    end = int(time.time() * 1000)
    delta = end - start
    print "--------------------perform take %s ms"%delta
    data = b.getvalue()
    end1 = int(time.time() * 1000)
    delta = end1 - end
    print "--------------------getvalue take %s ms"%delta
    return data

def call_trigger():
    global success_num, exception_num
    if start >= end:
        print "start >= end, just return"
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
    data_num = int(j['data_num'])
    delta = end - start
    print "send %s request, %s succeed, exception: %s, total_send=%s, duration=%smsec"\
          %(delta, data_num, exception_num, end, duration)

if __name__ == "__main__":
    init()
    start_ts = int(time.time() * 1000)
    while (True):
        if is_end():
            end_ts = int(time.time() * 1000)
            delta = end_ts - start_ts
            print "reinit and start from the beginning, last execution take %s sec"%(delta/1000)
            init()
            time.sleep(600)
            start_ts = int(time.time() * 1000)
                        
        set_delta()
        #time.sleep(5)
        call_trigger()
