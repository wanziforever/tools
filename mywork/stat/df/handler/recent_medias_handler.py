#!/usr/bin/env python

from ..datamodel.schema import Basic_Media
from ..datamodel.schema import SCHEMA, DATATYPE
from base_handler import db_handler
from sqlalchemy import desc


import logging

logger = logging.getLogger('RecentMediasHandler')

def registerRequstHander():
    return "schema_recent_medias", SCHEMA.schema_recent_medias, RecentMediasHandler


class RecentMediasHandler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(RecentMediasHandler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        data_type = self.data_desc.getDataType()
        logger.debug("processQuery with data_type[%s]" % data_type)
        if DATATYPE.data_type_query_by_time == data_type:
            ts = self.data_desc.getKey(1)
            query = self.session.query(Basic_Media.id).\
                filter(Basic_Media.modified_time > ts).order_by(desc(Basic_Media.modified_time))
            rows_limit = self.data_desc.getKey(2)
            if rows_limit:
                query = query.limit(rows_limit)    
            medias = query.all()
            logger.debug("count of got medias %d " % len(medias))
            return medias