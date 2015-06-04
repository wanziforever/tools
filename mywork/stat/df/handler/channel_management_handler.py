#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound

from base_handler import db_handler
from df.datamodel.schema import Basic_Media_Category_Rel
from df.datamodel.schema import Basic_Asset
from df.datamodel.schema import Basic_Category
from df.datamodel.schema import Basic_Video
from df.datamodel.schema import Basic_Media_Entertainer_Rel
from df.datamodel.schema import Basic_Video_Entertainer_Rel
from df.datamodel.schema import Basic_Media
from df.datamodel.schema import Basic_Entertainer
from df.datamodel.schema import Basic_Vender
from df.datamodel.schema import medias_update_record
from df.datamodel.schema import channel
from df.datamodel.schema import channel_info
from common.dbutil import slice_query
from sqlalchemy.sql import func
from sqlalchemy.sql import or_
from sqlalchemy import distinct
import time
import json
import logging
import df.data_function
from df.data_descriptor import DataDesc


logger = logging.getLogger('frontpage_api')

def registerRequstHander():
    return "schema_channel_management", SCHEMA.schema_channel_management, channel_management_handler


class channel_management_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(channel_management_handler, self).__init__(op, data_desc, session)


    def time_length_convert(self, time_length):
        result = None
        if time_length:
            h = int(time_length[0:2])
            m = int(time_length[3:5])
            s = int(time_length[6:8])
            result = h * 3600 + m * 60 + s
        return result

    def get_online_video_vender(self, video_id, media_id):
        video_venders = self.session.query(Basic_Asset.vender_id).\
                filter(Basic_Video.id == video_id).filter(Basic_Video.online == 1).\
                filter(Basic_Video.deleted == 0).filter(Basic_Video.available == 1).\
                filter(Basic_Asset.ref_id == video_id).filter(Basic_Asset.deleted == 0).\
                filter(Basic_Asset.online == 1).filter(Basic_Asset.available == 1).\
                filter(Basic_Asset.type == 1).all()
        result = []
        for v in video_venders:
            result.append(v[0])
        media_venders = self.get_online_venders(media_id)
        return list(set(result) & set(media_venders))

    def get_play_bills(self, channel_id, date):
        now_list = self.session.query(channel_info)\
                   .filter(channel_info.channel_id == channel_id)\
                   .filter(channel_info.date == date)\
                   .filter(channel_info.video_id != 0)\
                   .order_by(channel_info.start_stamp).all()
        last_list = self.session.query(channel_info)\
                   .filter(channel_info.channel_id == channel_id)\
                   .filter(channel_info.date == (date - 1))\
                   .filter(channel_info.video_id != 0)\
                   .order_by(channel_info.start_stamp.desc())\
                   .limit(1).all()
        return last_list +  now_list, len(last_list)
    
    def get_online_venders(self, media_id):
        media_venders = self.session.query(Basic_Asset.vender_id)\
            .filter(Basic_Media.id == media_id).filter(Basic_Media.online == 1)\
            .filter(Basic_Media.deleted == 0).filter(Basic_Media.available == 1)\
            .filter(Basic_Asset.ref_id == media_id).filter(Basic_Asset.deleted == 0)\
            .filter(Basic_Asset.online == 1).filter(Basic_Asset.available == 1)\
            .filter(Basic_Asset.type == 0).filter(Basic_Asset.vender_id == Basic_Vender.id)\
            .filter(Basic_Vender.deleted==0).filter(Basic_Vender.online == 1).all()
        online_venders = []
        for v in media_venders:
            online_venders.append(v[0])
        return online_venders if online_venders else [-1]
        
    def fill_video(self, media_id, video_id):
        result = {}
        result['videos'] = []
        online_venders = self.get_online_venders(media_id)
        q = self.session.query(Basic_Video.id,Basic_Video.title,Basic_Asset.vender_id,\
                  Basic_Asset.video_play_url,Basic_Vender.name,Basic_Asset.video_quality,\
                  Basic_Video.time_length,Basic_Asset.fee,Basic_Video.series,Basic_Asset.video_play_param)\
                  .filter(Basic_Video.id == video_id).filter(Basic_Video.id == Basic_Asset.ref_id)\
                  .filter(Basic_Asset.vender_id == Basic_Vender.id).filter(Basic_Video.online == 1)\
                  .filter(Basic_Video.deleted == 0).filter(Basic_Asset.online == 1)\
                  .filter(Basic_Asset.deleted == 0).filter(Basic_Asset.available == 1)\
                  .filter(Basic_Video.available == 1).filter(Basic_Asset.type == 1)\
                  .filter(Basic_Vender.id.in_(online_venders))
        video_asset_list = q.order_by(Basic_Vender.level.asc()).order_by(Basic_Asset.video_quality.desc()).all()
        vedeo_id_sort_list = []
        for asset in video_asset_list:
            play_way = {}
            play_way['id'] = asset[2]
            play_way['name'] = asset[4]
            play_way['fee'] = asset[7] if asset[7] else 0
            play_way['video_play_url'] = asset[3]
            play_way['video_play_param'] = asset[9]
            play_way['video_quality'] = asset[5]
        try:
            index = vedeo_id_sort_list.index(str(asset[0]))
            media_dict['videos'][index]['play_ways'].append(play_way)
        except ValueError:
            video = {}
            video['id'] = str(asset[0])
            video['title'] = asset[1]
            video['time_length'] = asset[6] if asset[6] else -1
            video['series'] = str(asset[8]) if asset[8] else ''
            video['play_ways'] = []
            video['play_ways'].append(play_way)
            result['videos'].append(video)
            vedeo_id_sort_list.append(str(asset[0]))
        return result

    def get_medias_id(self, video_id):
        media = self.session.query(Basic_Video.media_id)\
                .filter(Basic_Video.id == video_id).all()
        media_id = -1
        if len(media) > 0:
            media_id = media[0][0]
        return media_id

    def all_record_by_channel(self, channel_id):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.video_id == 0).order_by(channel_info.record_num).all()

    def get_start_time(self, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.video_id != 0).\
                    filter(channel_info.record_num < record_num).\
                    order_by(channel_info.start_stamp.desc()).\
                    all()                    

    def get_channel_videos(self, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.record_num == record_num).\
                    filter(channel_info.program_id != 0).all()

    def get_less_videos(self, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.video_id != 0).\
                    filter(channel_info.record_num < record_num).\
                    order_by(channel_info.start_stamp.desc()).all()

    def get_greater_videos(self, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.record_num > record_num).\
                    order_by(channel_info.start_stamp).all()

    def get_exists_record(self, program_id, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.program_id == program_id).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.record_num != record_num).all()

    def get_channel_info(self, channel_id):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.video_id != 0).\
                    order_by(channel_info.start_stamp.desc()).all()

    def get_all_channel_records(self, channel_id):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).all()
    
    def get_record_num_start_stamp(self, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.record_num == record_num).\
                    filter(channel_info.program_id == 0).all()

    def get_limit_one_record(self, channel_id, record_num):
        return self.session.query(channel_info).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.record_num < record_num).\
                    filter(channel_info.video_id != 0).\
                    order_by(channel_info.start_stamp.desc()).limit(1).all()

    def add_channel_info(self, details, channel_id, record_num):
        for video in details:
            date = video['start_time'][0: 10]
            dt = time.strptime(date, "%Y-%m-%d")
            day = (int(time.mktime(dt)) - time.timezone)/(60*60*24)
            time_array = time.strptime(video["start_time"], "%Y-%m-%d %H:%M:%S")
            time_stamp = int(time.mktime(time_array)) - 8 * 60 * 60
            time_length = video["time_length"]
            ch_info = channel_info(channel_id=channel_id,program_id=video["program_id"],
                                        video_id=video["video_id"],title=video["title"],
                                        start_time=video["start_time"],start_stamp=time_stamp,
                                        date=day,vender_id=video["vender_id"],
                                        time_length=video["time_length"],record_num=record_num)
            self.session.add(ch_info)

    def add_update_record(self, channel_id, start_stamp, start_time, record_num):
            ch_info = channel_info(channel_id=channel_id,program_id=0,
                                   video_id=0,title='',
                                   start_time=start_time,start_stamp=start_stamp,
                                   date=0,vender_id=0,
                                   time_length=0,record_num=record_num)
            self.session.add(ch_info)       

    def update_record_start_time(self, record_num, channel_id, details):
        start_time = details[0]['start_time']
        dt = time.strptime(start_time[0: 10], "%Y-%m-%d")
        day = (int(time.mktime(dt)) - time.timezone)/(60*60*24)
        time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_array)) - 8 * 60 * 60
        self.session.query(channel_info).\
                    filter(channel_info.record_num == record_num).\
                    filter(channel_info.channel_id == channel_id).\
                    filter(channel_info.video_id == 0).\
                    update({"start_time": start_time, "start_stamp": time_stamp,
                             "date": day})

    def update_greater_videos(self, gt_videos, diff_time):
        for video in gt_videos:
            start_stamp = video.start_stamp - diff_time
            timeArray = time.localtime(start_stamp + 8 * 60 * 60)
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            date = start_time[0: 10]
            dt = time.strptime(date, "%Y-%m-%d")
            day = (int(time.mktime(dt)) - time.timezone)/(60*60*24)
            self.session.query(channel_info).\
                        filter(channel_info.id == video.id).\
                        update({"start_time": start_time,"start_stamp": start_stamp,
                                       "date": day})

    def delete_channel_by_id(self, channel_id):
        self.session.query(channel).\
                filter(channel.channel_id == channel_id).delete()

    def delete_channel_info_by_id(self, channel_id):
        self.session.query(channel_info).\
                filter(channel_info.channel_id == channel_id).delete()

    def delete_now_record(self, channel_id, record_num):
        self.session.query(channel_info).\
                filter(channel_info.channel_id == channel_id).\
                filter(channel_info.record_num == record_num).delete()

    def delete_now_record_videos(self, channel_id, record_num):
        self.session.query(channel_info).\
                filter(channel_info.channel_id == channel_id).\
                filter(channel_info.record_num == record_num).\
                filter(channel_info.program_id != 0).delete()

    def flush_channel_detailpage(self, channel_id): 
        day_list = self.session.query(distinct(channel_info.date)).\
                filter(channel_info.channel_id == channel_id).all()
        for date in day_list:
            data_desc = DataDesc(SCHEMA.schema_channel_management,
                            DATATYPE.data_type_query_play_bills)
            data_desc.setKey(1, channel_id)
            data_desc.setKey(2, int(date[0]))
            self.add_notify_descriptor(data_desc, "reload")

    def flush_channel_list(self):
        data_desc = DataDesc(SCHEMA.schema_channel,
                        DATATYPE.data_type_query_all)
        self.add_notify_descriptor(data_desc, "reload")

    def flush_channel_video(self, program_id, channel_id):
        data_desc = DataDesc(SCHEMA.schema_Basic_Media_model,
                         DATATYPE.get_channel_video_detail)
        data_desc.setKey(1, program_id)
        data_desc.setKey(2, channel_id)
        self.add_notify_descriptor(data_desc, "reload")


    def processQuery(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_query_video_online == data_type:
            video_id = int(self.data_desc.getKey(1))
            media_id = int(self.data_desc.getKey(2))
            return self.get_online_video_vender(video_id, media_id)
        elif DATATYPE.data_type_all_record_by_channel== data_type:
            channel_id = self.data_desc.getKey(1)
            return self.all_record_by_channel(channel_id)
        elif DATATYPE.data_type_all_start_time== data_type:
            channel_id = self.data_desc.getKey(1)
            record_num = self.data_desc.getKey(2)
            return self.get_start_time(channel_id, record_num)
        elif DATATYPE.data_type_all_query_channel_videos == data_type:
            channel_id = self.data_desc.getKey(1)
            record_num = self.data_desc.getKey(2)
            return self.get_channel_videos(channel_id, record_num)
        elif DATATYPE.data_type_query_channel_info == data_type:
            channel_id = self.data_desc.getKey(1)
            return self.get_channel_info(channel_id)        
        elif DATATYPE.data_type_judege_program_id == data_type:
            channel_id = self.data_desc.getKey(1)
            record_num = self.data_desc.getKey(2)
            details = self.data_desc.getKey(3)
            for ve in details:
                pr_exists = self.get_exists_record(ve["program_id"], channel_id, record_num)
                if len(pr_exists) > 0:
                    return pr_exists[0].program_id
        elif DATATYPE.data_type_query_play_bills == data_type:
            channel_id = self.data_desc.getKey(1)
            date = self.data_desc.getKey(2)
            program_list, last_len = self.get_play_bills(channel_id, date)
            result = []
            for now in program_list:
                program = {}
                program["start_stamp"] = now.start_stamp
                program["title"] = now.title
                program["time_length"] = now.time_length
                program["start_time"] = now.start_time
                program["channel_id"] = now.channel_id
                program["program_id"] = now.program_id
                program["vender_id"] = now.vender_id
                program["play_time"] = 0
                program["play_ways"] = []
                program["is_show"] = 1
                result.append(program)
            return result, last_len

    def processUpdate(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_update_program == data_type:
            channel_id = self.data_desc.getModifier("channel_id")
            record_num = self.data_desc.getModifier("record_num")
            details = self.data_desc.getModifier("details")
            self.delete_now_record_videos(channel_id, record_num)
            for video in details:
                date = video['start_time'][0: 10]
                dt = time.strptime(date, "%Y-%m-%d")
                day = (int(time.mktime(dt)) - time.timezone)/(60*60*24)
                time_array = time.strptime(video["start_time"], "%Y-%m-%d %H:%M:%S")
                time_stamp = int(time.mktime(time_array)) - 8 * 60 * 60
                time_length = video["time_length"]
                ch_info = channel_info(channel_id=channel_id,program_id=video["program_id"],
                                            video_id=video["video_id"],title=video["title"],
                                            start_time=video["start_time"],start_stamp=time_stamp,
                                            date=day,vender_id=video["vender_id"],
                                            time_length=video["time_length"],record_num=record_num)
                self.session.add(ch_info)
            self.update_record_start_time(record_num, channel_id, details)
            gt_videos = self.get_greater_videos(channel_id, record_num) 
            if len(gt_videos) > 0:
                diff_time = gt_videos[0].start_stamp - (time_stamp + time_length)
                self.update_greater_videos(gt_videos, diff_time)

            self.session.commit()
            self.flush_channel_detailpage(channel_id)
            for video in details:
                self.flush_channel_video(video["program_id"], channel_id)

        elif DATATYPE.data_type_update_record == data_type:
            channel_id = self.data_desc.getModifier("channel_id")
            record_num = self.data_desc.getModifier("record_num")
            start_stamp = 0
            start_time = '0000-00-00 00:00:00'
            time_list = self.get_limit_one_record(channel_id, record_num)
            if len(time_list) > 0 and time_list[0].start_stamp != 0:
                start_stamp = time_list[0].start_stamp + 8 * 60 * 60 + time_list[0].time_length
                timeArray = time.localtime(start_stamp)
                start_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            self.add_update_record(channel_id, start_stamp, start_time, record_num)
            
            self.session.commit()

    def processDelete(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_delete_record == data_type:
            channel_id = self.data_desc.getKey(1)
            record_num = self.data_desc.getKey(2)
            self.delete_now_record(channel_id, record_num)
            le_videos = self.get_less_videos(channel_id, record_num)
            gt_videos = self.get_greater_videos(channel_id, record_num)
            if len(le_videos) > 0 and len(gt_videos) > 0:
                diff_time = gt_videos[0].start_stamp - le_videos[0].start_stamp - le_videos[0].time_length
                self.update_greater_videos(gt_videos, diff_time)

            self.session.commit()
            self.flush_channel_detailpage(channel_id)
        elif DATATYPE.data_type_delete_channel_by_id == data_type:
            channel_id = self.data_desc.getKey(1)
            self.delete_channel_by_id(channel_id)
            self.delete_channel_info_by_id(channel_id)

            self.session.commit()
            self.flush_channel_list()
            
            
