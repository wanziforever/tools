#!/usr/bin/env python

"""
The script is used to load VOD media infomation to iCNTV audit
system, script will access the detail page from VOD backend
through a public API, and convert it to the format that iCNTV
audit system required, 

ISSUES:
 the following field cannot be get out from detail page view
 is3d, video's pubdate, videos'post_url, video's summary

 note, the definition for videos is not defined for video,
 but for play_ways
 
"""

import os
import time
import datetime
import urllib
import re
import json
import sys
import getopt
import threading
from functools import wraps

FRONTPAGE_API = "http://api.vod.jamdeocloud.com/frontpage/api/master_views"
DETAIL_PAGE_API = "http://api.vod.jamdeocloud.com/medias/api/media/{0}?vender=0"
RELATED_API = "http://api.vod.jamdeocloud.com/recom/api/getRelatedMedia?media={0}&uuid={1}&mac={2}&devid={3}&tz={4}"
guess_your_like="http://api.vod.jamdeocloud.com/recom/api/getGuess?uuid={0}&mac={1}&devid={2}&tz={3}"

current = 0
PROGRESS= ".progress"
ENTRY_LIST_FILE = ""
ENTRY_LIST = []
DEBUG = False
TNUM = 2
get_next_lock = threading.Lock()

def log_err(msg):
    log("ERROR:%s"%msg)

def log(msg):
    if DEBUG:
        print "DEBUG: %s"%(msg)
    else:
        print msg
    
def EXIT(code, msg):
    if code == 0:
        log("SUCCESS: "+ msg)
    else:
        log_err("Exit(%d), "%code + msg)
    exit(code)
    

def timed(f):
    ''' measure a execution time duration for a function, a threshold
    will be used to indicate whether print the alarm for function take
    a long time '''
    threshold = 1
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        result = f(*args, **kwds)
        elapsed = time.time() - start
        if elapsed > threshold:
            print "-%s- %s took %d seconds to finish" % (threading.current_thread(),
                                                         f.__name__, elapsed)
        return result
    return wrapper

no_valid_re = re.compile(r"success")
def valid_url(msg):
    m = no_valid_re.search(msg)
    if m is None:
        return True
    else:
        return False

valid_url_lock = threading.Lock()
valid_url_file = "valid_url"
valid_url_fd = open(valid_url_file, "a")
def record_valid_url(url):
    valid_url_lock.acquire()
    valid_url_fd.write(url+"\n")
    valid_url_fd.flush()
    valid_url_lock.release()
    
def vod_get(url, check_resp=True):
    #log("\nurl:%s"%url)
    resp = urllib.urlopen(url)
    if check_resp is False:
        return {'msg': "check_resp is False"}
    got = resp.read()
    if valid_url(got) is True:
        print "VALID: %s"%url
        record_valid_url(url)
    else:
        print "NO_VALID: %s"%url
    try:
        j = json.loads(got)
    except Exception as e:
        log_err("fail to jsonlize the response (%s):\n%s"%(repr(e), detail))
        EXIT(1, "fail to get detail for entry %s"%entry)
    if DEBUG:
        log(j)
    return j


@timed
def get_detail(entry):
    ''' access the detail page for backend, return jsonlize response'''
    url = DETAIL_PAGE_API.format(entry)
    return vod_get(url, True)

@timed
def get_related(entry):
    url = RELATED_API.format(entry, "1111", "05-16-DC-59-C2-34", "243234dfas45fda", "1242")
    return vod_get(url, False)

uuid = 100
@timed
def get_guess(entry):
    global uuid
    uuid += 1
    url = guess_your_like.format("%s"%uuid, "05-16-DC-59-C2-34", "243234dfas45fda", "1242")
    return vod_get(url, False)

@timed
def get_frontpage():
    url = FRONTPAGE_API
    return vod_get(url, False)

def validate(content):
    ''' validate the response from the VOD backend, currently the ``success``
    field will be taken when there is no data found '''
    if content.has_key('success'):
        if content['success'] is True:
            return (False, "no data")
        else:
            return (False, "fail to get detail page")
    else:
        return (True, "")

def restore_v2():
    global current
    pwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(pwd, PROGRESS)
    if not os.path.exists(path):
        current = -1
        return
    
    with open(PROGRESS, "r") as f:
        content = f.read().strip()
        if len(content) == 0:
            content = "-1"
        current = int(content)

def get_next_v2():
    global current
    if len(ENTRY_LIST) == 0:
        EXIT(1, "no entry found")
    get_next_lock.acquire()
    current += 1
    if current >= len(ENTRY_LIST):
        get_next_lock.release()
        EXIT(0, "get the end")
    ret = ENTRY_LIST[current].strip()
    get_next_lock.release()
    return ret

def write_status_v2():
    pwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(pwd, PROGRESS)
    with open(path, "w") as f:
        f.write("%s"%current)

########################################################
#
# performance call load function
#
########################################################

def call_provision(entry):
    ''' provision one entry '''
    #---------------------------------------------

    content = get_detail(entry)
    #content = get_related(entry)
    #content = get_guess(entry)
    #content = get_frontpage()
    
    #---------------------------------------------
    if DEBUG:
        print content
    return True, ""

def call_perf():
    restore()
    entry = get_next()
    print "----- the next entry is %s -----"%entry
    time.sleep(2)
    while True:
        succ, msg = call_provision(entry)
        #write_status()
        entry = get_next()

def usage():
    print "%s df:"%sys.argv[0]


class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_received = False
    def run(self):
        entry = get_next()
        print "----- the next entry is %s -----"%entry
        time.sleep(1)
        while not self.kill_received:
            succ, msg = call_provision(entry)
            #write_status()
            entry = get_next()
        print "thread end"
            

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "df:")
        for opt, arg in opts:
            if opt == '-d':
                DEBUG = True
            elif opt == '-f':
                ENTRY_LIST_FILE = os.path.join(os.path.dirname(\
                    os.path.abspath(__file__)), arg)
                if not os.path.exists(ENTRY_LIST_FILE):
                    print "%s file not exist"%ENTRY_LIST_FILE
                    exit(1)

                with open(ENTRY_LIST_FILE, "r") as f:
                    ENTRY_LIST = f.readlines()
                restore = restore_v2
                get_next = get_next_v2
                write_status = write_status_v2
            else:
                EXIT(1, "no support for %s"%opt)

    except getopt.GetoptError:
        print "error parsing option"
        exit(1)
            
    restore()

    #for i in xrange(10):
    #    threading.Thread(target = call_perf,  args = (), name = 'thread-' + str(i)).start()

    threads = []
    for i in range(TNUM):
        t = Worker()
        threads.append(t)
        t.start()
        
    
    while len(threads) > 0:
        try:
            #threads = [t.join(1) for t in threads]
            time.sleep(2)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads............."
            for t in threads:
                t.kill_received = True
            time.sleep(4)
            valid_url_fd.close()
            exit(0)
                

