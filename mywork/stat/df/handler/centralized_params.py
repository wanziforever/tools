#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
old release will only build specific format video play parameters for
video player, and on the front end, terminal logic will have code to
adapt all the player parameters, and new player normally cannot be
supported without the code change, so this file is used to make all
player parameters adaption work at backend, and let the terminal handle
the consistant parameters, also called centralizedParams
"""

import json

class Extras(object):
    PROGRAM_ID = "program_id"
    EPISODE_ID = "episode_id"
    EPISODE_RESOLUTION = "episode_resolution"
    LAST_POSITION_INFO = "last_position_info"
    EPISODE_ACTION_URL = "episode_action_url"
    VIDEO_NAME = "video_name"
    FAVORITE = "isCollect"

class CentralizedParams(object):
    STARTUP_TYPE_ACTIVITY = 1
    STARTUP_TYPE_BROADCAST = 2
    STARTUP_TYPE_INNERPLAYER = 3
    def __init__(self):
        self.StartupType = 1
        self.IntentAction = ""
        self.BundleInfo = []
        self.IntentFlags = []
        self.Extras = []
        self.IntentUrlData = ""
        self.Package = ""

    def convert(self):
        final = {"IntentAction": self.IntentAction,
                 "BundleInfo": self.BundleInfo,
                 "IntentFlags": self.IntentFlags,
                 "Extras": self.Extras,
                 "IntentUrlData": self.IntentUrlData,
                 "Package": self.Package}
        
        return final
        
    def setStartupType(self, type):
        self.StartupType = type
    def setIntentAction(self, action):
        self.IntentAction = action
    def addBundleInfo(self, key, value):
        self.BundleInfo.append({"key":key, "value":value})
    def addFlags(self, flag):
        self.IntentFlags.append(flag)
    def addExtras(self, key, value, type):
        self.Extras.append({"key":key,
                            "value":value,
                            "valueType":type})
    def setIntentUrlData(self, url):
        self.IntentUrlData = url
    def setPackage(self, package_name):
        self.Package = package_name

class CentralizedParamConvertor(object):
     def __init__(self, startup, action, params):
         self.params = params
         self.startup = startup
         self.cp = CentralizedParams()
         self.cp.setStartupType(self.startup)
         self.cp.setIntentAction(action)
         try:
             self.j = json.loads(self.params)
         except Exception, e:
             print "load json fail, ", repr(e)
             self.j = None
     def convert(self):
         return self.cp.convert()
     
     def getStartupType(self):
         return self.startup

class SOHU_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(SOHU_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_ACTIVITY,
             "com.sohutv.tv.action.hisense",
             params
             )
     def convert(self):
         self.cp.addBundleInfo("videoInfo", self.params)
         return self.cp.convert()

class IQIYI_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(IQIYI_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_BROADCAST,
             "com.qiyi.video.action.ACTION_PLAYVIDEO",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         self.j['playType'] = 'vod'
         self.j['history'] = '${history_true_as_0}'
         self.cp.addBundleInfo("playInfo", json.dumps(self.j))
         self.cp.addFlags("FLAG_ACTIVITY_SINGLE_TOP")
         self.cp.addFlags("FLAG_ACTIVITY_NEW_TASK")
         self.cp.addFlags("FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET")
         self.cp.addFlags("FLAG_INCLUDE_STOPPED_PACKAGES")
         return self.cp.convert()

class KU6_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(KU6_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_INNERPLAYER,
             "",
             params
             )

class ICNTV_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(ICNTV_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_INNERPLAYER,
             "",
             params
             )

class LEKAN_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(LEKAN_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_ACTIVITY,
             "com.lekan.tv.kids.his.LekanPlayer",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         self.cp.addExtras(Extras.PROGRAM_ID, "${program_id}", 1)
         self.cp.addExtras("mProgramId", "${program_id}", 1)
         self.cp.addExtras(Extras.EPISODE_ID, "${episode_id}", 1)
         self.cp.addExtras("mEpisodeId", "${episode_id}", 1)
         #self.cp.addExtras("episode_id", "${episode_id}", 1)
         self.cp.addExtras(Extras.EPISODE_RESOLUTION, "${resolution}", 1)
         self.cp.addExtras(Extras.FAVORITE, "${is_favorite}", 3)
         self.cp.addExtras("video_id", self.j.get('video_id', ''), 1)
         self.cp.addExtras("video_idx", self.j.get('video_idx', ''), 1)
         self.cp.addExtras("video_url", self.j.get('video_url', ''), 1)
         self.cp.addExtras("video_w", self.j.get('video_w', 0), 2)
         self.cp.addExtras("video_h", self.j.get('video_h', 0), 2)
         self.cp.addExtras("video_br", self.j.get('video_br', 0), 2)
         
         self.cp.addExtras("openid", "52", 1)
         self.cp.addExtras("media_id", "22", 1)
         self.cp.addExtras("video_name", self.j.get('video_name', ''), 1)
         self.cp.addExtras("video_msg", self.j.get('video_msg', ''), 1)
         self.cp.addExtras("video_pos", "${position_s}", 2)
         return self.cp.convert()

class PPTV_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(PPTV_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_ACTIVITY,
             "android.intent.action.VIEW",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         url = self.j.get("url", '')
         url = url.replace('?', '&')
         if url.find("start_pos") == -1:
             url = url + "&start_pos=${position_ms}"
         self.cp.setIntentUrlData(url)
         self.cp.setPackage("com.pptv.ott.channelplayer")
         self.cp.addFlags("FLAG_ACTIVITY_NEW_TASK")
         self.cp.addExtras(Extras.PROGRAM_ID, "${program_id}", 1)
         self.cp.addExtras(Extras.EPISODE_ID, "${episode_id}", 1)
         self.cp.addExtras(Extras.EPISODE_RESOLUTION, "${resolution}", 1)
         self.cp.addExtras(Extras.FAVORITE, "${is_favorite}", 3)
         return self.cp.convert()

class YOUKU_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(YOUKU_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_BROADCAST,
             "com.youku.tv",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         self.cp.addBundleInfo("RECOMMEND", json.dumps(self.j))
         #self.cp.addFlags("FLAG_INCLDUE_STOPPED_PACKAGES")
         self.cp.addFlags("FLAG_ACTIVITY_NEW_TASK")
         #self.cp.addFlags("FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET")
         return self.cp.convert()

class YOUPENG_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(YOUPENG_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_ACTIVITY,
             "com.voole.epg.Aggregate",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         self.cp.addExtras("mid", self.j.get('intentMid', ''), 1)
         self.cp.addExtras("sid", self.j.get('sid', ''), 1)
         self.cp.addExtras("isCollect", "${is_favorite}", 3)
         self.cp.addExtras("isPlayBack", "${history_0_as_true}", 3)
         self.cp.addExtras("program_id", self.j.get('program_id', ''), 1)
         self.cp.addExtras("episode_id", self.j.get('episode_id', ''), 1)
         return self.cp.convert()
         

class LETV_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(LETV_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_BROADCAST,
             "com.letv.external.launch.channeldetail",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         self.cp.addExtras("iptvalbumid", self.j.get("iptvalbumid", 0), 4)
         self.cp.addExtras("vrsalbumid", self.j.get("vrsalbumid", 0), 4)
         self.cp.addExtras("channelcode", self.j.get("channelcode", ''), 1)
         self.cp.addFlags("FLAG_ACTIVITY_NEW_TASK")
         self.cp.addFlags("FLAG_INCLUDE_STOPPED_PACKAGES")
         return self.cp.convert()

class TENCENT_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(TENCENT_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_BROADCAST,
             "QQLIVETV.OPEN.INTENT.VOD.OPEN_VIDEO",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         j = {}
         #j['IntentD_Tencent.KEY_COVER_ID'] = self.j.get('coverId', '')
         #j['IntentD_Tencent.KEY_COVER_INDEX'] = self.j.get('index', '')
         j['QQLIVETV.OPEN.INTENT.VOD.KEY_COVER_ID'] = self.j.get('coverId', '')
         j['QQLIVETV.OPEN.INTENT.VOD.KEY_COVER_INDEX'] = self.j.get('index', '')
         self.cp.addExtras("cmdInfo", json.dumps(j), 1)
         self.cp.addFlags("FLAG_INCLUDE_STOPPED_PACKAGES")
         #self.cp.addFlags("FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET")
         return self.cp.convert()
         

class FENGHUANG_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(FENGHUANG_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_ACTIVITY,
             "com.ifeng.easyVideo.hisensetv.PLAYVIDEO_IFENG",
             params
             )
     def convert(self):
         if self.j is None:
             return self.cp.convert()
         self.cp.addExtras("postion", "${position_ms}", 2)
         self.cp.addExtras("subTitle", self.j.get("subTitle", ''), 1)
         self.cp.addExtras("video_id", self.j.get("video_id", ''), 1)
         resolution = self.j.get('episode_resolution', '')
         if len(resolution.strip()) == 0:
             resolution = "SD"
         self.cp.addExtras("episode_resolution", resolution, 1)
         #self.cp.addExtras("episode_resolution",
         #                  self.j.get('episode_resolution', ''), 1)
         self.cp.addExtras("video_name", self.j.get('video_name', ''), 1)
         self.cp.addExtras("ColumnId", self.j.get('ColumnId', ""), 1)
         self.cp.addExtras("isCollect", "${is_favorite}", 3)
         self.cp.addExtras("episode_action_url",
                           self.j.get('episode_action_url', ''), 1)
         self.cp.addExtras(Extras.PROGRAM_ID, "${program_id}", 1)
         self.cp.addExtras(Extras.EPISODE_ID, "${episode_id}", 1)
         return self.cp.convert()

class Rainbow_Convertor(CentralizedParamConvertor):
     def __init__(self, params):
         super(Rainbow_Convertor, self).__init__(
             CentralizedParams.STARTUP_TYPE_INNERPLAYER,
             "",
             params
             )     
         
class CentralizedParamFactry(object):
     vender_map = {1001:SOHU_Convertor,
                   1002:IQIYI_Convertor,
                   1003:KU6_Convertor,
                   1004:ICNTV_Convertor,
                   1005:LEKAN_Convertor,
                   1006:PPTV_Convertor,
                   1007:YOUKU_Convertor,
                   1008:YOUPENG_Convertor,
                   1009:LETV_Convertor,
                   1011:TENCENT_Convertor,
                   1012:FENGHUANG_Convertor,
                   1014:Rainbow_Convertor}
     def __init__(self, venderId, params):
         self.venderId = venderId
         self.params = params
     def convert(self):
         if not CentralizedParamFactry.vender_map.has_key(self.venderId):
             return ""
         CONVERTOR = CentralizedParamFactry.vender_map[self.venderId](self.params)
         return CONVERTOR.getStartupType(), CONVERTOR.convert()
    
