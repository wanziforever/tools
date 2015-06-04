#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2011-10-23

@author: mengchen
'''
import doctest
import time

def datetime2timestamp(dt):
    '''
    >>> import datetime
    >>> datetime2timestamp(datetime.datetime(2000, 1, 1))
    946656000000L
    '''
    return long(time.mktime(dt.timetuple()) * 1000)

def sleep_until(time):
    pass

def timestamp():
    return long(time.time() * 1000)

def wait_until(max_time, check_interval, evaluate):
    elapsed = 0
    rslt = None
    while elapsed <= max_time:
        rslt = evaluate()
        if rslt:
            return rslt
        time.sleep(check_interval)
        elapsed += check_interval
    return rslt

if __name__ == '__main__':
    doctest.testmod()
    