#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# Copyright (c)  2015 Denny Wang (wangliang8@hisense.com)
# License: Hisense Cloud

'''
This program are subject to monitor the healthy of hisense vod product,
it mainly focus on the frontpage view data checking, and some frequently
used item data checking, error will be recorded and send email of the
notification, supporting the cntv and wasu site, use 'cntv' or 'wasu' as
the arguemtn to complete the monitor of a site.
'''

import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import sys
import pycurl
import StringIO
import json
import importlib
import settings
from utils import (
    warn,
    info,
    err,
    errtrace,
    debug,
    validate_pic
    )
from alarm import ALARM_LEVEL, alarm
from alarm_definition import *
from datetime import datetime, timedelta
from api_module import ErrCode
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)
import api_module

class Tile(object):
    def __init__(self, id):
        self.index = id
        self.size = []
        self.facets = []

    def __repr__(self):
        s =  "++<Tile> index: {0}, size: ({1}, {2})\n"\
            .format(self.index, self.size[0], self.size[1])
        for f in self.facets:
            s += repr(f) + "\n"
        return s[:-1]

    def _short(self):
        s =  "++<Tile> index: {0}, size: ({1}, {2})"\
            .format(self.index, self.size[0], self.size[1])
        return s

    def self_verify_basic(self):
        """ quickly verify the basic information, return False if found
        any problem """
        om_output("Basic verify the tile %s"%self._short())
        settings.exam_stack_push(self)
        for f in self.facets:
            if not f.self_verify_basic():
                om_err_output("fail to verify %s"%self._short())
                settings.exam_stack_pop()
                # note currently there is only on facet in one tile
                # and we can return when we found an error,
                # if you want to check all the facet, and return together
                # just do not return here
                return False
        settings.exam_stack_pop()
        return True

    def self_verify(self):
        om_output("verifying the tile %s"%self._short())
        settings.exam_stack_push(self)
        for f in self.facets:
            if not f.self_verify():
                om_err_output("fail to verify %s"%self._short())
                return False
        settings.exam_stack_pop()
        return True

class Facet(object):
    def __init__(self, typecode, title):
        self.title = title
        self.typecode = typecode
        self.id = 0
        self.pic = ""

    def __repr__(self):
        s = "++++<Facet> title:{0}, typecode={1}, id={2}, pic={3}"\
            .format(self.title.encode('utf-8'), self.typecode, self.id,
                    self.pic)
        return s
    def _short(self):
        s = "++++<Facet> title:{0}, typecode={1}, id={2}, pic={3}"\
            .format(self.title.encode('utf-8'), self.typecode, self.id,
                    self.pic)
        return s

    def self_verify_basic(self):
        om_output("Basic verify the Facet %s"%self._short())
        settings.exam_stack_push(self)
        if not self.pic_verify():
            settings.exam_stack_pop()
            return False
        api = api_module.api_mapping[self.typecode]
        if self.typecode not in api_module.module_mapping:
            om_err_output("Facet::self_verify_basic() no api module defined for "
                          "typecode %s"%self.typecode)
            settings.exam_stack_pop()
            #return False
            # currently the not support api module need not return fail
            return True
        # get class type related to the typecode
        cl = api_module.module_mapping[self.typecode]
        m = cl(self.id)
        if not m.valid():
            om_err_output("apimodule is not valid for typecode %s"%self.typecode)
            settings.exam_stack_pop()
            return False
        if not m.verify_basic():
            for ecode, emsgs in m.last_err.items():
                om_err_output("fail to basic verify %s"%(self._short()))
                alarm_msg = ""
                for m in emsgs:
                    om_err_output("meet error %s, %s"%(ecode, m))
                    alarm_msg += m + "\n"
                alm = None
                # check every error code for the api module, and send related
                # alarm according to the severity level
                alarm_msg += "\nlocation:\n%s"%settings.show_exam_stack()
                if ecode == ErrCode.RESOURCE_CANT_ACCESS:
                    alarm(ALARM_LEVEL.CRITICAL, ALM_NETWORK_ISSUE, alarm_msg)
                elif ecode == ErrCode.RESOURCE_OFFLINE:
                    alarm(ALARM_LEVEL.CRITICAL, ALM_MEDIA_OFFLINE, alarm_msg)
                elif ecode == ErrCode.DATA_INVALID:
                    alarm(ALARM_LEVEL.HIGH, ALM_MEDIA_DATA_INVALID, alarm_msg)
                elif ecode == ErrCode.BAD_LIST_VIEW_MEDIA or \
                         ecode == ErrCode.BAD_LIST_VIEW_IMAGE:
                    alarm(ALARM_LEVEL.HIGH, ALM_CATEGORY_HAS_BAD_MEDIAS, alarm_msg)
                else:
                    alarm(ALARM_LEVEL.NORMAL, ALM_BASIC, alarm_msg)
                    
            settings.exam_stack_pop()
            return False
        settings.exam_stack_pop()
        return True
    
    def self_verify(self):
        om_output("verifying the Facet %s"%self._short())
        settings.exam_stack_push(self)
        if not self.pic_verify():
            return False
        api = api_module.api_mapping[self.typecode]
        if self.typecode not in api_module.module_mapping:
            om_err_output("Facet::self_verify() no api module defined for typecode %s"%
                          self.typecode)
            return False
        
        cl = api_module.module_mapping[self.typecode]
        m = cl(self.id)
        if not m.valid():
            om_err_output("apimodule is not valid for typecode %s"%self.typecode)
            return False
        if not m.verify():
            om_err_output("fail to verify %s"%(self._short()))
            return False
        settings.exam_stack_pop()
        return True

    def pic_verify(self):
        succ, msg = validate_pic(self.pic)
        if succ is False:
            om_err_output("Facet::pic_verify() fail to valid pic, %s"%msg)
            return False
        return True

