#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound

from base_handler import db_handler
from df.datamodel.schema import video_startup, Basic_Category

def registerRequstHander():
    return "schema_basicvideo", SCHEMA.schema_video_startup_manage, video_startup_manage_handler

class video_startup_manage_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(video_startup_manage_handler, self).__init__(op, data_desc, session)

    def getCategoryId(self, caList):
        categoryList = self.session.query(Basic_Category.id, Basic_Category.name).filter(*caList).all()
        return categoryList

    def processUpdate(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_update_video_startup == data_type:
            provider_id = self.data_desc.getKey(1)
            startup_type = self.data_desc.getModifier("startupType")
            params = self.data_desc.getModifier("details")
            details = "{\"details\":" + str(params) + "}"
        try:
            startup = self.session.query(video_startup).\
                filter(video_startup.provider_id == provider_id).one()
        except NoResultFound:
            startup = video_startup()
            startup.provider_id = provider_id
            startup.startup_type = startup_type
            startup.params = details
            self.session.add(startup)
            self.session.commit()
            return None

        self.session.query(video_startup).\
            filter(video_startup.provider_id == provider_id).\
            update({"params": details, "startup_type": startup_type})
        self.session.commit()
