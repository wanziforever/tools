#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound
import df.data_function
from base_handler import db_handler
from ..datamodel.schema import topic_category
from ..datamodel.schema import topic_info
from df.data_descriptor import DataDesc
from ..datamodel.schema import SCHEMA, DATATYPE
import json


def registerRequstHander():
    return "schema_topic_manage", SCHEMA.schema_topic_manage, topic_manage_handler


class topic_manage_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(topic_manage_handler, self).__init__(op, data_desc, session)

    def findMediasByStrategyId(self, id):
        result = self.session.query(topic_info).\
            filter(topic_info.strategy_id == id).one()
        return result

    def deleteTopicCategory(self, strategy_id):
        self.session.query(topic_category).filter(topic_category.strategy_id == strategy_id).delete()

    def deleteTopicInfo(self, strategy_id):
        self.session.query(topic_info).filter(topic_info.strategy_id == strategy_id).delete()

    def flushTopicListDesc(self):
        data_desc2 = DataDesc()
        data_desc2.setSchema(SCHEMA.schema_topic_category)
        data_desc2.setDataType(DATATYPE.data_type_query_all)
        data_desc2.setCached(True, 600)
        return data_desc2

    def flushTopicDetailpageDesc(self, strategy_id):
        data_desc2 = DataDesc()
        data_desc2.setSchema(SCHEMA.schema_topic_manage)
        data_desc2.setDataType(DATATYPE.data_type_query_topic_media_by_strategy)
        data_desc2.setKey(1, strategy_id)
        data_desc2.setCached(True, 600)
        return data_desc2

    def processInsert(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_save_topic == data_type:
            strategy_id = self.data_desc.getModifier("topicId")
            type_name = self.data_desc.getModifier("topicName")
            summary = self.data_desc.getModifier("topicDesc")
            provider_id = self.data_desc.getModifier("provider_id")
            pic1 = self.data_desc.getModifier("pic1")
            pic2 = self.data_desc.getModifier("pic2")
            pic3 = self.data_desc.getModifier("pic3")
            pic4 = self.data_desc.getModifier("pic4")
            pic5 = self.data_desc.getModifier("pic5")
            pic_link = "{\"pic1\":\""+pic1+"\",\"pic2\":\""+pic2+"\",\"pic3\":\""+pic3+"\",\"pic4\":\""+pic4+"\",\"pic5\":\""+pic5+"\"}"
            topic = topic_category()
            topic.strategy_id = strategy_id
            topic.type_name = type_name
            topic.summary = summary
            topic.pic_link = pic_link
            topic.online = 1
            topic.provider_id = provider_id
            self.session.add(topic)
            self.session.commit()

            data_desc2 = self.flushTopicListDesc()
            self.add_notify_descriptor(data_desc2, "reload")

    def processUpdate(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_update_name_by_topic_id == data_type:
            t = self.data_desc.getKey(1)
            # if isinstance(t["topicName"], unicode):
            #     topic_name = t["topicName"].encode('utf-8')
            pic1 = t["pic1"]
            pic2 = t["pic2"]
            pic3 = t["pic3"]
            pic4 = t["pic4"]
            pic5 = t["pic5"]
            pic_link = "{\"pic1\":\""+pic1+"\",\"pic2\":\""+pic2+"\",\"pic3\":\""+pic3+"\",\"pic4\":\""+pic4+"\",\"pic5\":\""+pic5+"\"}"
            self.session.query(topic_category).\
                filter(topic_category.strategy_id == t["old_strategy_id"]).\
                update({"strategy_id": t["topicId"], "type_name": t["topicName"], "pic_link": pic_link})
            #add update topic info id 
            self.session.query(topic_info).\
                filter(topic_info.strategy_id == t["old_strategy_id"]).\
                update({"strategy_id": t["topicId"]})

            self.session.commit()
            data_desc2 = self.flushTopicListDesc()
            self.add_notify_descriptor(data_desc2, "reload")
            data_desc3 = self.flushTopicDetailpageDesc(t["old_strategy_id"])
            self.add_notify_descriptor(data_desc3, "flush_cache")

        if DATATYPE.data_type_save_topic_media_info == data_type:
            strategy_id = self.data_desc.getKey(1)
            medias = self.data_desc.getModifier("details")
            background = self.data_desc.getModifier("background")
            figure = self.data_desc.getModifier("figure")
            character = self.data_desc.getModifier("character")
            music = self.data_desc.getModifier("music")
            pic_link = "{\"background\":\""+background+"\",\"figure\":\""+figure+"\",\"character\":\""+character+"\"}"
            
            try:
                topic = self.session.query(topic_info.medias).\
                    filter(topic_info.strategy_id == strategy_id).one()
            except NoResultFound:
                tinfo = topic_info()
                tinfo.strategy_id = strategy_id
                self.session.add(tinfo)
                self.session.commit()
                topic = self.session.query(topic_info.medias).\
                    filter(topic_info.strategy_id == strategy_id).one()

            topic1 = self.session.query(topic_info).\
                        filter(topic_info.strategy_id == strategy_id).\
                        update({"music_link": music})
            self.session.commit()

            topic2 = self.session.query(topic_info).\
                        filter(topic_info.strategy_id == strategy_id).\
                        update({"pic_link": pic_link})
            self.session.commit()

            topic = self.session.query(topic_info).\
                    filter(topic_info.strategy_id == strategy_id).\
                    update({"medias": medias})
            self.session.commit()

            data_desc2 = self.flushTopicDetailpageDesc(strategy_id)
            self.add_notify_descriptor(data_desc2, "reload")

    def processDelete(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_del_by_strategy_id == data_type:
            strategy_id = self.data_desc.getKey(1)
            try:
                self.deleteTopicCategory(strategy_id)
                self.deleteTopicInfo(strategy_id)
                self.session.commit()
            except NoResultFound:
                return None
            data_desc2 = self.flushTopicListDesc()
            data_desc3 = self.flushTopicDetailpageDesc(strategy_id)
            self.add_notify_descriptor(data_desc2, "reload")
            self.add_notify_descriptor(data_desc3, "flush_cache")