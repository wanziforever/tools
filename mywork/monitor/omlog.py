#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
reload(sys)  # Reload does the trick!
from datetime import datetime
from datetime import timedelta
import time
import textwrap
sys.setdefaultencoding('UTF8')

from jinja2 import Template

from omstring import *
indent = "   "

lineprefix = "+++ {host} {date} {level} {module} #{seq}"
linesuffix = "END OF REPORT #{seq}++-"

OM_LOG_LEVEL = ['INFO', 'WARN', 'ERROR', 'FATAL', 'NORMAL_ALARM',
                "HIGH_ALARM", "CRITICAL_ALARM"]
seq = 0

def get_seq():
    global seq
    s = "%08d"%seq
    seq += 1
    return s

def add_indent(inpstr, indent):
    return indent + inpstr.replace("\n", "\n"+indent)

def wrap_long_line(content):
    max_length = 80
    s = []
    for l in content.splitlines():
        s.append(textwrap.fill(l.strip(), width=80))
    return "\n".join(s)

class OMlog(object):
    def __init__(self, level = 'INFO'):
        self.attributes = {}
        if level not in OM_LOG_LEVEL:
            print "invalid log level %s, default to INFO"
            self.level = 'INFO'
        else:
            self.level = level
        self.module = None

    def set_module(self, module_name):
        self.module = module_name.upper()

    def add(self, name, value):
        self.attributes[name] = value

    def spool(self, omstring):
        current_seq = get_seq()
        begain = lineprefix.format(
            host=os.uname()[1],
            date=str(datetime.now())[0:19],
            level = self.level,
            module = self.module if self.module is not None else __name__,
            seq = current_seq
            )
        s = ""
        s += add_indent(begain, indent) + "\n"
        prefix = ""
        # add alarm related prefix of OM log, so CRITICAL_ALARM will
        # have CA prefix, HIGH_ALARM will have HA
        if self.level != "INFO":
            if self.level.find('_') != -1:
                for c in self.level.split('_', 1):
                    prefix += c[0]
            else:
                prefix = self.level[0]
        if len(prefix) > 2:
            prefix = prefix[0:2]
        s = prefix + s[len(prefix):]
        t = Template(omstring)
        content = t.render(**self.attributes)
        content = wrap_long_line(content)
        s += add_indent(content, indent+" ") + "\n\n"
        s += add_indent(linesuffix.format(seq=current_seq), indent) + "\n"
        print s
        return s

def om_output(omstring):
    om = OMlog("INFO")
    om.set_module(os.environ.get('module_name', 'UNDEFINED'))
    om.spool(omstring)

def om_err_output(errstring):
    om = OMlog("ERROR")
    om.set_module(os.environ.get('module_name', 'UNDEFINED'))
    om.spool(errstring)

def om_warn_output(warnstring):
    om = OMlog("WARN")
    om.set_module(os.environ.get('module_name', 'UNDEFINED'))
    om.spool(warnstring)

def om_fatal_output(fatalstring):
    om = OMlog('FATAL')
    om.set_module(os.environ.get('module_name', 'UNDEFINED'))
    om.spool(fatalstring)

if __name__ == "__main__":
    pass
    om = OMlog("ERROR")
    om.set_module(os.environ.get('module_name', 'UNDEFINED'))
    om.spool('''mark fails with a "'str' object does not support item assignment" error,even though''')
