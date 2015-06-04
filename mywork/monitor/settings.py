#!/usr/bin/env python

import re
import os
import jinja2


FRONTPAGE = {
    'CNTV': 'http://api.vod.jamdeocloud.com/frontpage/api/master_views',
    'WASU': 'http://api.wasuvod.hismarttv.com/frontpage/api/master_views',
    'WASU3_0': 'http://api.wasuvod.hismarttv.com/frontpage/api/master_views3_0',
    'WASU3_1': 'http://api.wasuvod.hismarttv.com/frontpage/api/master_views3_1',
    'WASU3_2': 'http://api.wasuvod.hismarttv.com/frontpage/api/master_views3_2',
    'WASU3_3': 'http://api.wasuvod.hismarttv.com/frontpage/api/master_views3_3',
    'EDU': 'http://api.edu.hismarttv.com/frontpage/api/master_views'
    }
VOD_FRONTPAGE_URL = ""
VENDER = ""
RE_COLUMN_URL = "http://api.wasuvod.hismarttv.com/frontpage/api/recom_columns"
WEB_HOME = "/home/denny/web/"
POSTER_HOME = os.path.join(WEB_HOME, 'poster')

IMAGES_DIR = os.path.join(WEB_HOME, "images")

IMAGE_URL_BASE = "http://42.96.137.19/images/"
HISTORY_URL = "http://42.96.137.19/sim/play?user_id={0}&media_id={1}&video_id={2}"

uuid = 1234
model_id = 0
re_num = 8

override = True

master_views = []

last_warn_stack_msg = ""
last_warn_msg = ""

examine_stack = []

ERRNO_MSG = []

log_stack= []

debug_mode = False
#debug_mode = True

alarm_server_port = 7777
alarm_server_host = '0.0.0.0'

def exam_stack_push(obj):
    examine_stack.append(obj)

def exam_stack_pop():
    f = examine_stack.pop()
    
def show_exam_stack():
    s = ""
    if len(examine_stack) == 0:
        return ""
    for stack in examine_stack:
         s += stack._short() + "\n"
    return s[:-1]

def show_current_err_msg():
    if len(ERRNO_MSG) == 0:
        return ""
    return "last error msg: " + ERRNO_MSG[-1]

def set_module_name(module_name):
    os.environ['module_name'] = module_name

def set_file_prefix(prefix):
    os.environ['file_prefix'] = prefix
