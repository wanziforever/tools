#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

MEDIA_OFFLINE = ("Media [{{mediaid}}] is offline\n"
                 "Location: \n"
                 "{{location}}")

ALARM_STRING = ("PROBLEM: {{problem}}, \tALARM_ID: {{alarmid}}\n{{msg}}")
                                               
