#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import time
import traceback
import urllib2

logger = logging.getLogger(__name__)

def get_content_by_url(url, is_retry=True, is_raise=False, time_out=3):
    logger.info(url)
    try:
        return urllib2.urlopen(url, timeout=time_out).read()
    except:
        if is_retry:
            time.sleep(1)
            try:
                return urllib2.urlopen(url, timeout=time_out).read()
            except:
                if is_raise:
                    raise
                else:
                    logger.error(url)
                    logger.error(traceback.format_exc())
        elif is_raise:
            raise
        else:
            logger.error(url)
            logger.error(traceback.format_exc())

def get_content_by_proxy(proxy, url, is_retry=True, is_raise=False, time_out=3):
    try:
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}))
        urllib2.install_opener(opener)
        return urllib2.urlopen(url, timeout=time_out).read()
    except:
        if is_retry:
            time.sleep(1)
            try:
                opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}))
                urllib2.install_opener(opener)
                return urllib2.urlopen(url, timeout=time_out).read()
            except:
                if is_raise:
                    raise
                else:
                    logger.error(url)
                    logger.error(traceback.format_exc())
        elif is_raise:
            raise
        else:
            logger.error(url)
            logger.error(traceback.format_exc())