#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# Copyright (c)  2015 Denny Wang (wangliang8@hisense.com)
# License: Hisense Cloud

import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import pycurl
import StringIO
import json
import time

import settings
from alarm import ALARM_LEVEL, alarm
from alarm_definition import *
from datetime import datetime, timedelta
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)

STATIC_FRONTPAGE_THRESHOLD = 2000 # msec
RECOM_FRONTPAGE_THRESHOLD = 2000 # msec
TOTAL_FRONTPAGE_THRESHOLD = 4000 # msec

def get_frontpage_data():
    data = ""
    om_output("going to get frontpage data from url %s"
              %settings.VOD_FRONTPAGE_URL)
    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, settings.VOD_FRONTPAGE_URL)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    try:
        c.perform()
        data = b.getvalue()
        return data
    except Exception, e:
        om_err_output("exception meet when getting frontapge data (%s)"
                      %settings.VOD_FRONTPAGE_URL)
        om_err_output(str(e))
    return None

def get_recom_data():
    data = ""
    url = settings.RE_COLUMN_URL + "?uuid={0}&model_id={1}&re_num={2}".\
          format(settings.uuid, settings.model_id, settings.re_num)
    om_output("going to get recom data from url %s"%url)
    try:
        c = pycurl.Curl()
        b = StringIO.StringIO()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.CONNECTTIMEOUT, 60)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.perform()
        data = b.getvalue()
    except Exception, e:
        om_err_output("exception meet when getting recom data (%s)"%url)
        om_err_output(str(e))
        data = None
    return data

def handle_argv():
    args = sys.argv[1:]
    if '-d' in args:
        settings.debug_mode = True
        args.remove('-d')
    if len(args) == 0:
        om_err_output("handle_args() fail to get vender information")
        exit(0)
    settings.VENDER = args[0].upper()
    if settings.VENDER not in settings.FRONTPAGE.keys():
        om_err_output("not support vender %s"%settings.VENDER)
        exit(0)
    settings.VOD_FRONTPAGE_URL = settings.FRONTPAGE[settings.VENDER]

    if len(args) < 2:
        return

    settings.uuid = int(args[1])
    return

def call_monitor():
    # firstly check the static frontpage data
    start_ts = int(time.time() * 1000)
    data = get_frontpage_data()
    if data is None:
        alarm(ALARM_LEVEL.CRITICAL, ALM_NETWORK_ISSUE, "static frontpage load fail")
        return False
    end_ts = int(time.time() * 1000)
    delta = end_ts - start_ts
    if delta > STATIC_FRONTPAGE_THRESHOLD:
        alarm(ALARM_LEVEL.CRITICAL, ALM_NETWORK_SLOW,
              "static frontpage load consume too much time %s(threshold %s)"
              %(delta, STATIC_FRONTPAGE_THRESHOLD))
    jdata = json.loads(data)
    settings.re_num = int(jdata['re_num'])
    settings.model_id = jdata['model_id']
    # secondly check the recom frontpage data
    start_ts = int(time.time() * 1000)
    data = get_recom_data()
    if data == None:
        alarm(ALARM_LEVEL.CRITICAL, ALM_NETWORK_ISSUE, "recom frontpage load fail")
        return False
    end_ts = int(time.time() * 1000)
    delta = end_ts - start_ts
    if delta > RECOM_FRONTPAGE_THRESHOLD:
        alarm(ALARM_LEVEL.CRITICAL, ALM_NETWORK_SLOW,
              "recom frontpage load consume too much time %s(threshold %s)"
              %(delta, RECOM_FRONTPAGE_THRESHOLD))
    return True

def set_alarm_configration():
    # set the alarm file
    alarm_file = "%s_%s.alm"%(os.path.splitext(sys.argv[0])[0], settings.VENDER)
    os.environ['alarm_file'] = alarm_file
    # if the file already exit, just clear it
    if os.path.exists(alarm_file):
        os.remove(alarm_file)
        
if __name__ == "__main__":
    handle_argv()
    set_alarm_configration()
    while True:
        start_ts = int(time.time() * 1000)
        succ = call_monitor()
        if succ is False:
            continue
        end_ts = int(time.time() * 1000)
        delta = end_ts - start_ts
        if delta > TOTAL_FRONTPAGE_THRESHOLD:
            alarm(ALARM_LEVEL.CRITICAL, ALM_NETWORK_SLOW,
                  "total frontpage load consume too much time %s(threshold %s)"
                  %(delta, TOTAL_FRONTPAGE_THRESHOLD))
        time.sleep(2)
