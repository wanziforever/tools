#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
created on 1th,June by wujintao
'''

from common import settings


if settings.DISTRIBUTION_MODE=='aliyun':
    import aliyun as s3
elif settings.DISTRIBUTION_MODE=='huaweiyun':
    import huaweiyun as s3
elif settings.DISTRIBUTION_MODE=='local' or settings.DISTRIBUTION_MODE=='ftp':
    import local as s3