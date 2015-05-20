#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)
import os
from omstring import ALARM_STRING
from alarm_definition import *

class ALARM_LEVEL():
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0

class Alarm(object):
    ''' three alarm level from 0 to 2, 0 means highest level '''
    def __init__(self, level, alm_definition):
        self.problem = alm_definition[1]
        self.level = level
        self.level_string = ""
        self.almid = alm_definition[0]
        if self.level == ALARM_LEVEL.NORMAL:
            self.level_string = "NORMAL"
        elif self.level == ALARM_LEVEL.HIGH:
            self.level_string = "HIGH"
        elif self.level == ALARM_LEVEL.CRITICAL:
            self.level_string = "CRITICAL"
        else:
            self.level_string = "UNDEFINED_ALARM_LEVEL"

    def report_alarm(self, err_msg):
        om = OMlog('ALARM')
        om.set_module('ALARM')
        om.add("problem", self.problem)
        om.add("alarmid", self.almid)
        om.add("msg", err_msg)
        return om.spool(ALARM_STRING)

class NormalAlarm(Alarm):
    def __init__(self, specific_problem):
        Alarm.__init__(self, 2, specific_problem)

class HighAlarm(Alarm):
    def __init__(self, specific_problem):
        Alarm.__init__(self, 1, specific_problem)

    def report_alarm(self, err_msg):
        om = OMlog('HIGH_ALARM')
        om.set_module('ALARM')
        om.add("problem", self.problem)
        om.add("alarmid", self.almid)
        om.add("msg", err_msg)
        return om.spool(ALARM_STRING)
        
class CriticalAlarm(Alarm):
    def __init__(self, specific_problem):
        Alarm.__init__(self, 0, specific_problem)

    def report_alarm(self, err_msg):
        om = OMlog('CRITICAL_ALARM')
        om.set_module('ALARM')
        om.add("problem", self.problem)
        om.add("alarmid", self.almid)
        om.add("msg", err_msg)
        return om.spool(ALARM_STRING)

def alarm(level, specific_problem, err_msg):
    alm = None
    if level == ALARM_LEVEL.CRITICAL:
        alm = CriticalAlarm(specific_problem)
    elif level == ALARM_LEVEL.HIGH:
        alm = HighAlarm(specific_problem)
    elif level == ALARM_LEVEL.NORMAL:
        alm = NormalAlarm(specific_problem)
    else:
        print("wrong alarm level")
        return
    om_msg = alm.report_alarm(err_msg)

    # every alarm message will be write to a file
    alarm_file = os.environ.get('alarm_file', '')

    if len(alarm_file.strip()) == 0:
        return

    fd = open(alarm_file, "a")
    fd.write(om_msg + "\n")
    fd.flush()
    fd.close()
    
