#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from common import httputil
from settings import settings
from urllib import quote

def get_search_result(core_name,
                      query_condition,
                      start=0,
                      rows=10,
                      wt='json',
                      sort=None,
                      fl=None,
                      fq=None):
    url = 'http://{solr_ip}:{solr_port}/sse/{core_value}/select?q={q_value}&rows={rows_value}&start={start_value}&wt={wt_value}'\
          .format(
                solr_ip = settings.SOLR_IP,
                solr_port = settings.SOLR_PORT, 
                core_value = core_name,
                q_value = quote(query_condition),
                rows_value = rows,
                start_value = start,
                wt_value = wt)
    if fl:
        url = url + '&fl=' + quote(fl)
    if fq:
        url = url + '&fq=' + quote(fq) 
    if sort:
        url = url + '&sort=' + quote(sort)
    return httputil.get_content_by_url(url, is_raise=True)

def escape_solr_word(word):
    return re.sub('(\\\|\+|-|&|\|\||!|\(|\)|\{|}|\[|]|\^|"|~|\*|\?|:|;|/|\~)', lambda m: '\\' + m.group(0), word)

def update_solr_field(core_name, key_name, key_value, field_dict):
    list_fields = []
    not_list_fields = []
    for k, v in field_dict.items():
        if isinstance(v, list):
            list_fields.append((k, v))
        else:
            not_list_fields.append((k, v))
    base_body = '<add><doc><field name="%s">%s</field>%s</doc></add>'
    not_list_fields_body = ''
    list_fields_body = ''
    if not_list_fields:
        not_list_fields_content = ''.join(['<field name="%s" update="set">%s</field>' % (item[0], item[1]) for item in not_list_fields])
        not_list_fields_body = base_body % (key_name, key_value, not_list_fields_content)
    if list_fields:
        for item in list_fields:
            item_list_fields_content = '<field name="%s" update="set">%s</field>' % (item[0], item[1][0])
            item_list_fields_body = base_body % (key_name, key_value, item_list_fields_content)
            for i in range(1, len(item[1])):
                item_list_fields_content = '<field name="%s" update="add">%s</field>' % (item[0], item[1][i])
                item_list_fields_body = item_list_fields_body + base_body % (key_name, key_value, item_list_fields_content)
            list_fields_body += item_list_fields_body
    url = 'http://{solr_ip}:{solr_port}/sse/{core_value}/update?wt=json&stream.body=%3Cupdate%3E{body}%3C/update%3E'\
          .format(solr_ip = settings.SOLR_IP,
                solr_port = settings.SOLR_PORT,
                core_value = core_name,
                body = quote(not_list_fields_body + list_fields_body))
    return httputil.get_content_by_url(url, is_raise=True, time_out=20)