class Column(object):
    def __init__(self, name, columnid):
        self.name = name
        self.columnid = columnid
        self.tiles = []
        self.from_re = False

    def __repr__(self):
        s = "<View> name: {0}, columnid: {1}\n"\
            .format(self.name.encode('utf-8'), self.columnid)
        for t in self.tiles:
            s += repr(t) + "\n"
        return s

    def _short(self):
        s = "<View> name: {0}, columnid: {1}"\
            .format(self.name.encode('utf-8'), self.columnid)
        return s

    def self_verify_basic(self):
        om_output("Basic verify view name %s"%self.name)
        settings.exam_stack_push(self)
        has_false = False
        for t in self.tiles:
            if not t.self_verify_basic():
                om_err_output("fail to basic verify %s"%self._short())
                has_false = True
                #return False
        settings.exam_stack_pop()
        om_output("complete basic verified view %s"%self.name)
        
        return not has_false

    def self_verify(self):
        om_output("verifying the view %s"%self.name)
        settings.exam_stack_push(self)
        for t in self.tiles:
            if not t.self_verify():
                om_err_output("fail to verify %s"%self._short())
                #return False
        settings.exam_stack_pop()
        om_output("complete verifying view %s"%self.name)
        return True
        
def show_all_apis():
    for code, apiobj in settings.api_mapping.items():
        print repr(apiobj)
    
def get_frontpage_data():
    data = ""
    om_output("going to get frontpage data from url %s"%settings.VOD_FRONTPAGE_URL)
    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, settings.VOD_FRONTPAGE_URL)
    c.setopt(pycurl.CONNECTTIMEOUT, 5)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    retry = 3
    retry_count = 0
    while retry_count < retry:
        try:
            c.perform()
            data = b.getvalue()
            return data
        except Exception, e:
            om_err_output("exception meet when getting frontapge data (%s)"%
                          settings.VOD_FRONTPAGE_URL)
            om_err_output(str(e))
            retry_count += 1
            continue
    return None

def refresh_recom_data(user, cnum):
    import importlib
    try:
        m = importlib.import_module("production")
        fresh_func = getattr(m, "recom_refresh")
        fresh_func(user, cnum)
    except Exception, e:
        om_output("launcher_monitor3::refresh_recom_data() fail to refresh"
            " recom data, err(%s)"%str(e))
        return False
    return True
    
def get_recom_data():
    refresh_recom_data(settings.uuid, settings.re_num)
    data = ""
    url = settings.RE_COLUMN_URL + "?uuid={0}&model_id={1}&re_num={2}".\
          format(settings.uuid, settings.model_id, settings.re_num)
    om_output("going to get recom data from url %s"%url)
    try:
        c = pycurl.Curl()
        b = StringIO.StringIO()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.CONNECTTIMEOUT, 5)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.perform()
        data = b.getvalue()
    except Exception, e:
        om_err_output("exception meet when getting recom data (%s)"%url)
        om_err_output(str(e))
        data = None
    return data

def parse_api_mapping(data):
    for code in data.keys():
        api = api_module.API(code)
        api.set_url(data[code]['api'])
        api.set_params(data[code]['params'])

def parse_column(data):
    if not isinstance(data, dict):
        om_err_ouptut("navigation data is not a dict type, exit now")
        exit(-1)
        
    v = Column(data['title'], data['navigationId'])
    if 'tiles' not in data:
        om_err_output("parse_navigation()::no tiles in view data")
        exit(-1)
    for t in data['tiles']:
        tile = parse_tile(t)
        if tile is None:
            om_err_output("parse_view() fail to parse view %s"%data['title'])
            return None
        v.tiles.append(parse_tile(t))
    return v
        
def parse_tile(data):
    default_tile_heigth = 300
    if not isinstance(data, dict):
        om_err_output("parse_tile()::tile data is not a dict type, exit now")
        exit(-1)
        
    t = Tile(data['index'])
    t.size = [default_tile_heigth, int(data['width'])]

    if 'facets' not in data:
        om_err_output("parse_tile()::no facets in tile data")
        exit(-1)

    for f in data['facets']:
        facet = parse_facet(f)
        if facet is None:
            return None
        t.facets.append(facet)
    return t
        
