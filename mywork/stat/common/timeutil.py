#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
time related utility
@author: Guojian Shao
"""
import datetime
import time
from common.errors import BadArgValueError


def strpmills(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.strptime(datetime_str, format)
    return long(time.mktime(dt.timetuple()))

def get_today_yesterday():
    now = time.gmtime()
    today = datetime.datetime(now[0], now[1], now[2])
    yesterday = today - datetime.timedelta(days=1)
    return today, yesterday