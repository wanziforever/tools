#!/usr/bin/python
# -*- coding: utf-8 -*-
from ..datamodel.schema import Basic_Video, Basic_Asset, Basic_Vender, channel_info,\
    DATATYPE,SCHEMA
from base_handler import db_handler
from centralized_params import CentralizedParamFactry
from core import solr
import json
import logging
logger = logging.getLogger('BasicMediaHandler')


def registerRequstHander():
    return "schema_Basic_Media_model", SCHEMA.schema_Basic_Media_model, basic_media_model_handler


class basic_media_model_handler(db_handler):
    default_fq = 'media_deleted:0 AND media_available:1 AND media_online:1 AND video_deleted:0 AND video_available:1 AND video_online:1 AND asset_deleted:0 AND asset_available:1 AND asset_online:1'
    def __init__(self,op, data_desc, session=None):
        super(basic_media_model_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.get_detail_page_model == data_type:
            return self.get_detail_page_model()
        elif DATATYPE.get_latest_media_model == data_type:
            return self.get_latest_videos()
        elif DATATYPE.get_list_page_model == data_type:
            return self.get_list_page_model()
        elif DATATYPE.get_media_by_ids == data_type:
            return self.get_media_by_ids()
        elif DATATYPE.get_channel_video_detail == data_type:
            return self.get_channel_video_detail()

    def get_latest_videos(self):
        start_time = self.data_desc.getKey('start_time')
        start = self.data_desc.getKey('start')
        rows = self.data_desc.getKey('rows')
        query_condition = 'modified_time:[%d TO *]' % start_time
        try:
            query_condition = (query_condition + 
                ' AND category_id:%s'%self.data_desc.getKey('category_id') )
        except :
            pass 
        logger.debug('get_latest_videos, start_time:%d, start:%d, rows:%d' % (start_time, start, rows))
        search_result = json.loads(solr.get_search_result(core_name='vod_media',
                                                          query_condition=query_condition,
                                                          start=start,
                                                          rows=rows,
                                                          fq=self.default_fq,
                                                          sort='modified_time desc'))
        return basic_media_model_handler.assembly_search_result(search_result)

    @staticmethod
    def assembly_search_result(search_result):
        total = int(search_result['response']['numFound'])
        medias = [basic_media_model_handler.convert_media(x) for x in search_result['response']['docs']]
        return dict(total=total, medias=medias)

    @staticmethod
    def get_update_mark(search_media):
        total = search_media.get('total', 0)
        current = search_media.get('current', 0)
        category_ids = search_media.get('category_id', [])
        for category_id in category_ids:
            if category_id == 1001 or category_id == 1005:
                if total == current and total != 0:
                    return str(current) + '集全'
                elif current != 0:
                    return '更新到第' + str(current) + '集'
            elif category_id == 1002:
                if current != 0:
                    return '更新到' + str(current) + '期'
        return ''
    
    @staticmethod
    def get_time_length(search_media):
        video_id_list = search_media.get('video_id', [])
        is_series = search_media.get('is_series', '')
        if len(video_id_list) == 1 and not is_series:
            time_length_list = search_media.get('video_time_length', [])
            if time_length_list and time_length_list[0]:
                return time_length_list[0]
        return -1
            
    @staticmethod
    def convert_media(search_media):
        media_id = search_media['media_id']
        title = search_media.get('title', '')
        is_new = search_media['is_new']
        current = search_media.get('current', -1)
        category_ids = search_media.get('category_id')
        category_id = -1
        if category_ids:
            category_id = category_ids[0]
        is_clip = search_media.get('is_clip', 0)
        de_list = search_media.get('definition', '').split(';')
        de_result = []
        for de in de_list:
            de_result.extend(de.split(','))
        definition = max(de_result)
        update_mark = basic_media_model_handler.get_update_mark(search_media)
        image_icon_url = basic_media_model_handler.get_icon_url(search_media)
        time_length = basic_media_model_handler.get_time_length(search_media)
        return dict(id=media_id, title=title, is_new=is_new, current=current,
                    category_id=category_id, image_icon_url=image_icon_url,
                    update_mark=update_mark, time_length=time_length,
                    is_clip=is_clip, definition = definition)

    @staticmethod
    def get_icon_url(search_media):
        for k in ('image_icon_url', 'asset_image_icon_url'):
            if k in search_media:
                return search_media[k]
        logger.debug("can't find image icon url for media[%s]" % search_media['media_id'])
        return ''
        
    def get_media_by_ids(self):
        media_ids = self.data_desc.getKey("media_ids")
        conditions = 'media_id:(' + ' '.join([str(x) for x in media_ids]) + ')'

        logger.debug('get_media_by_ids:media_ids:%s' % conditions)
        search_result = json.loads(solr.get_search_result('vod_media',
                                   conditions, rows=len(media_ids), fq=self.default_fq))
        return basic_media_model_handler.assembly_search_result(search_result)

    def get_list_page_model(self):
        media_id = self.data_desc.getKey(1)
        json_result = json.loads(solr.get_search_result('vod_media', 'media_id:' + str(media_id), fq=self.default_fq))
        medias = json_result['response']['docs']
        if len(medias) > 0:
            return basic_media_model_handler.convert_media(medias[0])
        return None

    def get_online_venders(self, media):
        vender_list = media.get('vender_id', [])
        available_list = media.get('asset_available', [])
        online_list = media.get('asset_online', [])
        online_venders = []
        for index in range(len(vender_list)):
            if available_list[index] and online_list[index]:
                online_venders.append(vender_list[index])
        return online_venders if online_venders else [-1]

    def get_channel_video_detail(self):
        program_id = self.data_desc.getKey(1)
        channel_id = self.data_desc.getKey(2)
        pr_list = self.get_video_by_program_id(program_id, channel_id)
        video_id = pr_list[0].video_id if len(pr_list) > 0 else 0
        media_id = self.get_medias_id(video_id)
        json_result = json.loads(solr.get_search_result('vod_media', 'media_id:' + str(media_id), fq=self.default_fq))
        medias = json_result['response']['docs']
        if len(medias) > 0 :
            media = medias[0]
            video_dict = {}
            self.fill_videos(video_dict, media, video_id, pr_list)
            if video_dict is None:
                return None
            self.convertCentralizedPlayerParams(video_dict)
            # self.check_and_convert_phonix_to_ku6(media_dict)
            # self.check_and_convert_rainbow_to_ku6(media_dict)
            return video_dict

        return None

    def get_detail_page_model(self):
        media_id = self.data_desc.getKey(1)
        json_result = json.loads(solr.get_search_result('vod_media', 'media_id:' + str(media_id), fq=self.default_fq))
        medias = json_result['response']['docs']
        if len(medias) > 0 :
            media = medias[0]
            media_dict = {}
            media_dict['id'] = media.get('media_id')
            media_dict['title'] = media.get('title', '')
            media_dict['summary'] = media.get('summary', '')
            media_dict['definition'] = media.get('definition', '')
            media_dict['pubdate'] = media.get('pubdate', '')
            media_dict['rate'] = str(media.get('rate', ''))
            media_dict['total'] = media.get('total', -1)
            media_dict['current'] = media.get('current', -1)
            media_dict['default_play_source'] = media.get('default_play_source', -1)
            media_dict['country'] = media.get('country', '')
            media_dict['language'] = media.get('language', '')
            media_dict['category'] = '|'.join(media.get('category_name', []))
            media_dict['child_category'] = media.get('child_category_name', [])
            media_dict['director'] = media.get('director_name', [])
            media_dict['director_id_list'] = media.get('director_id', [])
            media_dict['actor'] = media.get('actor_name', [])
            media_dict['actor_id_list'] = media.get('actor_id', [])
            media_dict['image_post_url'] = media['image_post_url'] if media.get('image_post_url', '') else media.get('asset_image_post_url', '')
            media_dict['image_icon_url'] = media['image_icon_url'] if media.get('image_icon_url', '') else media.get('asset_image_icon_url', '')
            media_dict['image_rec_url'] = media.get('image_rec_url', '')
            media_dict['is_new'] = media.get('is_new')
            media_dict['is_series'] = media.get('is_series', '')
            media_dict['is_collected'] = media.get('is_collected', '')
            media_dict['is_clip'] = media.get('is_clip', 0)
            category_id = -1
            category_ids = media.get('category_id', [])
            if category_ids:
                category_id = category_ids[0]
            media_dict['category_id'] = category_id
            if 1001 in category_ids and media_dict['total'] != -1 and media_dict['total'] < media_dict['current']:
                media_dict['total'] = -1
            self.fill_videos(media_dict, media)
            if media_dict is None:
                return None
            self.convertCentralizedPlayerParams(media_dict)
            # self.check_and_convert_phonix_to_ku6(media_dict)
            # self.check_and_convert_rainbow_to_ku6(media_dict)
            return media_dict

        return None

    def fill_videos(self, mv_dict, media, video_id=None, pr_list=None):
        mv_dict['videos'] = []
        online_venders = self.get_online_venders(media)
        q = self.get_query_sql(mv_dict, video_id, online_venders)
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
                mv_dict['videos'][index]['play_ways'].append(play_way)
            except ValueError:
                video = {}
                video['id'] = str(asset[0])
                if pr_list and len(pr_list) > 0:
                    video['title'] = pr_list[0].title
                    video['time_length'] = pr_list[0].time_length
                else:
                    video['title'] = asset[1]
                    video['time_length'] = asset[6] if asset[6] else -1
                video['series'] = str(asset[8]) if asset[8] else ''
                video['play_ways'] = []
                video['play_ways'].append(play_way)
                mv_dict['videos'].append(video)
                vedeo_id_sort_list.append(str(asset[0]))
    
    def concat_all_persons(self, person_list, seporator):
        persons = ''
        for person in person_list:
            persons = persons + seporator + person.stagename
        if persons != '':
            return persons[len(seporator):]
        return ''

    def get_medias_id(self, video_id):
        media = self.session.query(Basic_Video.media_id)\
                .filter(Basic_Video.id == video_id).all()
        media_id = 0
        if len(media) > 0:
            media_id = media[0][0]
        return media_id

    def convertCentralizedPlayerParams(self, media):
        ''' convert the player param to new centralized params
        add the following field to play_ways '''
        if not media.has_key('videos'):
            return
        videos = media['videos']
        for v in videos:
            ways = v['play_ways']
            for w in ways:
                try:
                    startup_type, params_str = (
                        CentralizedParamFactry(w['id'], w['video_play_param']).convert()
                        )
                except:
                    import traceback
                    traceback.print_exc()
                    startup_type, params_str = 1, None
                w['centralized_play_params'] = params_str
                w['startup_type'] = startup_type

    def check_and_convert_phonix_to_ku6(self, media):
        ''' a workaround way to convert the phonix video to ku6 format,
        and play the video with ku6 player'''
        if not media.has_key('videos'):
            return
        videos = media['videos']
        miss_counter = 0
        
        from centralized_params import CentralizedParams
        for v in videos:
            # for performance issue, for a media who has a lot of videos
            # the checking will be waste of CPU resource, so just check
            # every videos, if meet continuas 3 vidoes who do not need
            # to conver, just break out
            if miss_counter > 2:
                break
                
            ways = v['play_ways']
            found = False
            for w in ways:
                if w['id'] != 1012:
                    continue
                found = True
                old_param = w['video_play_param']
                old_j = json.loads(old_param)
                new_j = {}
                new_j['subTitle'] = old_j['subTitle']
                new_j['title'] = old_j['subTitle']
                new_j['url'] = old_j['episode_action_url']
                new_j['program_id'] = old_j['program_id']
                new_j['episode_id'] = old_j['episode_id']
                new_j['isCollect'] = '${isCollect}'
                new_j['position'] = '${history}'
                new_j['resolution'] = old_j['episode_resolution']
                old_video = w['video_play_url']
                new_video = new_j['url']
                w['video_play_param'] = json.dumps(new_j)
                w['video_play_url'] = new_video
                w['id'] = 1003
                w['name'] = '酷6'
                w['centralized_play_params'] = CentralizedParams().convert()
                if w.has_key('startup_type'):
                    w['startup_type'] = CentralizedParams.STARTUP_TYPE_INNERPLAYER
    
            if found is True:
                miss_counter = 0
            else:
                miss_counter += 1
    
    def check_and_convert_rainbow_to_ku6(self, media):
        ''' a workaround way to convert the rainbow to ku6 format,
        since the rainbox already has ku6 format by the aggreation,
        only vender id convert is need for this convertion'''
        if not media.has_key('videos'):
            return
        videos = media['videos']
        miss_counter = 0
    
        from centralized_params import CentralizedParams
        for v in videos:
            # for performance issue, for a media who has a lot of videos
            # the checking will be waste of CPU resource, so just check
            # every videos, if meet continuas 3 vidoes who do not need
            # to conver, just break out
            if miss_counter > 2:
                break
                
            ways = v['play_ways']
            found = False
            for w in ways:
                if w['id'] != 1014: # 1014 is the vender id for rainbow
                    continue
                found = True
                w['id'] = 1003
                w['name'] = '酷6'
                w['centralized_play_params'] = CentralizedParams().convert()
                if w.has_key('startup_type'):
                    w['startup_type'] = CentralizedParams.STARTUP_TYPE_INNERPLAYER
    
            if found is True:
                miss_counter = 0
            else:
                miss_counter += 1

    def get_video_by_program_id(self, program_id, channel_id):
        return self.session.query(channel_info).filter(channel_info.program_id == program_id).\
                              filter(channel_info.channel_id == channel_id).all()

    def get_query_sql(self, mv_dict, video_id, online_venders):
        if video_id:
            q = self.session.query(Basic_Video.id,Basic_Video.title,Basic_Asset.vender_id,\
                  Basic_Asset.video_play_url,Basic_Vender.name,Basic_Asset.video_quality,\
                  Basic_Video.time_length,Basic_Asset.fee,Basic_Video.series,Basic_Asset.video_play_param)\
                  .filter(Basic_Video.id == video_id).filter(Basic_Video.id == Basic_Asset.ref_id)\
                  .filter(Basic_Asset.vender_id == Basic_Vender.id).filter(Basic_Video.online == 1)\
                  .filter(Basic_Video.deleted == 0).filter(Basic_Asset.online == 1)\
                  .filter(Basic_Asset.deleted == 0).filter(Basic_Asset.available == 1)\
                  .filter(Basic_Video.available == 1).filter(Basic_Asset.type == 1)\
                  .filter(Basic_Vender.id.in_(online_venders))
        else:
            q = self.session.query(Basic_Video.id,Basic_Video.title,Basic_Asset.vender_id,\
                     Basic_Asset.video_play_url,Basic_Vender.name,Basic_Asset.video_quality,\
                     Basic_Video.time_length,Basic_Asset.fee,Basic_Video.series,Basic_Asset.video_play_param)\
                     .filter(Basic_Video.id==Basic_Asset.ref_id).filter(Basic_Asset.vender_id==Basic_Vender.id)\
                     .filter(Basic_Video.online==1).filter(Basic_Video.deleted==0).filter(Basic_Asset.online==1)\
                     .filter(Basic_Asset.deleted==0).filter(Basic_Vender.deleted==0).filter(Basic_Video.media_id==mv_dict['id'])\
                     .filter(Basic_Asset.available==1).filter(Basic_Video.available==1).filter(Basic_Asset.type==1)\
                     .filter(Basic_Vender.online==1).filter(Basic_Vender.id.in_(online_venders))   
            if mv_dict['category_id'] in [1002,1009,1010,1014,1016,1017]:
                q = q.order_by(Basic_Video.series.desc()).order_by(Basic_Video.pubdate.desc())
            else:
                q = q.order_by(Basic_Video.series.asc()).order_by(Basic_Video.pubdate.asc())
        return q
