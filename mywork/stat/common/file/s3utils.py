#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
created on 1th,June by wujintao
'''

from __future__ import division
import logging
import os
import time
from common import settings
from common.error.errors import ResourceNotFoundError
from common.db import dbutils
from common.error.errors import S3OperateError

def getBucketNameByDeliveryType(deliveryType):
    for d in settings.deliveryMappers:
        if d['type'] == deliveryType:
            return d['bucket']
    return None

def getBucketNameByUrl(url):
    for d in settings.deliveryMappers:
        if url.lower().startswith(d['url'].lower()):
            return d['bucket']
    return None

def getUrlByDeliveryType(deliveryType):
    for d in settings.deliveryMappers:
        if d['type'] == deliveryType:
            return d['url']
    return None


def get_url(host,filekey):
    bucketname =  get_bucketname(filekey)
    return 'http://%s/%s/%s' % (host,bucketname,filekey)


def get_common(filekey,get_method):
    bucketname =  get_bucketname(filekey)
    return get_file(filekey,get_method,bucketname)



def get_file_common(bucket_name,s3_path,local_file,get_method):
    try:
        if s3_path == 'tmp':
            return False
        start = time.time()
        rep = get_method(bucket_name,s3_path,local_file)
        if rep:
            if rep.status != 200:
                if os.path.exists(local_file):
                    os.remove(local_file)
                logging.error('get file %s from s3 failed!' % s3_path)
                logging.error(u'error message: %s' % unicode(rep.read()))
                return False
        end = time.time()
        size = os.path.getsize(local_file)/1024/1024
        speed = size/(end-start)
        logging.info('get file %s from s3 successfully!filename:%s ,filesize:%sMB ,cost time:%ss ,speed is %s MB/S' % (s3_path,local_file,size,str(end-start),speed))
        return True
    except:
        if os.path.exists(local_file):
            os.remove(local_file)
        logging.info('get file %s from s3 failed!' % s3_path)
        return False
    

def put_common(local_file,put_method):
    if os.path.exists(local_file):
        bucket_name =  get_bucketname(local_file)
        s3_relative_path = local_file[(len(settings.FILESTORE_DIR)+1):]
        res = put_method(bucket_name,s3_relative_path,local_file)        
    else:
        logging.info('local file %s not exists,can not put to s3' % local_file)
        raise S3OperateError('local file %s not exists,can not put to s3' % local_file,None)
    
def put_file_common(bucket_name,s3_path,local_file,put_method, try_times = 5):
    start = time.time() * 1000
    times = 0
    size = os.path.getsize(local_file)/1024/1024

    while times < try_times:
        try:
            resp = put_method(bucket_name, s3_path, local_file)
            end = time.time() * 1000
            
            if resp and int(resp.status) == 200:
                speed = size/(end-start)
                logging.info('successfully put %s to %s, take %d, speed %dk' % (local_file, s3_path, (end - start), speed))
                return 
            else:
                logging.exception('%dth put %s to %s failed!, message [%s]' % (times, local_file, s3_path, resp.read()))
        except:
            logging.exception('%dth put %s to %s failed' % (times, local_file, s3_path))
        times = times + 1
    
    logging.error('retry %d times, fail to put %s to %s' % (times, local_file, s3_path))

def get_vodieo(filekey,get_method):
    return get_file(filekey,get_method,settings.S3_VOD_BUCKET)    
    

def getVideo(video_id,local_file,get_method):
    kernel_db =  dbutils.KERNEL_DB
    video = list(kernel_db.select('Video',where="id = $id ", vars = {'id':video_id}))
    if video:
        logging.info('videoid: %s ,get video from s3 base on videoid' % video_id)
        s3_path = video[0].videoKey
        local_path = os.path.join(settings.FILESTORE_DIR, s3_path)
        if os.path.exists(local_path):
            copy_file(local_path,local_file)
        else:
            get_file(s3_path,get_method,settings.S3_VOD_BUCKET)

    else:
        logging.info('videoid: %s , video not exists,can get from s3' % video_id)
        raise S3OperateError('videoid: %s , video not exists,can get from s3' % video_id,None)
    


def validateMode():
    mode = settings.DISTRIBUTION_MODE
    if mode and (mode == 'aliyun' or mode == 'huaweiyun'):
        return True
    else:
        return False


def get_bucketname(filekey):
    bucketname = None
    if (filekey.endswith('.ts') or filekey.endswith('.m3u8')):
        bucketname = settings.S3_IOS_BUCKET
        
    elif(('uploaded-asset' in filekey) or ('snapshot' in filekey) or ('player' in filekey) or ('.xml' in filekey) or ('.jpg' in filekey)):
        bucketname = settings.S3_STATIC_BUCKET
        
    elif(('uploaded-video' in filekey) or filekey.endswith('.mp4') or filekey.endswith('.flv') or ('uploaded-audio' in filekey)) or filekey.endswith('.mp3') or filekey.endswith('.acc'):    
        bucketname = settings.S3_VOD_BUCKET
    
    else:
        bucketname = settings.S3_LIVE_BUCKET
    
    return bucketname

def get_file(filekey,method,video_bucket_name):
    path = os.path.join(settings.FILESTORE_DIR, filekey)
    create_dir(path)
    
        
    if isnot(path,3600):
        if  not os.path.exists(path):
            if(create_pid(filekey,path,method,video_bucket_name)):
                return path
            else:
                return get_file(filekey,method,video_bucket_name)    
        else:
            #logging.info('file:  %s is already exists,use it ......' % path)
            return path
    else:
        #这里什么都不应该返回，直接抛出异常
        
        raise ResourceNotFoundError('S3 GET FILE FAILED', path)
    

def del_pid(path):
    piddir = path+'.pid'
    os.rmdir(piddir)



def create_dir(file):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except Exception,e:
            pass               


def create_pid(filekey,path,download_s3file_to_local,bucket_name):
    piddir = path+'.pid'
    try:
        #logging.info('create piddir %s' % piddir)
        os.mkdir(piddir)
        base_name =  os.path.basename(piddir)
        if base_name == '.pid':
            del_pid(path)
            return True
        
        logging.info('create piddir %s succesful' % piddir)
        flag = download_s3file_to_local(bucket_name,filekey,path)
        if flag:
            kernel_db =  dbutils.KERNEL_DB
            id_generator = dbutils.IdGenerator(0)
            publishers = list(kernel_db.query('select * from Deletefile where name=\'%s\'' % path))
            if not publishers:
                try:
                    kernel_db.insert('Deletefile',id=id_generator.get_next_id(),name=path,creationTime=time.time(),modifiedTime=time.time())
                except:
                    logging.info('insert table Deletefile failed, name:%s' % path)
            else:
                try:
                    kernel_db.update('Deletefile',where="name = $name", vars = {'name':path},modifiedTime=time.time())
                except:
                    logging.info('update table Deletefile failed, name:%s' % path)    
    
        #logging.info('delete piddir %s' % piddir)
        del_pid(path)
        return True
    except Exception, e:
        # delete pid dir to prevent from distribution hanging
        if os.path.exists(path):
            del_pid(path)
        #logging.info('create piddir %s fail,once again......' % piddir)
        return False
        
    return False    

    

def isnot(path,deadline):
    piddir = path+'.pid'
    if deadline==0:
        #logging.info('deadline leave:%s ,deadline is arrival,error' % deadline)
        return False
    
    if(os.path.exists(piddir)):
        #logging.info('oh no!!!! someone using ! piddir %s is already exists,please wait......' % piddir)
        #logging.info('deadline leave:%s ,go on......' % deadline)
        time.sleep(15)
        deadline = deadline-15
        return isnot(path,deadline)
    else:
        #logging.info('piddir %s is not exists......' % piddir)
        return True 

def copy_file(src_path,dest_path):
    dest_file = open(dest_path,'wb')
    with open(src_path,'rb') as file:
        while True:
            content = file.read()
            if not content:
                break
            dest_file.write(content,)
        dest_file.close()