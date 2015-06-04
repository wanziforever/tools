#!/usr/bin/env python

from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound

from base_handler import db_handler
from df.datamodel.schema import Basic_UserCollect, Basic_UserHistory, \
    user_center_layout, Basic_Video, DATATYPE
import time
import datetime


def registerRequstHander():
    return "schema_usercenter", SCHEMA.schema_usercenter, usercenter_handler


def cloneAttribute(o, d):
    for key in d.keys():
            setattr(o, key, d[key])


class usercenter_handler(db_handler):
    def __init__(self, op, data_desc, session = None):
        super(usercenter_handler, self).__init__(op, data_desc, session)

    def processCount(self):
        dataType = self.data_desc.getDataType()
        if dataType in (DATATYPE.data_type_usercenter_favorite,
                        DATATYPE.data_type_usercenter_query_favorite_index,
                    DATATYPE.data_type_usercenter_query_favorite_byuidtype):
            return self.session.query(Basic_UserCollect).\
                    filter_by(**self.data_desc.keys).count()
        if dataType == DATATYPE.data_type_usercenter_query_favorite_newvideo:
            today = int(time.mktime(datetime.date.today().timetuple()))
            mediaId = self.data_desc.getKey("media_id")
            query = self.session.query(Basic_Video).\
                    filter(Basic_Video.media_id == mediaId,
                           Basic_Video.modified_time > today,
                           Basic_Video.deleted == 0,
                           Basic_Video.online == 1,
                           Basic_Video.available == 1)
            return query.count()

    def processQuery(self):
        dataType = self.data_desc.getDataType()
        if dataType in (DATATYPE.data_type_usercenter_favorite,
                        DATATYPE.data_type_usercenter_query_favorite_index,
                    DATATYPE.data_type_usercenter_query_favorite_byuidtype):
            query = self.session.query(Basic_UserCollect)
            query = query.filter_by(**self.data_desc.keys)
            query = query.order_by(Basic_UserCollect.modified_time.desc())
            if self.data_desc.page[1] != 0:
                query = query.limit(self.data_desc.page[1])
            if self.data_desc.page[0] != 0:
                query = query.offset(self.data_desc.page[0])
            return query.all()

        elif dataType in (
            DATATYPE.data_type_usercenter_query_updatedvideos_by_mediaids,):

            mediaIds = self.data_desc.getKey("media_ids")
            today = int(time.mktime(datetime.date.today().timetuple()))
            query = self.session.query(Basic_Video).\
                    filter(Basic_Video.media_id.in_(mediaIds),
                           Basic_Video.modified_time > today,
                           Basic_Video.deleted == 0,
                           Basic_Video.online == 1,
                           Basic_Video.available == 1)
            query = query.order_by(Basic_Video.modified_time.desc())

            return query.all()

        elif dataType in (DATATYPE.data_type_usercenter_history,
                          DATATYPE.data_type_usercenter_query_history,
                          DATATYPE.data_type_usercenter_query_history_index):
            query = self.session.query(Basic_UserHistory).\
                        filter_by(**self.data_desc.keys)
            query = query.order_by(Basic_UserHistory.modified_time.desc())
            if self.data_desc.page[1] != 0:
                query = query.limit(self.data_desc.page[1])
            if self.data_desc.page[0] != 0:
                query = query.offset(self.data_desc.page[0])

            history = query.all()
            return history
        elif dataType in (DATATYPE.data_type_usercenter_query_layout,):

            query = self.session.query(user_center_layout)
            layout = query.all()
            return layout

        else:
            raise Exception("not supported data type" + dataType)

    def processUpdate(self):
        dataType = self.data_desc.getDataType()
        if DATATYPE.data_type_usercenter_history == dataType:
            updater = dict({"modified_time": long(time.time())},
                           **self.data_desc.modifier)
            self.session.query(Basic_UserHistory).\
                        filter_by(**self.data_desc.keys).\
                        update(updater)
            self.session.commit()
        else:
            raise Exception("not supported data type" + dataType)

    def processDelete(self):
        dataType = self.data_desc.getDataType()
        if DATATYPE.data_type_usercenter_favorite == dataType:
            userid = self.data_desc.getModifier("user_id")
            mediaid = self.data_desc.getModifier("media_id")
            self.session.query(Basic_UserCollect).\
                        filter_by(user_id = userid, media_id = mediaid).\
                        delete()
            self.session.commit()

        elif DATATYPE.data_type_usercenter_history == dataType:
            userid = self.data_desc.getKey("user_id")
            self.session.query(Basic_UserHistory).\
                        filter_by(user_id = userid).\
                        delete()
            self.session.commit()
        else:
            raise Exception("not supported data type" + dataType)

    def processInsert(self):
        dataType = self.data_desc.getDataType()
        myObject = None
        if DATATYPE.data_type_usercenter_favorite == dataType:
            myObject = Basic_UserCollect()
        elif DATATYPE.data_type_usercenter_history == dataType:
            myObject = Basic_UserHistory()
        elif DATATYPE.data_type_usercenter_layout == dataType:
            myObject = user_center_layout()
        else:
            raise Exception("not supported data type" + dataType)

        cloneAttribute(myObject, self.data_desc.modifier)

        self.session.add(myObject)
        self.session.commit()
