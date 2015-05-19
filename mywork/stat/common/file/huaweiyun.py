# -*- coding: utf-8 -*-
from boto.s3.connection import S3Connection,OrdinaryCallingFormat
from boto.s3.key import Key
from common import settings
import s3utils

'''
 conn = S3Connection('<aws access key>', '<aws secret key>')
 
 create by wujintao on 06th,09,2012
'''
calling_format=OrdinaryCallingFormat()
conn = S3Connection(settings.HUAWEIYUN_S3_ACCESSED_ID, settings.HUAWEIYUN_S3_SECRECT_ACCESS_KEY,host=settings.HUAWEIYUN_S3_HOST,is_secure=True,calling_format=calling_format)



'''
put local file to s3
param:just local file absolute  path
'''
def put(local_file):
    return s3utils.put_common(local_file,put_file)

def putByDeliveryType(local_file, delivery_type):
    raise NotImplementedError()

def put_common(bucket_name, s3_path, local_file): 
    b = conn.get_bucket(bucket_name)
    k = Key(b)
    k.key = s3_path
    k.set_contents_from_filename(local_file,policy='public-read')


'''
put local file to s3,must pass in a buketname,local file,the path of s3
'''  
def put_file(bucket_name,s3_path,local_file):
    return s3utils.put_file_common(bucket_name,s3_path,local_file,put_common)




'''
get any file from s3 to local by filekey and bucketname
'''
def get(filekey):
    return s3utils.get_common(filekey,get_file)


def get_common(bucket_name,s3_path,local_file):
    b = conn.get_bucket(bucket_name)
    key = b.lookup(s3_path)
    key.get_contents_to_filename(local_file)
    
'''
get file from s3 to local
'''
def get_file(bucket_name,s3_path,local_file):
    s3utils.get_file_common(bucket_name,s3_path,local_file,get_common)



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
    return s3utils.get_url(settings.HUAWEIYUN_S3_HOST,filekey)  