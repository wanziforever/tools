#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import cPickle
import settings
from omlog import (OMlog, om_output, om_err_output,
                   om_warn_output, om_fatal_output)


def call_alarm_monitor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    om_output("alarm server bind to %s:%s"%(settings.alarm_server_host,
                                            settings.alarm_server_port))
    sock.bind((settings.alarm_server_host,
              settings.alarm_server_port))
    while True:
        data, addr = sock.recvfrom(2048)
        if not data:
            continue
        alarm_obj = cPickle.loads(data)
        alarm_obj.report_alarm()

if __name__ == "__main__":
    settings.set_module_name('ALARM_SERVER')
    call_alarm_monitor()
