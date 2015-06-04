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
import api_module
from api_module import ErrCode
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)

alarm_file = ""

class Tile(object):
    def __init__(self, id):
        self.index = id
        self.pos = []
        self.size = []
        self.facets = []

    def __repr__(self):
        s =  "++<Tile> index: {0}, pos: ({1}, {2}), size: ({3}, {4})\n"\
            .format(self.index, self.pos[0], self.pos[1], self.size[0],
                    self.size[1])
        for f in self.facets:
            s += repr(f) + "\n"
        return s[:-1]

    def _short(self):
        s =  "++<Tile> index: {0}, pos: ({1}, {2}), size: ({3}, {4})"\
            .format(self.index, self.pos[0], self.pos[1], self.size[0],
                    self.size[1])
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
        om_output("verify the tile %s"%self._short())
        settings.exam_stack_push(self)
        for f in self.facets:
            if not f.self_verify():
                om_err_output("fail to verify %s"%self._short())
                # note currently there is only on facet in one tile
                # and we can return when we found an error,
                # if you want to check all the facet, and return together
                # just do not return here
                settings.exam_stack_pop()
                return False
        settings.exam_stack_pop()
        return True

class Facet(object):
    """ alarm will be print in Facet """
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
            return False
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
        om_output("verify the Facet %s"%self._short())
        settings.exam_stack_push(self)
        if not self.pic_verify():
            settings.exam_stack_pop()
            return False
        api = api_module.api_mapping[self.typecode]
        if self.typecode not in api_module.module_mapping:
            om_err_output("Facet::self_verify() no api module defined for "
                          "typecode %s"%self.typecode)
            settings.exam_stack_pop()
            return False
        # get class type related to the typecode
        cl = api_module.module_mapping[self.typecode]
        m = cl(self.id)
        if not m.valid():
            om_err_output("apimodule is not valid for typecode %s"%self.typecode)
            settings.exam_stack_pop()
            return False
        if not m.verify():
            for ecode, emsgs in m.last_err.items():
                om_err_output("fail to verify %s"%(self._short()))
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
                    alarm(ALARM_LEVEL.HIGH, ALM_DATA_INVALID, alarm_msg)
                elif ecode == ErrCode.BAD_LIST_VIEW_MEDIA or \
                         ecode == ErrCode.BAD_LIST_VIEW_IMAGE:
                    alarm(ALARM_LEVEL.HIGH, ALM_CATEGORY_HAS_BAD_MEDIAS, alarm_msg)
                else:
                    alarm(ALARM_LEVEL.NORMAL, ALM_BASIC, alarm_msg)
                    
            settings.exam_stack_pop()
            return False
        settings.exam_stack_pop()
        return True

    def pic_verify(self):
        succ, msg = validate_pic(self.pic)
        if succ is False:
            alarm(ALARM_LEVEL.CRITICAL, ALM_POSTER_IMAGE_GONE,
                  "picture of url{url} cannot be loaded, err({err_msg})\n"
                  "\nlocation: \n{location}".\
                  format(url=self.pic, err_msg=msg,
                         location=settings.show_exam_stack()))
            return False
        return True

class View(object):
    def __init__(self, name, navid):
        self.name = name
        self.navid = navid
        self.layout = ""
        self.tiles = []

    def __repr__(self):
        s = "<View> name: {0}, navid: {1}, layout: {2}\n"\
            .format(self.name.encode('utf-8'), self.navid, self.layout)
        for t in self.tiles:
            s += repr(t) + "\n"
        return s

    def _short(self):
        s = "<View> name: {0}, navid: {1}, layout: {2}"\
            .format(self.name.encode('utf-8'), self.navid, self.layout)
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
        om_output("verify view name %s"%self.name)
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
    om_output("get frontpage data from %s"%settings.VOD_FRONTPAGE_URL)
    try:
        c = pycurl.Curl()
        b = StringIO.StringIO()
        c.setopt(pycurl.URL, settings.VOD_FRONTPAGE_URL)
        c.setopt(pycurl.CONNECTTIMEOUT, 8)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.LOW_SPEED_LIMIT, 1)
        c.setopt(pycurl.LOW_SPEED_TIME, 20)
        c.perform()
        data = b.getvalue()
    except:
        om_err_output("exception meet when getting frontapge data (%s)"%
                      settings.VOD_FRONTPAGE_URL)
        data = None
    return data

def parse_api_mapping(data):
    for code in data.keys():
        api = api_module.API(code)
        api.set_url(data[code]['api'])
        api.set_params(data[code]['params'])

