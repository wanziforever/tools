#!/usr/bin/python
# -*- coding: utf-8 -*-
from basic_media_model_handler import basic_media_model_handler
from base_handler import request_handler
from common import t9
from core import solr
from df.datamodel.schema import DATATYPE, SCHEMA
import json
import re
import time
import types

def registerRequstHander():
    return "schema_search", SCHEMA.schema_search, search_handler

class search_handler(request_handler):
    def __init__(self, op, data_desc, session=None):
        super(search_handler, self).__init__(op, data_desc)

    def processQuery(self):
        data_type = self.data_desc.getDataType()
        request_param_dict = self.data_desc.getKey(1)
        search_type = request_param_dict.pop('type', '')
        start = request_param_dict.pop('start', '')
        rows = request_param_dict.pop('rows', '')
        fq = request_param_dict.pop('fq', '')
        sort = request_param_dict.pop('sort', '')
        fl = request_param_dict.pop('fl', '')
        m = re.compile('_online\':|_available\':|_deleted\':')
        words_relation = request_param_dict.pop('wordsRelation', '')
        if not m.search(str(request_param_dict)):
            default_fq = 'media_deleted:0 AND media_available:1 AND media_online:1 AND video_deleted:0 AND video_available:1 AND video_online:1 AND asset_deleted:0 AND asset_available:1 AND asset_online:1'
            if fq:
                fq = fq + ' AND ' + default_fq
            else:
                fq = default_fq
        result = None
        if DATATYPE.data_type_query_all == data_type or DATATYPE.data_type_for_console == data_type:
            result = self.get_result_by_field(request_param_dict, start, rows, fq, sort, fl, words_relation)
        elif DATATYPE.data_type_query_pinyin_cache == data_type or DATATYPE.data_type_query_pinyin == data_type:
            result = self.get_result_by_pinyin(request_param_dict, start, rows, fq, sort, words_relation)
        elif DATATYPE.data_type_query_t9 == data_type or DATATYPE.data_type_query_t9_cache == data_type:
            result = self.get_result_by_T9(request_param_dict, start, rows, fq, sort)
        return result

    def get_result_by_pinyin(self, search_key, start, rows, fq, sort, words_relation):
        if not sort:
            sort = 'title_length asc'
        pinyin = search_key.pop('search_key')
        q = 'media_acronym:*{acronym}*'.format(acronym=pinyin)
        if search_key:
            if words_relation == '1':
                q = q + ' OR ' + self.box_q(search_key, words_relation)
            else:
                q = q + ' AND ' + self.box_q(search_key, words_relation)
        return self.get_search_result(pinyin, q, start, rows, fq, sort)

    def get_result_by_T9(self, search_key, start, rows, fq, sort):
        if not sort:
            sort = 'title_length asc'
        t9keys = t9.get_cartesian_products_by_t9num(search_key.get('search_key'))
        if t9keys is not None:
            q = ' OR '.join(['media_acronym:*{acronym}*'.format(acronym = key) for key in t9keys])
            return self.get_search_result(t9keys, q, start, rows, fq, sort)
        return self.build_blank_result()
    
    def get_result_by_field(self, search_key, start, rows, fq, sort, fl, words_relation):
        q = self.box_q(search_key, words_relation)
        return self.get_search_result(None, q, start, rows, fq, sort, fl)
    
    def box_q(self, search_key, words_relation=None):
        qlist = []
        for k,v in search_key.items():
            if v.find('|^|') == -1:
                qlist.append(k + ':' + (v if re.compile('(^\[)(\S+)( TO )(\S+)(\]$)|(^\*\S+\*$)').match(v) else solr.escape_solr_word(v)))
            else:
                vlist = v.split('|^|')
                qlist.append('(' + ' OR '.join(['{key}:{value}'.format(
                            key=k, value=or_value if re.compile('(^\[)(\S+)( TO )(\S+)(\]$)|(^\*\S+\*$)').match(or_value)\
                            else solr.escape_solr_word(or_value)) for or_value in vlist]) + ')')
        if words_relation == '1':
            return ' OR '.join(qlist)
        return ' AND '.join(qlist)
    
    def get_result_by_t9_and_field(self, search_key, start, rows, fq, sort):
        if not sort:
            sort = 'title_length asc'
        t9keys = t9.get_cartesian_products_by_t9num(search_key.pop('t9'))
        q_acronym = ' OR '.join(['media_acronym:*{acronym}*'.format(acronym = key) for key in t9keys])
        q = '({acronym}) AND '.format(acronym = q_acronym)
        q = q + ' AND '.join(['{key}:{value}'.format(key=k, value=v) for (k, v) in search_key.items()])
        return self.get_search_result(t9keys, q, start, rows, fq, sort)
    
    def get_search_result(self, search_pinyin, q, start, rows, fq=None, sort=None, fl=None):
        if start != '' and rows != '':
            return self.parse_solr_result(search_pinyin, solr.get_search_result(\
                    'vod_media', q, start, rows, fq=fq, sort=sort, fl=fl), fl)
        else:
            return self.parse_solr_result(search_pinyin, solr.get_search_result(\
                    'vod_media', q, fq=fq, sort=sort, fl=fl), fl)
    
    def build_blank_result(self):
        result_dict = {}
        result_dict['total'] = 0
        result_dict['medias'] = []
        result_dict['ts'] = int(time.time())
        return result_dict
    
    def parse_solr_result(self, search_pinyin, result, fl):
        if result:
            json_result = json.loads(result)
            result_dict = {}
            result_dict['total'] = json_result['response']['numFound']
            medias = json_result['response']['docs']
            result_dict['medias'] = []
            if search_pinyin:
                result_dict['search_key'] = search_pinyin
                for index, media in enumerate(medias):
                    result_dict['medias'].append(self.box_media_dict(media, fl))
                    hl_index_dict = self.box_hl_index_dict(search_pinyin, media['media_acronym'])
                    result_dict['medias'][index]['hl_start_index'] = hl_index_dict['start']
                    result_dict['medias'][index]['hl_end_index'] = hl_index_dict['end']
            else:
                for media in medias:
                    result_dict['medias'].append(self.box_media_dict(media, fl))
            result_dict['ts'] = int(time.time())
            return result_dict
    
    def box_hl_index_dict(self, search_key, pinyin_list):
        if type(search_key) is types.ListType:
            for key in search_key:
                hl_index_dict = self.find_hl_index(pinyin_list, key)
                if hl_index_dict:
                    return hl_index_dict
        else:
            return self.find_hl_index(pinyin_list, search_key)
    
    def find_hl_index(self, pinyin_list, search_key):
        search_key = search_key.lower()
        hl_index_dict = {}
        for pinyin in pinyin_list:
            pinyin = pinyin.lower()
            if pinyin.find(search_key) > -1:
                hl_index_dict['start'] = pinyin.index(search_key)
                hl_index_dict['end'] = pinyin.index(search_key) + len(search_key)
                return hl_index_dict
    
    def box_media_dict(self, media, fl):
        media_dict = {}
        if fl:
            fields = fl.split(',')
            for field in fields:
                media_dict[field] = media.get(field, '')
        else:
            media_dict = basic_media_model_handler.convert_media(media)
        return media_dict
