#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)
import os
import socket
import cPickle
import settings
from omstring import ALARM_STRING
from alarm_definition import *

sock = None
addr = (settings.alarm_server_host, settings.alarm_server_port)
def setup_network():
    global sock
    # need to check the alarm server exists??
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

setup_network()

class ALARM_LEVEL():
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0

class Alarm(object):
    ''' three alarm level from 0 to 2, 0 means highest level '''
    def __init__(self, level, alm_definition, err_msg):
        self.problem = alm_definition[1]
        self.level = level
        self.almid = alm_definition[0]
        self.err_msg = err_msg
        self.module_name = os.environ.get('module_name', "UNDEFINED")

    def report_alarm(self):
        om = OMlog(self.level)
        om.set_module(self.module_name)
        om.add("problem", self.problem)
        om.add("alarmid", self.almid)
        om.add("msg", self.err_msg)
        return om.spool(ALARM_STRING)

    def sync_to_server(self):
        global sock, addr
        if sock is None:
            return False
        obj = cPickle.dumps(self)
        sock.sendto(obj, addr)

class NormalAlarm(Alarm):
    def __init__(self, specific_problem, err_msg):
        Alarm.__init__(self, 'NORMAL_ALARM', specific_problem, err_msg)

class HighAlarm(Alarm):
    def __init__(self, specific_problem, err_msg):
        Alarm.__init__(self, 'HIGH_ALARM', specific_problem, err_msg)

class CriticalAlarm(Alarm):
    def __init__(self, specific_problem, err_msg):
        Alarm.__init__(self, 'CRITICAL_ALARM', specific_problem, err_msg)

def alarm(level, specific_problem, err_msg):
    alm = None
    if level == ALARM_LEVEL.CRITICAL:
        alm = CriticalAlarm(specific_problem, err_msg)
    elif level == ALARM_LEVEL.HIGH:
        alm = HighAlarm(specific_problem, err_msg)
    elif level == ALARM_LEVEL.NORMAL:
        alm = NormalAlarm(specific_problem, err_msg)
    else:
        print("wrong alarm level")
        return
    om_msg = alm.report_alarm()
    alm.sync_to_server()

    # every alarm message will be write to a file
    alarm_file = os.environ.get('alarm_file', '')

    if len(alarm_file.strip()) == 0:
        return

    fd = open(alarm_file, "a")
    fd.write(om_msg + "\n")
    fd.flush()
    fd.close()
    
