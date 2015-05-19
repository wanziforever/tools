#!/usr/bin/env python

from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound

from base_handler import db_handler
from df.datamodel.schema import area_apps


def registerRequstHander():
    return "schema_areapps", SCHEMA.schema_areapps, areapps_handler


class areapps_handler(db_handler):
    def __init__(self, op, data_desc, session = None):
        super(areapps_handler, self).__init__(op, data_desc, session)

    def getAllApps(self):
        allApps = self.session.query(area_apps).all()
        return allApps

    def processQuery(self):
        data_type = self.data_desc.getDataType()
        #print "areapps_handler::processQuery with data_type ", data_type
        if DATATYPE.data_type_query_all == data_type:
            try:
                return self.getAllApps()
            except NoResultFound:
                return None
        else:
            print "areapps_handler::processQuery does not support data_type ", data_type

    def processUpdate(self):
        appId = self.data_desc.getKey("id")
        self.session.query(area_apps).filter_by(id = appId).\
                                      update(self.data_desc.modifier)
        self.session.commit()

    def processDelete(self):
        appId = self.data_desc.getKey("id")
        self.session.query(area_apps).filter_by(id = appId).delete()
        self.session.commit()

    def processInsert(self):
        appNew = area_apps()
        for key in self.data_desc.modifier.keys():
            setattr(appNew, key, self.data_desc.getModifier(key))
        self.session.add(appNew)
