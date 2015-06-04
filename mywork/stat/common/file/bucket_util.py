#from oss_api import *
#from oss_util import GetAllObjects
#import sys
#sys.path.append('F:/VideoTxSpace/aliyun/common/py/src')
#from common import settings
#
#def initOOS():
#    host = settings.ALIYUN_S3_HOST
#    access_id = settings.ALIYUN_S3_ACCESSED_ID
#    secret_access_key = settings.ALIYUN_S3_SECRECT_ACCESS_KEY
#    oos = OssAPI(host, access_id, secret_access_key)
#    return oos
#
#
#def delete_file(bucketname,s3path):
#    flag = False
#    oos = initOOS()
#    headers = {}
#    res1 = oos.get_object(bucketname, s3path, headers)
#    if (res1.status / 100) == 2:
#        res = oos.delete_object(bucketname, s3path, headers)
#        if (res.status / 100) == 2:
#            print "delete object from s3 OK"
#            flag = True
#        else:
#            print "delete object from s3 ERROR"
#    else:
#        print 'file not exists on s3'       
#    
#    return flag    
#
#
#def listAllObjectInBuckt(bucketname):
#    ao = GetAllObjects()
#    oos = initOOS()
#    ao.get_all_object_in_bucket(oos,bucketname,"","")
#    return ao.object_list    
#        
#def removeAllObjectInBucket(bucketname):
#    oos = initOOS()
#    objs = listAllObjectInBuckt()
#    for obj in objs:
#        print 'delete obj %s' % obj
#        oos.delete_object(bucketname,obj,{})       
#
#def deleteBucket(bucketname):
#    oos = initOOS()
#    oos.delete_bucket(bucketname)
#
#def createBucket(bucketname): 
#    oos = initOOS()
#    acl=''
#    headers = {}
#    oos.create_bucket(bucketname, acl, headers)
#    
#deleteBucket('wujintao')    