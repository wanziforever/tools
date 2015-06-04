##!/usr/bin/env python
## -*- coding: utf-8 -*-
#'''
#created on 1th,June by wujintao
#'''
#from common.file.store import s3
#import logging
#
#def init_logging(log_file):
#    logger = logging.getLogger()
#    handler = logging.FileHandler(log_file)
#    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#    handler.setFormatter(formatter)
#    logger.addHandler(handler)
#    logger.setLevel(logging.INFO)
#
#def test_put(local_file):
#    s3.put(local_file)
#    
#
#def test_get(filekey):
#    s3.get(filekey)    
#
#def test_get_url(filekey):
#    return  s3.get_url(filekey)  
#  
#if __name__ == '__main__':
#    pass
##    init_logging('/var/log/s3.log')
##    test_put('/srv/upload/snapshot/jintao/11.jpg')
##    test_put('/srv/upload/snapshot/jintao/22.jpg')
##    test_put('/srv/upload/snapshot/jintao/jintao.jpg')
##    test_put('/srv/upload/rendition/jintao/jintao.mp4')
##    test_put('/srv/upload/uploaded-video/jintao/jintao')
##    test_put('/srv/upload/uploaded-asset/jintao/jintao.ts')
#
#    test_get('snapshot/jintao/11.jpg')
#    test_get('snapshot/jintao/22.jpg')        
#    test_get('snapshot/jintao/jintao.jpg')
#    test_get('rendition/jintao/jintao.mp4')
#    test_get('uploaded-video/jintao/jintao')
#    test_get('uploaded-asset/jintao/jintao.ts') 
##    print test_get_url('snapshot/jintao/11.jpg')
##    print test_get_url('snapshot/jintao/22.jpg')    
##    print test_get_url('snapshot/jintao/jintao.jpg')
##    print test_get_url('rendition/jintao/jintao.mp4')  
##    print test_get_url('uploaded-video/jintao/jintao')  
##    print test_get_url('uploaded-asset/jintao/jintao.ts')      