#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c)  2015 Denny Wang (wangliang8@hisense.com)
# License: Hisense Cloud

'''
this file define the class or functions to handle the detail
implementation of the APIs, different kind of API has different
working rules, so here define API module for each API, it has
the self verification, setup url abilities.

the real url for each API was given from the data file, so
api_mapping dictionary will be filled by launcher program
'''

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import os
import re
import pycurl
import jinja2
import StringIO
import json
import settings
import time
import logging
import logging.config
import media_desc
from datetime import datetime, timedelta
from utils import validate_pic,  dump_pic
api_mapping = {}


logging.config.fileConfig('api_module.conf')

rate = 0.6

list_view_height = 360 * rate
list_view_width = 275 * rate
list_view_info_height = 80 * rate

media_desc.data_initialize()

def get_second_title(mid, title):
    ret = media_desc.get_desc_by_title(title.strip())
    if ret is None:
        return title
    return ret

def _gen_medias_html(path, medias):
    x = 20
    y = 60
    count_per_line = 7
    
    xcell = 10
    ycell = 10
    line = '''<div class="poster" style="top:{top};left:{left};position:absolute;z-index:1;visibility:show;"><a href="{detail_link}"><img src="{pic}" title="{title}" alt="{alt}" style="width:100%; height:100%"></img></a><div class="info"><p class="title">{title}</p><p class="desc">{description}</p></div></div>'''
    i = 0
    s = ""
    while i < len(medias):
        m = medias[i]
        picture = m['image_icon_url']
        iqiyi_re = re.compile(r'qiyipic')
        if iqiyi_re.search(picture):
            picture = dump_pic(picture)
        title = m['title']
        alt = title
        ret, msg = validate_pic(picture)
        if not ret:
            alt += " (no picture load)"

        yy = (i / count_per_line) * (list_view_height + ycell + list_view_info_height) +  y
        xx = (i % count_per_line) * (list_view_width + xcell)  + x
        ma = MediaApiModule(m['id'])
        # we know the media path is the same level of category
        detail_link = ma.export_html(path, False)
        detail_link = os.path.join('../', detail_link)
        s += line.format(top=yy, left=xx, pic=picture,
                         title=title,
                         width=list_view_width,
                         height=list_view_height,
                         detail_link=detail_link,
                         alt=alt,
                         description = get_second_title(m['id'], title))
        s += '\n'
        i += 1

    return s

# all the API verification will support return multiple err code
class ErrCode():
    RESOURCE_CANT_ACCESS = 1
    RESOURCE_OFFLINE = 2
    DATA_INVALID = 3

    BAD_LIST_VIEW_IMAGE = 10
    BAD_LIST_VIEW_MEDIA = 11
    BAD_DETAIL_VIEW_IMAGE = 12

    OTHERS = 99
    

class API(object):
    def __init__(self, code):
        global api_mapping
        self.code = code
        api_mapping[code] = self
        self.url = ""
        self.params = ""

    def set_url(self, url):
        self.url = url

    def set_params(self, params):
        self.params = params

    def __repr__(self):
        return "code: %s\nurl: %s\nparams=%s"%(self.code,
                                               self.url,
                                               self.params)


