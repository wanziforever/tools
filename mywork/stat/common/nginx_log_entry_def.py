#!/usr/bin/env python
import re
import time

class CallAPI(object):
    FRONTPAGE = 1000
    CATEGORY = 1001
    MEDIA_DETAIL = 1002
    FEATURE_VIEW = 1005
    TOP_SEARCH = 2001
    ALL_WATCHING = 2002
    NEW7DAYS = 2003
    HOT_LIST = 2004
    TOPIC = 2005
    GUESS = 2006
    RELATED_MEDIAS = 2007
    TOPIC_LIST = 2008
    SEARCH_RESULT = 2009
    HISTORY = 3001

    def __init__(self):
        self.mapping = {
            "/frontpage/api/master_views":CallAPI.FRONTPAGE,
            "/category/api/search": CallAPI.CATEGORY,
            "/medias/api/media": CallAPI.MEDIA_DETAIL,
            "/frontpage/api/feature_views": CallAPI.FEATURE_VIEW,
            "/medias/api/topMediaFromSearch": CallAPI.TOP_SEARCH,
            "/stat/api/allwatching": CallAPI.ALL_WATCHING,
            "/medias/api/new7days": CallAPI.NEW7DAYS,
            "/recom/api/getPopularBoard": CallAPI.HOT_LIST,
            "/medias/api/topic/detailpage": CallAPI.TOPIC,
            "/recom/api/getGuess": CallAPI.GUESS,
            "/recom/api/getRelatedMedia": CallAPI.RELATED_MEDIAS,
            "/medias/api/topic/topiclist": CallAPI.TOPIC_LIST,
            "/search/api/getResult": CallAPI.SEARCH_RESULT,
            "/usercenter/api/history/add": CallAPI.HISTORY
            }

    def get_code(self, api):
        #print "CallAPI::get_code() with ", api
        if api in self.mapping:
            return self.mapping[api]
        for api_prefix, code in self.mapping.items():
            l = len(api_prefix)
            if api[:l] == api_prefix:
                return code
        return 0
    

callapi = CallAPI()
class NginxEntry(object):
    #def __init__(self, raw):
    def __init__(self):
        self._init()
        #self.raw = raw

    def set_raw(self, raw):
        self.raw = raw

    def _init(self):
        self.raw = ''
        self.ip = ''
        self.devid = ''
        self.ts = ''
        self.method = ""
        self.api = ''
        self.api_code = 0
        self.params = {}
        self.vender = "NginxEntry_vender"
        self.userid = ''

    def reset(self):
        self._init()

    def parse(self):
        pos = self.raw.find(' ')
        #if pos == -1:
        #    return False
        #self.ip = self.raw[:pos]
        #pos = pos + 6
        #ts = self.raw[pos:pos+20]
        ## add 8 hour to utc time
        #self.ts = int(time.mktime(time.strptime(ts, "%d/%b/%Y:%H:%M:%S")) * 1000) \
        #          + 28800000
        #pos  = pos + 29
        #self.method = self.raw[pos: pos+3]
        #pos = pos + 4
        #epos = self.raw.find(' ', pos)
        #if pos == -1:
        #    return False
        #api = self.raw[pos: epos]
        #p = api.find('?')
        #if p == -1:
        #    self.api = api
        #else:
        #    self.api = api[:p]
        #    for param in api[p+1:].split('&'):
        #        try:
        #            name, value = param.split('=')
        #        except:
        #            continue
        #        self.params[name] = value
        #self.api_code = callapi.get_code(self.api)
        
        return True

    def get_ip(self):
        return self.ip

    def get_devid(self):
        return self.devid

    def get_userid():
        return self.userid

    def get_ts(self):
        return self.ts

    def get_vender(self):
        return self.vender

    def get_method(self):
        return self.method

    def get_api(self):
        return self.api
    
    def get_apicode(self):
        return self.api_code
    
    def get_params(self):
        return self.params
        
    def get_param(self, name):
        if name not in self.params:
            return None
        return self.params[name]