def parse_facet(data):
    if not isinstance(data, dict):
        om_err_output("parse_facet()::facet data is not a dict type, exit now")
        om_err_output(str(data))
        exit(-1)
    f = Facet(str(data['typeCode']), data['title'])
    f.id = data['id']
    if len(data['backgroundImages']) == 0:
        om_err_output("parse_facet() fail to parse facet %s due to no "
                 "backgroudImages found"%data['title'])
        return None
    f.pic = data['backgroundImages'][0]['url']
    return f

def show_all_views():
    for view in settings.master_views:
        print repr(view)

def examine():
    # quickly verify the basic data of the service, and return fail
    # as quickly as possible, just return after all the basic data
    # checking.
    meet_error = False
    om_output("firstly start to verify the basic service data, and try "
              "to return quickly if some basic error found")
    for view in settings.master_views:
        if not view.self_verify_basic():
            meet_error = True
    if meet_error:
        om_err_output("Basic verification fail, just stop not going detail "
                      "data verification")
        return False
    # for detail verification, just return false after all data checking
    # finished, and save all the errors together
    om_output("start to verify the detail service data")
    for view in settings.master_views:
        view.self_verify()
    return True

def data_initialize():
    frontpage_data = get_frontpage_data()
    if frontpage_data is None or len(frontpage_data) == 0:
        om_err_output("frontpage data is not complete, exit now")
        exit(-1)
    try:
        frontj = json.loads(frontpage_data)
    except:
        om_err_output("frontpage data can not be jsonlized, exit now")
        exit(-1)

    if 're_num' not in frontj:
        om_err_output("no re_num inforamtion in frontpage data, use default %s"%settings.re_num)
    else:
        settings.re_num = frontj['re_num']

    if 'model_id' not in frontj:
        om_err_output("model_id information in frontpage data, use default %s"%settings.model_id)
    else:
        settings.model_id = frontj['model_id']

    if 'apiMapping' not in frontj:
        om_err_output("no apiMapping information in frontpage data, exit now")
        exit(-1)
        
    parse_api_mapping(frontj['apiMapping'])
    
    #show_all_apis()

    if 'masterViews' not in frontj:
        om_err_output("no masterViews information in masterViews data, exit now")
        exit(-1)

    recom_data = get_recom_data()
    if recom_data is None or len(recom_data) == 0:
        om_err_output("recom data is not complete, exit now")
        exit(-1)

    try:
        recomj = json.loads(recom_data)
    except:
        om_err_output("recom data cannot be jnsonlized, exit now")
        exit(-1)

    if 'masterViews' not in recomj:
        om_err_output("no masterViews information in masterViews data, exit now")
        exit(-1)

    l = len(frontj['masterViews'])
    i = 1
    j = 1
    while i <= l: 
        v = frontj['masterViews'][i-1]
        column_index = v['index']
        from_re = v['from_re']
        merged_column = v
        recom_columns = recomj['masterViews']
        if j != column_index:
            for c in recom_columns:
                re_column_index = c['index']
                if re_column_index != j:
                    continue
                merged_column = c
                recom_columns.remove(c)
                i -= 1
                break
        col = parse_column(merged_column)
        if col is None:
            return False
        if from_re == 1:
            col.from_re = True
        settings.master_views.append(col)
        i += 1
        j += 1

    if len(recom_columns) == 0:
        return True
    for c in recom_columns:
        col = parse_column(c)
        settings.master_views.append(col)

    return True
        
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

def notify_alarm_by_mail():
    if not os.path.exists(alarm_file):
        return
    fd = open(alarm_file, "r")
    content = fd.read()
    fd.close()

    if len(content.strip()) == 0:
        return

    subject = ("production frontpage service(%s) has alarm need your "
               "attention"%settings.VENDER)
    signature = ("\nregards\n"
                 "wangliang8@hisense.com")
    content += "\n" + signature + "\n"

    from mail import send_mail
    send_mail(subject, content)
    om_output("alarm found, mail notification send")

def set_alarm_configration():
    # set the alarm file
    global alarm_file
    alarm_file = "%s_%s.alm"%(os.path.splitext(sys.argv[0])[0], settings.VENDER)
    os.environ['alarm_file'] = alarm_file
    # if the file already exit, just clear it
    if os.path.exists(alarm_file):
        os.remove(alarm_file)

web_directory = "/home/denny/project/web/monitor"
def copy_to_web_location(filename):
    # currently support copy filename in current path to web path
    if not os.path.exists(filename):
        print "cannot find alarm_file", filenaame
        return
    import shutil
    target = os.path.join(web_directory, filename+".txt")
    shutil.copyfile(filename, target)

def mark_success(alarm_file):
    with open(alarm_file, "w") as fd:
        fd.write("verification succeed at %s\n"%
                 (str(datetime.now())[:19]))
        fd.close()
        
if __name__ == "__main__":
    handle_argv()
    if not data_initialize():
        om_err_output("main() fail to initialize data")

    set_alarm_configration()
    examine()
    # if there is alarm file generated, it means there are some error
    # need to send mail report
    # if there is no alarm file generated, just create one and write
    # success sentence notification
    if not os.path.exists(alarm_file):
        mark_success(alarm_file)
    else:
        notify_alarm_by_mail()
    copy_to_web_location(alarm_file)

    print "Done"
    

