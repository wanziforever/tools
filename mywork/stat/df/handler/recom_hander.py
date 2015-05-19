#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound
from df.data_descriptor import DataDesc
from base_handler import db_handler
import json
import urllib2
from sqlalchemy.sql import func
from df.datamodel.schema import Basic_Media
        
def registerRequstHander():
    return "schema_recom", SCHEMA.schema_recom, recom_handler

HTTP_TIMEOUT = 2

class recom_handler(db_handler):
    def __init__(self, op, data_desc, session = None):
        super(recom_handler, self).__init__(op, data_desc, session)


    def get_recom_result(self, re_url):
        headers = {'User-Agent':'agent-vod'} 
        req = urllib2.Request(url=re_url, headers=headers)
        resp = urllib2.urlopen(req, None, HTTP_TIMEOUT)
        try:
            result = resp.read()
            result_json = json.loads(result)
            if not result_json:
                raise ValueError('recommend engine return nothing')
        except Exception, e:
            raise ValueError('error while request recommend engine'
                'with url %s,'%url,
                'with error %s'%str(e))
        return result_json        

    def get_max_search_index(self):
        result = [(-1, 0)]
        max_search = self.session.query(func.max(Basic_Media.search_index)).all()
        if max_search[0][0]:
            result = self.session.query(Basic_Media.id, Basic_Media.search_index).filter(Basic_Media.search_index == max_search[0][0]).all()
        return result

    def get_recom_result(self, re_url):
        headers = {'User-Agent':'agent-vod'} 
        req = urllib2.Request(url=re_url, headers=headers)
        resp = urllib2.urlopen(req, None, HTTP_TIMEOUT)
        try:
            result = resp.read()
            result_json = json.loads(result)
            if not result_json:
                raise ValueError('recommend engine return nothing')
        except Exception, e:
            raise ValueError('error while request recommend engine'
                'with url %s,'%url,
                'with error %s'%str(e))
        return result_json        

    def processQuery(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_all_by_home_recommend == data_type:
            re_url = self.data_desc.getKey(1)
            return self.get_recom_result(re_url)
        elif DATATYPE.data_type_all_max_search_index == data_type:
            return self.get_max_search_index()
        elif DATATYPE.data_type_all_by_home_recommend == data_type:
            re_url = self.data_desc.getKey(1)
            return self.get_recom_result(re_url)