class ApiModule(object):
    myinfo_format = "{type}: {id}, url: {url}"
    def __init__(self, sid, name=""):
        self.url = ""
        self.params = ""
        self.id = sid
        self.data = ""
        self.typecode = ""
        self.is_valid = False
        self.name = name
        # set my information but without url here
        self.myinfo = "type: %s, id: %s"%\
                      (self.__class__.__name__, self.id)
        # all module can return multiple error code, and will
        # store error messages for earch error code, so i use
        # a hash variable here
        self.last_err = {}

    def _fill(self, typecode):
        self.typecode = typecode
        if typecode not in api_mapping:
            self.is_valid = False
            return
        api = api_mapping[typecode]
        self.url = api.url
        self.url = self.setup_url()
        self.myinfo += ", url=%s"%self.url
        logging.debug(self.myinfo)
        self.params = api.params
        self.is_valid = True

    def set_err(self, ecode, msg):
        msg_with_myinfo = "%s %s"%(self.myinfo, msg)
        if ecode in self.last_err:
            self.last_err[ecode].append(msg_with_myinfo)
        else:
            self.last_err[ecode] = [msg_with_myinfo]
        
    def valid(self):
        return self.is_valid

    def setup_url(self):
        return "http://test_url"
    def retrieve(self):
        err_msg = ""
        logging.debug("going to access %s"%self.url)
        for i in range(0, 3):
            try:
                c = pycurl.Curl()
                b = StringIO.StringIO()
                c.setopt(pycurl.URL, self.url)
                c.setopt(pycurl.CONNECTTIMEOUT, 10)
                c.setopt(pycurl.WRITEFUNCTION, b.write)
                c.setopt(pycurl.LOW_SPEED_LIMIT, 1)
                c.setopt(pycurl.LOW_SPEED_TIME, 20)
                c.perform()
                self.data = b.getvalue()
                return True
            except KeyboardInterrupt:
                exit(2)
            except Exception, e:
                err_msg = "{url} canot be accessed, meet error ({err})".\
                          format(url=self.url, err=str(e))
                self.data = None
                continue
        # here means retrieve fail after retry serval times
        self.set_err(ErrCode.RESOURCE_CANT_ACCESS, err_msg)
        logging.error("cannot access %s"%self.url)
        return False
                
    def export_html(self, path, override=False):
        return "#"

    def verify_basic(self):
        if not self.retrieve():
            return False
        return self.verify_response_basic()
            
    def verify(self):
        if not self.retrieve():
            return False
        return self.verify_response()

    def verify_response(self):
        return True

    def verify_response_basic(self):
        return True

class CategoryApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self.first_page_start =  0
        self.page_count = 105
        self._fill('1001')
        self.MEDIA_DETAIL_ACCESS_DURATION = 3

    # should be called after calling self._fill()
    def setup_url(self):
        url = self.url + "/" + str(self.id) + "?start=%s&rows=%s"\
              %(self.first_page_start, self.page_count)
        return url

    def verify_response_basic(self):
        # for category, basic verification is just only check response data 
        j = None
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "fail to load response "
                         "data to json")
            return False
        if not isinstance(j, dict):
            self.set_err(ErrCode.DATA_INVALID, "data should be aa dict type")
            return False
        if 'medias' not in j:
            self.set_err(ErrCode.DATA_INVALID, "no medias tag found")
            return False

        medias = j['medias']
        if len(medias) == 0:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this category is 0")
            logging.error("the number of media is 0 for category %s"%self.id)
            return False
        
        min_num = 2
        if len(medias) < min_num:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this category is less than "
                         "%d, actual %d"%(min_num, len(medias)))
            logging.error("the number of media of category %s is less than "
                          "%d, actual %d"%(self.id, min_num, len(medias)))
            return False
        logging.debug("category %s has %s medias found"%(self.id, len(medias)))
            
        return True

    def verify_response(self):
        j = None
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "fail to load response "
                         "data to json")
            return False
        if not isinstance(j, dict):
            self.set_err(ErrCode.DATA_INVALID, "data should be aa dict type")
            return False
        if 'medias' not in j:
            self.set_err(ErrCode.DATA_INVALID, "no medias tag found")
            return False
        medias = j['medias']
        success = self._verify_medias(medias)
        return success

    def _verify_medias(self, medias):
        if not isinstance(medias, list):
            self.set_err(ErrCode.DATA_INVALID,
                         "medias data should be a list type")
            return False
        if len(medias) == 0:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this category is 0")
            logging.error("the number of media is 0 for category %s"%self.id)
            return False
        
        min_num = 2
        if len(medias) < min_num:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this category is less than "
                         "%d, actual %d"%(min_num, len(medias)))
            logging.error("the number of media of category %s is less than "
                          "%d, actual %d"%(self.id, min_num, len(medias)))
            return False
        logging.debug("category %s has %s medias found"%(self.id, len(medias)))
        succ = True
        for i in xrange(0, len(medias)):
            start_ts = time.time()
            # here will not return false for one media check fail
            if not self._verify_media(medias, i):
                succ = False
            end_ts = time.time()
            delta = int((end_ts - start_ts)*1000)
            if delta > self.MEDIA_DETAIL_ACCESS_DURATION * 1000:
                logging.warn("retrieving duration "
                             "more than %s msc, actual duration is %s msc, "
                             "%sst time"%(
                                 self.MEDIA_DETAIL_ACCESS_DURATION*1000,
                                 delta, i))
                
        return succ

    def _verify_media(self, medias, i):
        media = medias[i]
        if not isinstance(media, dict):
            self.set_err(ErrCode.DATA_INVALID,
                         "%sst media data should be dict type"%i)
            return False
        if 'title' not in media:
            self.set_err(ErrCode.DATA_INVALID,
                         "%sst media data has no title field"%i)
            return False

        if 'image_icon_url' not in media:
            self.set_err(ErrCode.DATA_INVALID, "media has no image field")
            logging.error("cannot load list view image for %s in category %d"%\
                          (media['title'], self.id))
            return False

        succ, msg = validate_pic(media['image_icon_url'])
        if succ is False:
            self.set_err(ErrCode.BAD_LIST_VIEW_IMAGE, "the %sst media(%s) "
                         "has no picture load successfully, err(%s)"%\
                         (i, media['title'], msg))
            logging.error("%sst media(%s) has no picture load successfully, "
                        "err(%s)"%(i, media['title'], msg))
            return False

        m = MediaApiModule(media['id'])
        if not m.verify():
            # because it is a category list view, so the media offline
            # error is not the same level of media view, so just wrap
            # it to a lower level of error
            # merge all the error here to one eror BAD_LIST_VIEW_MEDIA
            for ecode, msgs in m.last_err.items():
                for m in msgs:
                    self.set_err(ErrCode.BAD_LIST_VIEW_MEDIA,
                                 "\nthe %sst item:\n"%i + m)
                    logging.error(m)
            return False
        
        return True

    def export_html(self, path, override=False):
        prefix = os.environ.get('file_prefix', '')
        new_url = "categories/%s%s.html"%(prefix, self.id)
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"

        medias = j['medias']
        if len(medias) == 0:
            return new_url
        
        content = _gen_medias_html(path, medias)
        
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "category.tpl"
        template = templateEnv.get_template(template_file)
        output = template.render(content=content,
                                 width=list_view_width,
                                 height=list_view_height,
                                 info_height=list_view_info_height,
                                 page_title=self.name,
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url

class MediaApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill('1002')

    def setup_url(self):
        url = self.url + "/" + str(self.id) + "?vender=0"
        return url

    def verify_response_basic(self):
        # for media, the basic verification is the same with detail
        return self.verify_response()

    def verify_response(self):
        if self.data is None:
            return False
        j = None
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID,
                         "fail to load response data to json")
            return False
        
        return self._verify_media(j)

    def _verify_media(self, data):
        fail_reason = ""
        if not self._verify_online(data):
            self.set_err(ErrCode.RESOURCE_OFFLINE, "media is offline")
            logging.error("media %s is offline"%self.id)
            return False
        if not self._verify_title(data):
            self.set_err(ErrCode.DATA_INVALID, "no title information provided")
            logging.error("media %s has no title"%self.id)
            return False
        logging.debug("verify media %s"%data['title'])
        if not self._verify_video(data):
            self.set_err(ErrCode.DATA_INVALID, "video information is invalid")
            return False
        return True

    def _verify_online(self, data):
        """ the {'success': true} means offline """
        logging.debug("MediaApiModule::_verify_online() check whether the"
                      "medias is online")
        if 'id' in data:
            return True
        return False
   
    def _verify_title(self, data):
        logging.debug("MediaApiModule::_verify_title() check whether the media "
                      "has related title")
        if not "title" in data:
            return False
        return True

    def _verify_video(self, data):
        logging.debug("MediaApiModule::_verify_video() check the video is valid")
        if not "videos" in data:
            return False
        videos =  data['videos']
        if len(videos) == 0:
            logging.error("media %s %s has 0 videos information"%\
                          (self.id, data['title']))
            return False
        if 'play_ways' not in videos[0]:
            return False
        if len(videos[0]['play_ways']) == 0:
            return False
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "medias/%s%s.html"%(prefix, self.id)
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"
        content = {}
        if 'title' not in j:
            self.set_err(ErrCode.DATA_INVALID, "export_html() no title "
                         "field found")
            return "#None"
        content['title'] = j['title']
        content['num'] = len(j['videos'])
        iqiyi_re = re.compile(r'qiyipic')
        picture = j['image_post_url']
        m = iqiyi_re.search(picture)
        if m:
            content['pic'] = dump_pic(picture)
        else:
            content['pic'] = picture
        content['content'] = j['summary']
        content['create_time'] = str(datetime.now())[:19]
        content['actors'] = " | ".join(j['actor'])
        content['category'] = j['category']
        content['tag'] = " | ".join(j['child_category'])
        media_id = j['id']
        if len(j['videos']) == 0:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to get video info,"
                         " video number is 0")
            return "#None"
        video_id = j['videos'][0]['id']
        content['history_url'] = settings.HISTORY_URL.format(
            settings.uuid, media_id, video_id)
        
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "detail.tpl"
        template = templateEnv.get_template(template_file)
        output = template.render(**content)
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url

class TopicApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2005")
        self.MEDIA_DETAIL_ACCESS_DURATION = 3

    def setup_url(self):
        url = self.url + "?topicId=" + str(self.id)
        return url

    def verify_response_basic(self):
        j = None
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "fail to load response "
                         "data to json")
            return False
        if not isinstance(j, dict):
            self.set_err(ErrCode.DATA_INVALID, "data should be aa dict type")
            return False
        if 'medias' not in j:
            self.set_err(ErrCode.DATA_INVALID, "no medias tag found")
            return False

        if not 'background' in j:
            self.set_err(ErrCode.DATA_INVALID,
                         "the background image is absent")
            logging.err("the number of the background image of the topic "
                        "%d is absent"%self.id)

        succ, msg = validate_pic(j['background'])
        if succ is False:
            self.set_err(ErrCode.BAD_DETAIL_VIEW_IMAGE, "topic(%s) background "
                         "image cannot be loaded successfully, err(%s)"%\
                         (media['title'], msg))
            logging.error("topic(%s) background "
                         "image cannot be loaded successfully, err(%s)"%\
                         (media['title'], msg))
            return False

        medias = j['medias']
        if len(medias) == 0:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this topic is 0")
            logging.error("the number of media is 0 for topic %s"%self.id)
            return False
        
        min_num = 2
        if len(medias) < min_num:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this topic is less than "
                         "%d, actual %d"%(min_num, len(medias)))
            logging.error("the number of media of topic %s is less than "
                          "%d, actual %d"%(self.id, min_num, len(medias)))
            return False
        logging.debug("topic %s has %s medias found"%(self.id, len(medias)))
            
        return True

    def verify_response(self):
        j = None
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "fail to load response "
                         "data to json")
            return False
        if not isinstance(j, dict):
            self.set_err(ErrCode.DATA_INVALID, "data should be aa dict type")
            return False
        if 'medias' not in j:
            self.set_err(ErrCode.DATA_INVALID, "no medias tag found")
            return False
        medias = j['medias']
        success = self._verify_medias(medias)
        return success

    def _verify_medias(self, medias):
        if not isinstance(medias, list):
            self.set_err(ErrCode.DATA_INVALID,
                         "medias data should be a list type")
            return False
        if len(medias) == 0:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this category is 0")
            logging.error("the number of media is 0 for category %s"%self.id)
            return False
        
        min_num = 2
        if len(medias) < min_num:
            self.set_err(ErrCode.DATA_INVALID,
                         "the number of media of this category is less than "
                         "%d, actual %d"%(min_num, len(medias)))
            logging.error("the number of media of category %s is less than "
                          "%d, actual %d"%(self.id, min_num, len(medias)))
            return False
        logging.debug("category %s has %s medias found"%(self.id, len(medias)))
        succ = True
        for i in xrange(0, len(medias)):
            start_ts = time.time()
            # here will not return false for one media check fail
            if not self._verify_media(medias, i):
                succ = False
            end_ts = time.time()
            delta = int((end_ts - start_ts)*1000)
            if delta > self.MEDIA_DETAIL_ACCESS_DURATION * 1000:
                logging.warn("retrieving duration "
                             "more than %s msc, actual duration is %s msc, "
                             "%sst time"%(
                                 self.MEDIA_DETAIL_ACCESS_DURATION*1000,
                                 delta, i))
                
        return succ

    def _verify_media(self, medias, i):
        media = medias[i]
        if not isinstance(media, dict):
            self.set_err(ErrCode.DATA_INVALID,
                         "%sst media data should be dict type"%i)
            return False
        if 'title' not in media:
            self.set_err(ErrCode.DATA_INVALID,
                         "%sst media data has no title field"%i)
            return False

        if 'image_icon_url' not in media:
            self.set_err(ErrCode.DATA_INVALID, "media has no image field")
            logging.error("cannot load list view image for %s in category %d"%\
                          (media['title'], self.id))
            return False

        succ, msg = validate_pic(media['image_icon_url'])
        if succ is False:
            self.set_err(ErrCode.BAD_LIST_VIEW_IMAGE, "the %sst media(%s) "
                         "has no picture load successfully, err(%s)"%\
                         (i, media['title'], msg))
            logging.error("%sst media(%s) has no picture load successfully, "
                        "err(%s)"%(i, media['title'], msg))
            return False

        m = MediaApiModule(media['id'])
        if not m.verify():
            # because it is a category list view, so the media offline
            # error is not the same level of media view, so just wrap
            # it to a lower level of error
            # merge all the error here to one eror BAD_LIST_VIEW_MEDIA
            for ecode, msgs in m.last_err.items():
                for m in msgs:
                    self.set_err(ErrCode.BAD_LIST_VIEW_MEDIA,
                                 "\nthe %sst item:\n"%i + m)
                    logging.error(m)
            return False
        
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "topics/%s%s.html"%(prefix, self.id)
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"

        medias = j['medias']
        if len(medias) == 0:
            return new_url
        rate = 0.6
        height = 320 * rate
        width = 250 * rate
        content = self._gen_background_html(j['background'])
        content += self._gen_medias_html(path, medias, width, height)
        
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "topic.tpl"
        
        template = templateEnv.get_template(template_file)
        output = template.render(content=content,
                                 page_title="专题详情",
                                 width=width,
                                 height=height,
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url

    def _gen_background_html(self, bg_picture):
        line = '''
        <div style="top:{top};left:{left};width:{width};height:{height};position:absolute;z-index:0;visibility:show;background-image:url({pic}); background-repeat:no-repeat;background-size:100% 100%"></div>
        '''
        x = 20
        y = 60
        width = 1080
        height = 607
        return line.format(pic=bg_picture, top=y, left=x, width=width, height=height)

    def _gen_medias_html(self, path, medias, width, height):
        x = 20
        y = 480
        count_per_line = 7
        
        xcell = 12
        ycell = 10
        rate = 0.6
        line = '''<div class="poster" style="top:{top};left:{left};position:absolute;z-index:1;visibility:show;"><a href="{detail_link}"><img src="{pic}" title="{title}" alt="{alt}" style="width:100%; height:100%"></img></a></div>'''
        i = 0
        s = ""
        while i < len(medias):
            m = medias[i]
            picture = m['image_icon_url']
            iqiyi_re = re.compile(r'qiyipic')
            if iqiyi_re.search(picture):
                picture = dump_pic(picture)
            title = m['title']
            alt = title
            ret, msg = validate_pic(picture)
            if not ret:
                alt += " (no picture load)"
                
            yy = (i / count_per_line) * (height + ycell) + y
            xx = (i % count_per_line) * (width + xcell) + x + 10
            ma = MediaApiModule(m['id'])
            # we know the media path is the same level of category
            detail_link = ma.export_html(path, False)
            detail_link = os.path.join('../', detail_link)
            s += line.format(top=yy, left=xx, pic=picture,
                             title=title,
                             width=width*rate,
                             height=height*rate,
                             detail_link=detail_link,
                             alt=alt,
                             description=get_second_title(m['id'], title))
            s += '\n'
            i += 1
            
        return s

class RelateApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2007")

    def setup_url(self):
        url = self.url + "/" + str(self.id)
        return url

    def verify(self):
        return True

class getAllTrades(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("5002")

    def setup_url(self):
        url = self.url + "/" + str(self.id)
        return url

    def verify(self):
        return True

class ColumViewCategory(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name="")
        self._fill("1007")

    def setup_url(self):
        url = self.url + "/" + str(self.id)
        return url

    def verify(self):
        return True
    
class SearchApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2001")

    def setup_url(self):
        url = self.url
        return url

    def verify(self):
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "functions/%stopsearch.html"%prefix
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"
        if 'medias' not in j:
            raise Exception("SearchApiModule fail to export xml, due to "
                            "cannot find medias")
        medias = j['medias']
        if len(medias) == 0:
            return new_url

        content = _gen_medias_html(path, medias)
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "category.tpl"
        template = templateEnv.get_template(template_file)
        output = template.render(content=content,
                                 width=list_view_width,
                                 height=list_view_height,
                                 info_height=list_view_info_height,
                                 page_title="热门搜索",
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url
    
class News7daysApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2003")

    def setup_url(self):
        url = self.url
        return url

    def verify(self):
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "functions/%snews7days.html"%prefix
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"

        medias = j['medias']
        if len(medias) == 0:
            return new_url

        content = _gen_medias_html(path, medias)
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "category.tpl"
        template = templateEnv.get_template(template_file)
        output = template.render(content=content,
                                 width=list_view_width,
                                 height=list_view_height,
                                 info_height= list_view_info_height,
                                 page_title="7日更新",
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url
        
    
class TopiclistApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2008")

    def setup_url(self):
        url = self.url + "?start=0&rows=35"
        return url
    
    def verify(self):
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "functions/%stopiclist.html"%prefix
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"

        topics = j['topicList']
        if len(topics) == 0:
            return new_url
        rate = 0.6
        height = 360 * rate
        width = 800 * rate
        content = self._gen_topics_html(path, topics, width, height)
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "topiclist.tpl"
        template = templateEnv.get_template(template_file)
        
        output = template.render(content=content,
                                 width=width,
                                 height=height,
                                 info_height=list_view_info_height,
                                 page_title="所有专题",
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url

    def _gen_topics_html(self, path, topics, width, height):
        x = 20
        y = 60
        count_per_line = 2
        
        xcell = 10
        ycell = 10
        line = '''<div class="poster" style="top:{top};left:{left};position:absolute;z-index:1;visibility:show;"><a href="{detail_link}"><img src="{pic}" title="{title}" alt="{alt}" style="width:100%; height:100%"></img></a></div>'''
        i = 0
        s = ""
        while i < len(topics):
            t = topics[i]
            picture = t['pics'][0]['url']
            title = t['topicName']
            alt = title
            ret, msg = validate_pic(picture)
            if not ret:
                alt += " (no picture load)"

            yy = (i / count_per_line) * (height + ycell) + y
            xx = (i % count_per_line) * (width + xcell) + x
            td = TopicApiModule(t['topicId'])
            # we know the media path is the same level of category
            detail_link = td.export_html(path, False)
            detail_link = os.path.join('../', detail_link)
            s += line.format(top=yy, left=xx, pic=picture,
                             title=title, 
                             detail_link=detail_link,
                             alt=alt)
            s += '\n'
            i += 1
        return s

class HistoryApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("3001")

    def setup_url(self):
        url = self.url + "/" + self.id
        return url
    def verify(self):
        return True

class GuessApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2006")

    def setup_url(self):
        url = self.url + "/" + self.id
        return url

    def verify(self):
        return True

class AllwatchApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("2002")

    def setup_url(self):
        url = self.url
        return url

    def verify(self):
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "functions/%sallwatching.html"%prefix
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"
        if 'medias' not in j:
            self.set_err(ErrCode.DATA_INVALID, "no medias tag found")
            return False
        medias = j['medias']
        if len(medias) == 0:
            return new_url

        content = _gen_medias_html(path, medias)
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "category.tpl"
        template = templateEnv.get_template(template_file)
        output = template.render(content=content,
                                 width=list_view_width,
                                 height=list_view_height,
                                 info_height=list_view_info_height,
                                 page_title="大家正在看",
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url

class ConcertApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("5008")

    def setup_url(self):
        url = self.url + "/" + self.id
        return url

    def verify(self):
        return True

class CatchApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("3002")

    def setup_url(self):
        url = self.url + "/" + self.id
        return url

    def verify(self):
        return True

class getVIPinfo(ApiModule):
    VIP_TITLE_INDEX = 0
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("5006")

    def setup_url(self):
        url = self.url + "?vipId=" + self.id
        return url

    def verify(self):
        return True

    def gen_vip_dialog(self, id, title, desc, prices, medias_link):
        info = '''<div class="modal fade" id="{id}" tabindex="-1" role="dialog" aria-labelledby="{id}" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" id="myModalLabel">< {title}</h4>
          </div>
          <div class="modal-body">
            <div class="container">
              <div class="row">
                <div class="col-md-6">
                  {desc}
                </div>
                <div class="col-md-6">
                  <table class="table table-hover" style="boder:none;">
                    <tbody>
                      {prices_string}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <a href="{medias_link}" class="btn btn-primary">进入影片列表</a>
          </div>
        </div>
      </div>
    </div>'''
        price_info = '''<tr><td>{discount}</td><td><strike>{price}</strike></td></tr>'''
        prices_string = ""
        for p in prices:
            prices_string += price_info.format(price=p[0], discount=p[1])
        return info.format(title=title, id=id, desc=desc, prices_string=prices_string, medias_link=medias_link)


    def export_html(self, path, override=True):
        # normally export_html return the new url, but this api
        # return the html code
        prefix = os.environ.get('file_prefix', '')
        new_url = "functions/%sallwatching.html"%prefix
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"
        title = j['title']
        desc = j['desc']
        prices = []
        for p in j['fee_detail']:
            # no check for current price info, is should not be empty
            current = "%s元/%s"%(float(p['price']['price'])/100, p['price']['desc'])
            discount = ""
            if not p['discount']:
                discount = current
            else:
                discount = "%s元/%s"%(float(p['discount']['discountPrice'])/100, p['discount']['desc'])
            prices.append([current, discount])
        getVIPinfo.VIP_TITLE_INDEX += 1
        m = getVIPmedias(self.id, title)
        medias_link = m.export_html(settings.POSTER_HOME, settings.override)
        
        return self.gen_vip_dialog("basicModal%s"%str(getVIPinfo.VIP_TITLE_INDEX), title,
                                   desc, prices, medias_link)
        

class getVIPmedias(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("5007")

    def setup_url(self):
        url = self.url + "?vipId=" + self.id + "&start=0&rows=100"
        return url

    def verify(self):
        return True

    def export_html(self, path, override=True):
        prefix = os.environ.get('file_prefix', '')
        new_url = "functions/%svipinfo_%s.html"%(prefix, self.id)
        fname = os.path.join(path, new_url)
        if override is False and os.path.exists(fname):
            logging.debug("export %s, ignored"%fname)
            return new_url
        self.retrieve()
        try:
            j = json.loads(self.data)
        except:
            self.set_err(ErrCode.DATA_INVALID, "export_html() fail to load "
                         "response data to json")
            return "#None"
        if 'medias' not in j:
            self.set_err(ErrCode.DATA_INVALID, "no medias tag found")
            return False
        medias = j['medias']
        if len(medias) == 0:
            return new_url

        content = _gen_medias_html(path, medias)
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = "category.tpl"
        template = templateEnv.get_template(template_file)
        output = template.render(content=content,
                                 width=list_view_width,
                                 height=list_view_height,
                                 info_height=list_view_info_height,
                                 page_title=self.name,
                                 create_time=str(datetime.now())[:19])
        fd = open(fname, 'w')
        fd.write(output)
        fd.close()
        return new_url

class FavoriteApiModule(ApiModule):
    def __init__(self, sid, name=""):
        ApiModule.__init__(self, sid, name)
        self._fill("3003")

    def setup_url(self):
        url = self.url + "/" + self.id
        return url

    def verify(self):
        return True
    
module_mapping = {'1001': CategoryApiModule,
                  '1002': MediaApiModule,
                  '1003': MediaApiModule,
                  '1007': ColumViewCategory,
                  '2005': TopicApiModule,
                  '2001': SearchApiModule,
                  '2002': AllwatchApiModule,
                  '2003': News7daysApiModule,
                  '2006': GuessApiModule,
                  '2007': RelateApiModule,
                  '2008': TopiclistApiModule,
                  '3001': HistoryApiModule,
                  '3002': CatchApiModule,
                  '3003': FavoriteApiModule,
                  '5002': getAllTrades,
                  '5006': getVIPinfo,
                  '5007': getVIPmedias,
                  '5008': ConcertApiModule}

