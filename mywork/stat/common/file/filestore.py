## -*- coding: utf-8 -*-
#from oss_api import *
##import sys
##sys.path.append('F:/VideoTxSpace/aliyun/common/py/src')
#from common import settings
#from common.util import vtxutil
#from common.error.errors import ResourceNotFoundError
#import os
#import time
#import logging
#
#log = logging.getLogger(__name__)
#
#
#class filestore:
#    
#    host = settings.ALIYUN_S3_HOST
#    access_id = settings.ALIYUN_S3_ACCESSED_ID
#    secret_access_key = settings.ALIYUN_S3_SECRECT_ACCESS_KEY
#    bucket = settings.S3_VOD_BUCKET
#    
#    oss = OssAPI(host, access_id, secret_access_key)
#    
#    
#    def _get_file_path_back_up(self,filekey):
#         path = vtxutil.get_file_from_fs(filekey)
#         if  not os.path.isfile(path):
#                print 'file: \'',path,'\' not exists......'
#                #s3url = 'http://' + self.host + '/' + self.bucket + '/' + path[5:]
#                
#                print 'start download from s3 url: \'',filekey,'\'to local path: \'',path,'\'.......'
#                arr = str(path).split('/')
#                del arr[len(arr)-1]
#                dic = '/'.join(arr)
#                if not os.path.exists(dic):
#                    print 'create dir:\'',dic,'\'......'
#                    os.makedirs(dic)
#                res = self._download_s3file_to_local(self.bucket,filekey,path)
#                size = os.path.getsize(path) 
#                print 'end download......'
#                return path
#         else:
#             print 'file: \'',path,'\'already exists......'
#             return path
#   
#    def _get_file_path(self,filekey):
#        path = vtxutil.get_file_from_fs(filekey)
#        self._create_dir(path)
#        if self._isnot(path,3600):
#            if  not os.path.isfile(path):
#                if(self._create_pid(filekey,path)):
#                    return path
#                else:
#                    self._get_file_path(self,filekey)    
#            else:
#                print 'file:  %s is already exists,use it ......' % path
#                log.info('file:  %s is already exists,use it ......' % path)
#                return path
#        else:
#            #这里什么都不应该返回，直接抛出异常
#            
#            raise ResourceNotFoundError('FILE', path)
#
#    def _del_pid(self,path):
#        piddir = path+'.pid'
#        os.rmdir(piddir)
#
#
#    
#    def _create_dir(self,path):
#        arr = str(path).split('/')
#        del arr[len(arr)-1]
#        dic = '/'.join(arr)
#        if not os.path.exists(dic):
#            print 'create dir:\'',dic,'\'......'
#            try:
#                os.makedirs(dic)
#            except Exception,e:
#                pass               
#
#
#    def _create_pid(self,filekey,path):
#        piddir = path+'.pid'
#        try:
#            log.info('create piddir %s' % piddir)
#            print 'create pid',piddir
#            os.mkdir(piddir)
#            print 'create piddir %s succesful' % piddir
#            log.info('create piddir %s succesful' % piddir)
#            print 'start download %s from s3 to %s' % (filekey,path)
#            log.info('start download %s from s3 to %s' % (filekey,path))
#            self._download_s3file_to_local(self.bucket,filekey,path)
#            print 'end download %s from s3 to %s' % (filekey,path)
#            log.info('end download %s from s3 to %s' % (filekey,path))
#            log.info('delete piddir %s' % piddir)
#            print 'delete piddir %s' % piddir
#            self._del_pid(path)
#            return True
#        except Exception, e:
#            print 'create piddir %s fail,once again......' % piddir
#            log.info('create piddir %s fail,once again......' % piddir)
#            return False
#            
#        return False    
#
#        
#
#    def _isnot(self,path,deadline):
#        piddir = path+'.pid'
#        if deadline==0:
#            print 'deadline leave:%s ,deadline is arrival,error' % deadline
#            log.info('deadline leave:%s ,deadline is arrival,error' % deadline)
#            return False
#        
#        if(os.path.exists(piddir)):
#            print 'oh no!!!! someone using ! piddir %s is already exists,please wait......' % piddir
#            print 'deadline leave:%s ,go on......' % deadline
#            log.info('oh no!!!! someone using ! piddir %s is already exists,please wait......' % piddir)
#            log.info('deadline leave:%s ,go on......' % deadline)
#            time.sleep(15)
#            deadline = deadline-15
#            return self._isnot(path,deadline)
#        else:
#            print 'piddir %s is not exists......' % piddir
#            log.info('piddir %s is not exists......' % piddir)
#            return True 
#    
#    def _upload_file_to_s3(self,bucketname,s3path,localFilePath):
#         print 'start upload file: \'',localFilePath,'\' to s3 url: \'',s3path,'\''
#         res = self.oss.put_object_from_file(bucketname, s3path, localFilePath)
#         print 'end upload......' 
#         
#    
#    def _download_s3file_to_local(self,bucketname,s3path,localFilePath):
#         res = self.oss.get_object_to_file(bucketname,s3path,localFilePath)
#    
#    
#    
#    
#    def _create_file(self,filekey,sync=True):
#         from_path = '/jintao/'+filekey
#         to_path = vtxutil.get_file_from_fs(filekey)
#         self._copy_file(from_path, to_path)
#         s3url = to_path[5:]
#         self._upload_file_to_s3(self.bucket, s3url,to_path)
#        
#    #复制文件,二进制文本文件都行
#    def _copy_file(self,from_path,to_path):
#        to_file = open(to_path,'wb')
#        with open(from_path,'rb') as file:
#            while True:
#                content = file.read()
#                if not content:
#                    break
#                to_file.write(content,)
#            to_file.close()
#        
#
#if __name__ == "__main__":
#    #filestore()._read_file5("c:/test.txt")
#    #filestore()._write_file("c:/test.txt",'HelloWorld')
#    #filestore()._copy_file('c:/test.txt','f:/test.txt')
#    #filestore()._copy_file("f:/stagger.mp4", "c:/aa.mp4")
#    #filestore()._create_file("rendition/201205/75345726242029568/02/77958708914552833/77958714283261953/r64119950893122050-149k-320x240.flv");
#    #filestore()._upload_file_to_s3(filestore().bucket,'rendition/201205/75345726242029568/02/77958708914552833/77958714283261953/stagger.mp4','/srv/upload/rendition/201205/75345726242029568/02/77958708914552833/77958714283261953/stagger.mp4')
#    
##    try:
##        #os.mkdir('/aaa.bc')
##        #os.rmdir('/aaa.bc')
##        #os.makedirs("/abc/bcd/efc")
##        print os.path.exists("/abc/bcd/efcd")
##        print 'True'
##    except Exception:
##        print 'False'
##        pass
##    finally:
##        print 'Final'
#    #filestore()._create_pid("uploaded-video/201205/75345726242029568/a4/79857138951782401","/srv/upload/uploaded-video/201205/75345726242029568/a4/79857138951782401")
#    filestore()._get_file_path("uploaded-video/201205/75345726242029568/a4/79857138951782401")
