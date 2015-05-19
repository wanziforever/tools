#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jul 5, 2011

@author: mengchen
'''
from common.types import Properties, Dict
import logging
import os



FILESTORE_DIR = '/srv/upload'
FTP_DIR = os.path.join(FILESTORE_DIR, 'ftp-uploaded')
ENABLE_FLVTOOL = True

_props = Properties()
try:
    _props.load('/srv/www/video-tx.properties')
except:
    logging.warn('Properties file /srv/www/video-tx.properties not found.')
API_DOMAIN = _props.get('api.domain', 'api.video-tx.com')
SHARED_KEY = _props.get('api.sharedKey', 'Shared-4-Internal-API-Only')
IOS_SEGMENT_DURATION = int(_props.get('transcode.iosSegmentDuration', '0'))
FFMPEG_THREAD_COUNT = int(_props.get('transcode.ffmpeg.threadCount', 1))
PUBLIC_FILESTORE_DIR = _props.get('publicRestriction.publicFileStoreDir', '/srv/upload/public')
LIVE_DIR = _props.get('live.fms.dir')

DISTRIBUTION_MODE = _props.get('distribution.distributionMode', 'ftp')

S3_DELETEBEFORE_DAYS =  int(_props.get('distribution.s3.deletebeforedays', '30'))
S3_RENDITION_PATH = _props.get('distribution.s3.renditionpath', '/srv/upload/rendition')
S3_VIDEO_PATH = _props.get('distribution.s3.videopath', '/srv/upload/uploaded-video')
S3_STATICFILE_PATH = _props.get('distribution.s3.staticfilepath', '/srv/upload/uploaded-asset')
S3_SNAPSHOT_PATH = _props.get('distribution.s3.snapshotpath', '/srv/upload/snapshot')

ALIYUN_S3_HOST = _props.get('distribution.aliyun.s3.host', 'storage.aliyun.com')
ALIYUN_S3_ACCESSED_ID = _props.get('distribution.aliyun.s3.accessid', 'hyud3x41xh99ev4odz7fgzx4')
ALIYUN_S3_SECRECT_ACCESS_KEY = _props.get('distribution.aliyun.s3.accesskey', 'er9d/qScOK2YAcRQJk11kRuoPh8=')

HUAWEIYUN_S3_HOST = _props.get('distribution.huaweiyun.s3.host', 's3.hwclouds.com')
HUAWEIYUN_S3_ACCESSED_ID = _props.get('distribution.huaweiyun.s3.accessid', 'FE4E0B287AA9E98699C6')
HUAWEIYUN_S3_SECRECT_ACCESS_KEY = _props.get('distribution.huaweiyun.s3.accesskey', 'WMEbfJXSCXR1W2U1Zk0Fb7nwfoIAAAE4eqnphoNi')


S3_VOD_BUCKET =  _props.get('distribution.s3.vodbucket', 'vodmedia')
S3_LIVE_BUCKET =  _props.get('distribution.s3.livebucket', 'livemedia')
S3_IOS_BUCKET =  _props.get('distribution.s3.iosbucket', 'iosmedia')
S3_STATIC_BUCKET =  _props.get('distribution.s3.staticbucket', 'staticfile')

HTTP_FLV_URL = _props.get('distribution.ftp.http_flv.destRootDir', '')
HTTP_IOS_URL = _props.get('distribution.ftp.http_ios.destRootDir', '')
HTTP_STATIC_URL = _props.get('distribution.ftp.http_static.destRootDir', '')
HTTP_LIVE_URL = _props.get('live.http.baseUrl', '')

MAX_TASKS_PER_GROUP = _props.get('queue.maxTasksPerGroup', '10')
MAX_RETRY_TIMES = _props.get('queue.maxRetryTimes', '3')

API_DOMAIN = _props.get('api.domain', 'api.video-tx.com')
DB_HOST = _props.get('kernel.db.host', 'db.video-tx.com')
DB_USER = _props.get('kernel.jdbc.user', 'dev')
DB_PASSWORD = _props.get('kernel.jdbc.password', 'video-tx')
DB_KERNEL = _props.get('kernel.db.name', 'kernel')
KERNELS = _props.get('kernel.list', 'kernel.video-tx.com:8080')

def get_prop(key, default=None):
    return _props.get(key, default)

def _load_ftp_sites():
    types = set([k.split('.')[2] for k in _props.keys() if k.startswith('distribution.ftp.')])
    sites = {}
    for type in types:
        site = Dict()
        site.host = _props.get('distribution.ftp.%s.host' % type)
        site.user = _props.get('distribution.ftp.%s.userName' % type)
        site.passwd = _props.get('distribution.ftp.%s.password' % type)
        site.root_dir = _props.get('distribution.ftp.%s.rootDir' % type)
        site.dest_root_dir = _props.get('distribution.ftp.%s.destRootDir' % type)
        sites[type] = site
    return sites

FTP_SITES = _load_ftp_sites()

deliveryMappers = ({'type':'http_flv',
                   'bucket':S3_VOD_BUCKET,
                   'url':HTTP_FLV_URL
                   },
                  {'type':'http_ios',
                   'bucket':S3_IOS_BUCKET,
                   'url':HTTP_IOS_URL
                   },
                  {'type':'http_static',
                   'bucket':S3_STATIC_BUCKET,
                   'url':HTTP_STATIC_URL
                   }
                  )