def parse_view(data):
    if not isinstance(data, dict):
        om_fatal_output("navigation data is not a dict type, exit now")
        exit(-1)
        
    v = View(data['title'], data['navigationId'])
    v.layout = data['layoutId']
    if 'tiles' not in data:
        om_fatal_outut("parse_navigation()::no tiles in view data")
        exit(-1)
    for t in data['tiles']:
        tile = parse_tile(t)
        if tile is None:
            om_err_output("parse_view() fail to parse view %s"%data['title'])
            return None
        v.tiles.append(parse_tile(t))
    return v
        
def parse_tile(data):
    if not isinstance(data, dict):
        om_fatal_output("parse_tile()::tile data is not a dict type, exit now")
        exit(-1)
        
    t = Tile(data['index'])
    t.pos = [int(data['x']), int(data['y'])]
    t.size = [int(data['height']), int(data['width'])]

    if 'facets' not in data:
        om_fatal_output("parse_tile()::no facets in tile data")
        exit(-1)

    for f in data['facets']:
        facet = parse_facet(f)
        if facet is None:
            return None
        t.facets.append(facet)
    return t
        
def parse_facet(data):
    if not isinstance(data, dict):
        om_fatal_output("parse_facet()::facet data is not a dict type, exit now")
        om_output(str(data))
        exit(-1)
    f = Facet(str(data['typeCode']), data['title'])
    f.id = data['id']
    if len(data['backgroundImages']) == 0:
        # for no backgroundimage problem just set the picture to empty
        # and the later verification will report related error with alarm
        om_err_output("parse_facet() fail to parse facet %s due to no "
                      "backgroudImages found"%data['title'])
        f.pic = ""
    else:
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
    om_output("start to initialize frontpage data")
    retry_times_left = 3
    while retry_times_left > 0:
        frontpage_data = get_frontpage_data()
        if frontpage_data is not None and len(frontpage_data) > 0:
            break
        retry_times_left -= 1
    if retry_times_left <= 0:
        alarm(ALARM_LEVEL.CRITICAL, "NETWORK_ISSUE", "cannot get frontpage "
              "data after several reties, url(%s) is not accessable"
              %settings.VOD_FRONTPAGE_URL)
        exit(-1)

    try:
        frontj = json.loads(frontpage_data)
    except:
        om_fatal_output("frontpage data can not be jsonlized, exit now")
        exit(-1)

    if 'apiMapping' not in frontj:
        om_fatal_output("no apiMapping information in frontpage data, exit now")
        exit(-1)
        
    parse_api_mapping(frontj['apiMapping'])
    
    if 'masterViews' not in frontj:
        om_fatal_output("no apiMapping information in masterViews data, exit now")
        exit(-1)

    for v in frontj['masterViews']:
        view = parse_view(v)
        if view is None:
            return False
        settings.master_views.append(view)
    return True

def handle_argv():
    global VOD_FRONTPAGE_URL, VENDER
    if len(sys.argv) == 2:
        if sys.argv[1] == '-d':
            settings.debug_mode = True
        else:
            settings.VENDER = sys.argv[1]
            if settings.VENDER.upper() not in settings.FRONTPAGE.keys():
                om_fataal_ouptput("not support vender %s"%settings.VENDER)
                exit(0)
            settings.VOD_FRONTPAGE_URL = \
                            settings.FRONTPAGE[settings.VENDER.upper()]
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-d" :
            settings.debug_mode = True
            settings.VENDER = sys.argv[2]
            if settings.VENDER.upper() not in settings.FRONTPAGE.keys():
                #err("not support vender %s"%settings.VENDER)
                om_fatal_output("not support vender %s"%settings.VENDER)
                exit(0)
            settings.VOD_FRONTPAGE_URL = \
                            settings.FRONTPAGE[settings.VENDER.upper()]
        elif sys.argv[2] == '-d':
            settings.debug_mode = True
            settings.VENDER = sys.argv[1]
            if settings.VENDER.upper() not in settings.FRONTPAGE.keys():
                #err("not support vender %s"%settings.VENDER)
                om_fatal_output("not support vender %s"%settings.VENDER)
                exit(0)
            settings.VOD_FRONTPAGE_URL = \
                            settings.FRONTPAGE[settings.VENDER.upper()]
        else:
            #err("invalid parameter")
            om_fatal_output("invalid parameter")
            exit(0)
    else:
        #err("invalid parameter")
        om_fatal_output("invalid parameter")
        exit(0)

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
                 (str(datetime.now() + timedelta(hours=8))[:19]))
        fd.close()
    
if __name__ == "__main__":
    handle_argv()
    settings.set_module_name("LAUNCHER_MON_%s"
                             %(settings.VENDER))
    if not data_initialize():
        om_err_output("main() fail to initialize data")
        exit(0)
    
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
    #copy_to_web_location(alarm_file)

    print "Done"

