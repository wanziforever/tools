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
from common.dbutil import slice_query
import time
import json
import logging


logger = logging.getLogger('frontpage_api')

def registerRequstHander():
    return "schema_video_manage", SCHEMA.schema_video_manage, video_manage_handler


class video_manage_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(video_manage_handler, self).__init__(op, data_desc, session)


    def time_length_convert(self, time_length):
        result = None
        if time_length:
            h = int(time_length[0:2])
            m = int(time_length[3:5])
            s = int(time_length[6:8])
            result = h * 3600 + m * 60 + s
        return result

    def compareMedia(self, media, details):
        flag = False
        for key in details:
            former = eval("media."+ str(key)).encode('utf-8') if isinstance(eval("media."+ str(key)), unicode) else eval("media."+ str(key))
            if str(details.get(key)) != str(former):
                flag = True
                break
        return flag

    def getBasicMedia(self, id):
        media = self.session.query(Basic_Media).\
                                filter(Basic_Media.id == id).one()
        return media

    def getAssetList(self, ref_id, type):
        asset_list = self.session.query(Basic_Asset).\
                                filter(Basic_Asset.ref_id == ref_id).\
                                filter(Basic_Asset.type == type).all()
        return asset_list

    def getCategoryList(self, media_id):
        category_list = self.session.query(Basic_Media_Category_Rel).\
                                    filter(Basic_Media_Category_Rel.media_id == media_id).all()
        return category_list

    def getEntertainerList(self, media_id, type):
        entertainer_list = self.session.query(Basic_Media_Entertainer_Rel).\
                                        filter(Basic_Media_Entertainer_Rel.media_id == media_id).\
                                        filter(Basic_Media_Entertainer_Rel.type == type).all()
        return entertainer_list

    def getAssetByMediaId(self,mediaId):
        asset = self.session.query(Basic_Asset).filter(Basic_Asset.ref_id == mediaId).filter(Basic_Asset.type == 0).one()
        return asset

    def getCategoryId(self, caList):
        categoryList = self.session.query(Basic_Category.id, Basic_Category.name).filter(*caList).all()
        return categoryList

    def getVenderId(self, type, videoId):
        assetList = self.session.query(Basic_Asset).\
            filter(Basic_Asset.ref_id == videoId, Basic_Asset.type == type).all()
        return assetList

    def getCategory(self, type):
        if type == 0:
            categoryList = self.session.query(Basic_Category.id, Basic_Category.name).\
                filter(Basic_Category.parent_id == None).all()
        else:
            categoryList = self.session.query(Basic_Category.id, Basic_Category.name).\
                filter(Basic_Category.parent_id != None).all()
        return categoryList

    def getVenderList(self, mediaId):
        find = []
        find.append(Basic_Video.media_id == mediaId)
        find.append(Basic_Video.id == Basic_Video_Entertainer_Rel.video_id)
        find.append(Basic_Video_Entertainer_Rel.entertainer_id == Basic_Entertainer.id)
        venderList = self.session.query(Basic_Entertainer.stagename).filter(*find).all()
        return venderList

    def getEnterByMediaId(self, type, mediaId):
        enterIdList = self.session.query(Basic_Media_Entertainer_Rel.entertainer_id).\
            filter(Basic_Media_Entertainer_Rel.media_id == mediaId).filter(Basic_Media_Entertainer_Rel.type == type).all()
        return enterIdList

    def getEntersById(self, enterIdList):
        enters = []
        for enter in enterIdList:
            enters.append(enter[0])
        result = self.session.query(Basic_Entertainer.stagename).\
            filter(Basic_Entertainer.id.in_(enters)).all()
        return result

    def  convertPubdate(self, pubdate):
        import datetime
        if pubdate:
            t =time.strptime(pubdate, '%Y')
            d = datetime.datetime(* t[:6])
        else:
            d = None
        return d

    def update_basic_entertainer(self, media_id, update_names, type) :
        entertainer = None
        need_ids = []
        for name in update_names:
           try:
               entertainer = self.session.query(Basic_Entertainer).\
                                  filter(Basic_Entertainer.stagename == name).one()
           except NoResultFound:
                logger.info("==Basic_Entertainer   update==")
                entertainer1 = Basic_Entertainer(stagename=name)
                self.session.add(entertainer1)
                self.session.commit()
                entertainer = self.session.query(Basic_Entertainer).\
                                  filter(Basic_Entertainer.stagename == name).one()
           finally:
               need_ids.append(entertainer.id)
        entertainer_list = self.getEntertainerList(media_id, type)
        exist_ids = []
        for en in entertainer_list:
           exist_ids.append(en.entertainer_id)
           if en.entertainer_id in need_ids and en.deleted == 1 and en.type == type:
               logger.info("==Basic_Entertainer   update==")
               self.session.query(Basic_Media_Entertainer_Rel).\
                   filter(Basic_Media_Entertainer_Rel.id == en.id).\
                   update({'deleted': 0})
           if en.entertainer_id not in need_ids and en.deleted == 0 and en.type == type:
               logger.info("==Basic_Entertainer   update==")
               self.session.query(Basic_Media_Entertainer_Rel).\
                   filter(Basic_Media_Entertainer_Rel.id == en.id).\
                   update({'deleted': 1})
        add_ids = list(set(need_ids).difference(set(exist_ids)))
        for id in add_ids:
            logger.info("==Basic_Entertainer   update==")
            entertainer_rel = Basic_Media_Entertainer_Rel(media_id=media_id,
                                     entertainer_id=id, type=type)
            self.session.add(entertainer_rel)

    def get_all_update_medias(self, start, limit, cntv):
        if cntv:
            q = self.session.query(medias_update_record).\
                   filter(medias_update_record.onoff_vender == 'cntv').\
                   order_by(medias_update_record.modified_time.desc())
        else:
            q = self.session.query(medias_update_record).\
                   order_by(medias_update_record.modified_time.desc())
        return slice_query(q, start, limit).all()

    def get_all_update_count(self):
        return self.session.query(medias_update_record).count()


    def processQuery(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_query_by_media_id == data_type:
            mediaId = self.data_desc.getKey(1)
            type = self.data_desc.getKey(2)
            caList = []
            caList.append(Basic_Media_Category_Rel.media_id == mediaId)
            caList.append(Basic_Media_Category_Rel.category_id == Basic_Category.id)
            if type == 0:
                caList.append(Basic_Category.parent_id == None)
            if type == 1:
                caList.append(Basic_Category.parent_id != None)
            try:
                return self.getCategoryId(caList)
            except NoResultFound:
                return None
        if DATATYPE.data_type_query_by_video_id == data_type:
            type = self.data_desc.getKey(1)
            videoId = self.data_desc.getKey(2)
            try:
                return self.getVenderId(type, videoId)
            except NoResultFound:
                return None
        if DATATYPE.data_type_by_type_media_id == data_type:
            mediaId = self.data_desc.getKey(1)
            type = self.data_desc.getKey(2)
            try:
                enterIdList2 = self.getEnterByMediaId(type, mediaId)
                enters = self.getEntersById(enterIdList2)
                return enters
            except NoResultFound:
                return None
        if DATATYPE.data_type_query_pararent_category == data_type:
            type = self.data_desc.getKey(1)
            try:
                categoryList = self.getCategory(type)
                return categoryList
            except NoResultFound:
                return None
        if DATATYPE.data_type_all_vidio_venders == data_type:
            mediaId = self.data_desc.getKey(1)
            try:
                venderList = self.getVenderList(mediaId)
                return venderList
            except NoResultFound:
                return None

        if DATATYPE.data_type_query_all_vender_list == data_type:
            try:
                return self.session.query(Basic_Vender).order_by(Basic_Vender.level.desc()).all()
            except NoResultFound:
                return None

        if DATATYPE.data_type_query_media_by_online == data_type:
            type = self.data_desc.getKey(1)
            mediaId = self.data_desc.getKey(2)
            online = self.data_desc.getKey(3)
            try:
                return self.session.query(Basic_Asset).\
                            filter(Basic_Asset.ref_id == mediaId).\
                            filter(Basic_Asset.type == type).\
                            filter(Basic_Asset.online == online).all()
            except NoResultFound:
                return None

        if DATATYPE.data_type_query_all == data_type:
            start = int(self.data_desc.getKey(1))
            limit = int(self.data_desc.getKey(2))
            cntv = self.data_desc.getKey(3)
            medias = self.get_all_update_medias(start, limit, cntv)
            result = {}
            result["count"] = self.get_all_update_count()
            result["rows"] = medias
            return result

    def processUpdate(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_update_basic_media == data_type:
            details = self.data_desc.getModifier("details")
            id = details.get('id')
            try:
                media = self.getBasicMedia(id)
            except NoResultFound, e:
                raise e
            if self.compareMedia(media, details):
                logger.info("==Basic_Media   update==")
                self.session.query(Basic_Media).\
                     filter(Basic_Media.id == id).\
                     update(details)

        if DATATYPE.data_type_update_basic_asset == data_type:
            ref_id = self.data_desc.getKey(1)
            shield = self.data_desc.getModifier('shield')
            asset_list = self.getAssetList(ref_id, 0)      #0 is media
            shield_vender_ids = [int(i) for i in shield.split(',')] if shield else []
            for asset in asset_list:
                if asset.vender_id in shield_vender_ids and asset.online == 1:
                    logger.info("==Basic_Asset   update==")
                    self.session.query(Basic_Asset).\
                        filter(Basic_Asset.id == asset.id).\
                        update({'online': 0})
                if asset.vender_id not in shield_vender_ids and asset.online == 0:
                    logger.info("==Basic_Asset   update==")
                    self.session.query(Basic_Asset).\
                        filter(Basic_Asset.id == asset.id).\
                        update({'online': 1})

        if DATATYPE.data_type_update_basic_category == data_type:
            media_id = self.data_desc.getKey(1)
            category_id = self.data_desc.getModifier('category_id')
            child_category_ids = self.data_desc.getModifier('child_category_ids')
            category_list = self.getCategoryList(media_id)
            need_ids = []
            for ca in category_id.split(','):
                need_ids.append(int(ca))
            need_ids = need_ids + ([int(i) for i in child_category_ids.split(',')] if child_category_ids else [])
            exist_ids = []
            for category in category_list:
                exist_ids.append(category.category_id)
                if category.category_id in need_ids and category.deleted == 1:
                    logger.info("==Basic_Category   update==")
                    self.session.query(Basic_Media_Category_Rel).\
                        filter(Basic_Media_Category_Rel.id == category.id).\
                        update({'deleted': 0})
                if category.category_id not in need_ids and category.deleted == 0:
                    logger.info("==Basic_Category   update==")
                    self.session.query(Basic_Media_Category_Rel).\
                        filter(Basic_Media_Category_Rel.id == category.id).\
                        update({'deleted': 1})
            add_ids = list(set(need_ids).difference(set(exist_ids)))
            for id in add_ids:
                logger.info("==Basic_Category   update==")
                category_rel = Basic_Media_Category_Rel(media_id=media_id,
                                          category_id=id)
                self.session.add(category_rel)
                
        if DATATYPE.data_type_update_basic_entertainer == data_type:
            media_id = self.data_desc.getKey(1)
            directors = self.data_desc.getModifier('directors')
            actors = self.data_desc.getModifier('actors')
            update_actor_names =  actors.split(',') if actors else []
            update_director_names =  directors.split(',') if directors else []
            self.update_basic_entertainer(media_id, update_actor_names, 0)    #0 is actor
            self.update_basic_entertainer(media_id, update_director_names, 1)    #1 is director
            
        self.session.commit() 