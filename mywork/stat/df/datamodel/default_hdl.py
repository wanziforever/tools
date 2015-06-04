#!/usr/bin/env python

# from sqlalchymy.orm.exc import NoResultFound
# from ..datamodel.schema import SCHEMA, DATATYPE

# class Basci_Video_handler(db_handler):
#     def __init__(self, op, params):
#         super(Basic_Video_handler, self).__init__(op, params)

#     def process(self, dat_type):
#         from ..datamode.schema import Vod_Basic_Video
#         if DATATYPE.data_type_query_by_id == data_type:
#             id = params["id"]
#             try:
#                 ret = self.session.query(Vod_Basic_Video).\
#                       filter(Vod_Basic_Video.id == id ).one()
#                 return ret
#             except NoResultFound:
#                 return None
#         else:
#             print "not support data type ", data_type
#             return None
