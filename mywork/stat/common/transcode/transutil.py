#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.util.wrapper import Wrapper
import os

class ConverterWrapper(Wrapper):
    ACTION_CONVERT = 'convert'
    ACTION_VERIFY = 'verify'
    
    def __init__(self, class_name, action, src, dest_dir=None):
        classpath = os.path.join(os.path.dirname(__file__), 'convert', '*')
        cmd = 'java -cp "%s" %s %s %s %s' % (classpath, class_name, action, src, dest_dir)
        super(ConverterWrapper, self).__init__(cmd)
    
