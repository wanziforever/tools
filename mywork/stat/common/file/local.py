#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
created on 1th,June by wujintao
'''
from __future__ import division
import logging
from common.db import dbutils
from common import settings
import os
import time

'''
local do nothing
'''
def put(local_file):
    pass

def putByDeliveryType(local_file, delivery_type):
    pass

'''
local do nothing
'''
def get(filekey):
    return os.path.join(settings.FILESTORE_DIR, filekey)


    
def getVideo(video_id,dest_path):
    kernel_db =  dbutils.KERNEL_DB
    video = list(kernel_db.select('Video',where="id = $id ", vars = {'id':video_id}))
    src_path = None
    if video:
        start = time.time()
        src_path = os.path.join(settings.FILESTORE_DIR, video[0].videoKey)
        size = os.path.getsize(src_path)/1024/1024
        logging.info('videoid: %s ,get video from local path:%s base on videoid' % (video_id,src_path))
        try:
            _copy_file(src_path,dest_path)
            end = time.time()
            speed = size/(end-start)
            logging.info('success get video:%s ,filesize:%sMB, cost time:%ss, the speed is %smb/s' %(src_path,size,str(end-start),speed))
        except:
            logging.info('failed get video:%s ' % src_path)
    else:
        logging.info('videoid: %s , video not exists,can get from local path:%s' % (video_id,src_path))
  
def _copy_file(src_path,dest_path):
    dest_file = open(dest_path,'wb')
    with open(src_path,'rb') as file:
        while True:
            content = file.read()
            if not content:
                break
            dest_file.write(content,)
        dest_file.close()

if __name__ == '__main__':
     _copy_file('/srv/upload/rendition.flv','/srv/222222')               