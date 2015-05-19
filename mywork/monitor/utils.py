#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# Copyright (c)  2015 Denny Wang (wangliang8@hisense.com)
# License: Hisense Cloud
'''
this file define some utilities for all the project
'''

import re
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import settings
import pycurl
import StringIO
import jinja2
from datetime import datetime

''' define some log trace functions
for simply implementation, every function will call the log() base
function to complete the print to screen, and some specific thing
to do with each level of functions, all the log will also be saved
to a log stack list, for sending email notification.
'''
def warn(string):
    ''' warn does not require program exit, so just record the
    recent warn mesage '''
    settings.last_warn_stack_msg = settings.show_exam_stack()
    settings.last_warn_msg = string
    log("WARN: " + string)

def log(string):
    settings.log_stack.append(string)
    print string
    
def info(string):
    time = datetime.now()
    log("INFO: %s "%str(time)[:19] + string)

def err(string):
    log("ERR: " + string)

def errtrace(string):
    settings.ERRNO_MSG.append(string)
    err(string)

def debug(string):
    if settings.debug_mode is False:
        return
    print "debug: " + string

def validate_pic(url):
    ''' validate the picture with the given url, firstly check whether it
    is the valid url string, some time the url is not a complete url,
    the program should notice this problem '''
    url = url.strip()
    err_msg = ""
    if len(url.strip()) == 0:
        err_msg = "picture url is empty"
        debug("utils::validate_pic() picture url has invalid length(%s)"%url)
        return False, err_msg
    if len(url) < 5:
        err_msg = "picture url has length less than 5, real(%s)"%url
        debug("utils::validate_pic() picture url has invalid length(%s)"%url)
        return False, err_msg
    if url[0:4] != "http":
        err_msg = "picture url has no http prefix(%s)"%url
        debug("utils::validate_pic() picture url has no http prefix(%s)"%url)
        return False, err_msg
    # try 3 times
    errmsg = ""
    for i in xrange(0, 3):
        debug("utils::validate_pic() access picture %s %sst time"%(url, i+1))
        try:
            c = pycurl.Curl()
            #fp = open("tmppic", "wb")
            b = StringIO.StringIO()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.CONNECTTIMEOUT, 10)
            c.setopt(pycurl.TIMEOUT, 10)
            c.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            c.setopt(pycurl.LOW_SPEED_TIME, 20)
            c.perform()
            #fp.close()
            debug("urils::validate_pic() successfully access the picture")
            return True, ""
        except Exception, e:
            err_msg = str(e)
            debug("urils::validate_pic() failed to load picture for %s"%(i+1))
            continue
    return False, err_msg

def export_poster_list_js():
    ''' export a current all poster list javascript source file, so that
    all the poster file can include it and can have a navigation to all
    current poster '''
    poster_files = []
    re_poster = re.compile(r"poster.*.html")
    for f in os.listdir(settings.WEB_HOME):
        if not re_poster.match(f):
            continue
        poster_files.append(f)

    w = '''\n    l[{0}] = "{1}";'''
    s = ""
    i = 0
    for f in poster_files:
        s += w.format(i, f)
        i += 1
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = "poster_list.tpl"
    template = templateEnv.get_template(template_file)
    output = template.render(content=s)
    fname = os.path.join(settings.WEB_HOME, "poster_list.js")
    info("generating %s file"%fname)
    fd = open(fname, 'w')
    fd.write(output)

def dump_pic(url):
    head, tail = os.path.split(url)
    picname = tail
    path = os.path.join(settings.IMAGES_DIR, picname)
    new_url = os.path.join(settings.IMAGE_URL_BASE, picname)
    if os.path.exists(path) and os.stat(path).st_size != 0:
        return new_url
    try:
        info("dump %s to local"%url)
        fp = open(path, "w")
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.CONNECTTIMEOUT, 20)
        c.setopt(pycurl.WRITEFUNCTION, fp.write)
        c.setopt(pycurl.TIMEOUT, 20)
        c.setopt(pycurl.LOW_SPEED_LIMIT, 1)
        c.setopt(pycurl.LOW_SPEED_TIME, 20)
        c.perform()
        fp.close()
    except Exception,e :
        err("failed to save picture(%s) locally"%url)
        err(str(e))
        return url
    
    return new_url

if __name__ == "__main__":
    export_poster_list_js()
