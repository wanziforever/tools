#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from ..datamodel.schema import media_collections
from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound
import df.data_function
from df.data_descriptor import DataDesc, InvalidKeyException
from core.settings import settings
from ..exceptions import NoSupportDataType

from base_handler import db_handler

def registerRequstHander():
    return "schema_media_collections_manage", SCHEMA.schema_media_collections_manage, media_collections_manage_handler

class media_collections_manage_handler(db_handler):
    def __init__(self,op, data_desc, session=None):
        super(media_collections_manage_handler, self).__init__(op, data_desc, session)

    def getCollect(self, collectId):
        collect = self.session.query(media_collections).\
                   filter(media_collections.collect_id == collectId).one()
        return collect

    def processUpdate(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_update_by_collect_id==data_type:
            collectId = self.data_desc.getKey(1)
            collectId2 = self.data_desc.getModifier("collect_id2")
            name = self.data_desc.getModifier("name")
            medias1 = self.data_desc.getModifier("medias1")
            medias2 = self.data_desc.getModifier("medias2")
            medias3 = self.data_desc.getModifier("medias3")
            try:
                strategy = self.getCollect(collectId)
            except NoResultFound, e:
                raise e
            
            self.session.query(media_collections).\
                         filter(media_collections.collect_id==collectId).\
                         update({"name":name,
                         	"collect_id":collectId2,
                         	"medias1":medias1,
                         	"medias2":medias2,
                         	"medias3":medias3})
            self.session.commit()

    def processDelete(self):
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_collect_id == data_type:
            try:
                collect_id = self.data_desc.getKey(1)
            except:
                print "userDevice_handler: id parameters is required for data_type_del_by_collect_id"
                raise InvalidKeyException("userDevice_handler", "id")
            try:
                self.session.query(media_collections).filter(media_collections.collect_id==collect_id).delete()
                self.session.commit()
            except NoResultFound:
                print "userDevice_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType


