#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
created on 1th,June by wujintao
'''
from common import settings
from common.error.errors import BadArgValueError
from oss_api import *
from oss_util import GetAllObjects
import s3utils
import logging
from common.error.errors import S3OperateError
import urlparse

host = settings.ALIYUN_S3_HOST
access_id = settings.ALIYUN_S3_ACCESSED_ID
secret_access_key = settings.ALIYUN_S3_SECRECT_ACCESS_KEY


oss = OssAPI(host, access_id, secret_access_key)

'''
put local file to s3
param:just local file absolute  path
'''
def put(local_file):
    s3utils.put_common(local_file,put_file)

'''
deliver local file to s3 by deliveryType
'''
def putByDeliveryType(local_file, delivery_type):
    if os.path.exists(local_file):
        bucket_name =  s3utils.getBucketNameByDeliveryType(delivery_type)
        s3_relative_path = local_file[(len(settings.FILESTORE_DIR)+1):]
        put_file(bucket_name,s3_relative_path,local_file)
        return urlparse.urljoin(s3utils.getUrlByDeliveryType(delivery_type), s3_relative_path)
    else:
        logging.info('local file %s not exists,can not put to s3' % local_file)
        raise S3OperateError('local file %s not exists,can not put to s3' % local_file,None)

def put_common(bucket_name, s3_path, local_file): 
    return oss.put_object_from_file(bucket_name, s3_path, local_file)

'''
put local file to s3,must pass in a buketname,local file,the path of s3
''' 
def put_file(bucket_name,s3_path,local_file):
    s3utils.put_file_common(bucket_name,s3_path,local_file,put_common)


'''
# old version of get function, implemented by jintaowu
def get(filekey):
    return s3utils.get_common(filekey,get_file)
'''
'''
get any file from s3 to local by filekey and bucketname
'''
def get(filekey):
    guessed_bucketname =  s3utils.get_bucketname(filekey)
    try:
        return s3utils.get_file(filekey,get_file,guessed_bucketname)
    except:
        logging.info('failed to get file {0} from bucket {1}'.format(filekey, guessed_bucketname))
        bucketnames = [ d['bucket'] for d in settings.deliveryMappers if d['bucket'] != guessed_bucketname ]
        for bucketname in bucketnames:
            logging.info('try to get file from bucket %s' % bucketname)
            try:
                return s3utils.get_file(filekey,get_file,bucketname)
            except:
                logging.info('failed to get file {0} from bucket {1}'.format(filekey, bucketname))
        logging.warn('failed to get file {0} from all buckets, give up!'.format(filekey))

def get_common(bucket_name,s3_path,local_file):
    return oss.get_object_to_file(bucket_name,s3_path,local_file)
    
'''
get file from s3 to local
'''
def get_file(bucket_name,s3_path,local_file):
    return s3utils.get_file_common(bucket_name,s3_path,local_file,get_common)



'''
only get video from s3 to local by file_key
param:just filekey
'''
def get_vodieo(filekey):
    return s3utils.get_vodieo(filekey,get_file)    
    
'''
get only source video file from s3  to local by video_id and local_file
'''        
def getVideo(video_id,local_file):
    s3utils.getVideo(video_id, local_file, get_file)


'''
get a file's url on s3,it can be download
'''    
def get_url(filekey):
    return s3utils.get_url(settings.ALIYUN_S3_HOST,filekey)


'''
list all files in the specified bucket by bucketname ,the result type is list
'''
def list_all_file(bucketname):
    ao = GetAllObjects()
    try:
        ao.get_all_object_in_bucket(oss,bucketname,"","")
        logging.info('get files from s3  bucket %s successfully' % bucketname)
    except:
        raise S3OperateError('get files from s3  bucket %s failed' % bucketname,None)
            
    return ao.object_list

'''
delete all files in the specified bucket by bucketname, try not to use this method if no need
''' 
def delete_all_file(bucketname):
    objs = list_all_file(bucketname)
    if objs:
        for obj in objs:
                delete(bucketname,obj)
    else:
        logging.info('bucket %s have no files ' % bucketname)
        raise S3OperateError('bucket %s have no files' % bucketname,None)
'''
create a bucket instance in s3 by bucketname
'''
def create_bucket(bucketname): 
    acl=''
    headers = {}
    try:
        res = oss.create_bucket(bucketname, acl, headers)
        if (res.status / 100) == 2:
            logging.info('create  bucket %s  successfully' % (bucketname))
        else:
            logging.info('create  bucket %s  failed' % (bucketname))
            raise S3OperateError('create  bucket %s  failed' % bucketname,None)         
    except:
        logging.info('create  bucket %s  failed,beacuase of the connection interrupt' % (bucketname)) 
        raise S3OperateError('create  bucket %s  failed' % bucketname,'beacuase of the connection interrupt')                           

'''
delete a bucket instance from s3 by bucketname
'''    
def delete_bucket(bucketname):
    try:
        res = oss.delete_bucket(bucketname)
        if (res.status / 100) == 2:
            logging.info('delete  bucket %s  successfully' % bucketname)
        else:
            logging.info('delete  bucket %s  failed' % bucketname)
            raise S3OperateError('delete  bucket %s  failed' % bucketname,None)     
    except:
        logging.info('delete  bucket %s  failed,beacuase of the connection interrupt' % (bucketname))  
        raise S3OperateError('delete  bucket %s  failed' % bucketname,'beacuase of the connection interrupt')
               
        
'''
delete any file from s3 by bucketname and s3path
'''
def delete(bucketname,s3path):
    flag = False
    headers = {}
    res1 = None
    try:
        res1 = oss.get_object(bucketname, s3path, headers)
    except:
        logging.info('get file %s in  s3 bucket %s failed ,beacuase of the connection interrupt' % (s3path,bucketname))
            
    if (res1.status / 100) == 2:
        res = None
        try:
            res = oss.delete_object(bucketname, s3path, headers)
            if (res.status / 100) == 2:
                logging.info('delete file %s from s3 bucket %s  successfully' % (s3path,bucketname))
                flag = True
            else:
                logging.info('delete file %s from s3 bucket %s failed' % (s3path,bucketname))
                raise S3OperateError('delete file %s from s3 bucket %s failed' % (s3path,bucketname),None)
        except:
            logging.info('delete file %s from s3 bucket %s failed,beacuase of the connection interrupt' % (s3path,bucketname))          
            raise S3OperateError('delete file %s from s3 bucket %s failed' % (s3path,bucketname),'beacuase of the connection interrupt')
    else:
        logging.info('file %s not exists on s3 bucket %s' % (s3path,bucketname))  
        raise S3OperateError('file %s not exists on s3 bucket %s' % (s3path,bucketname),None)    
    
    return flag    

            
if __name__ == "__main__":
    get_vodieo("uploaded-video/201205/75345726242029568/a4/79857138951782401")
