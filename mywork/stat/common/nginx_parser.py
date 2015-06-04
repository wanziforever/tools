#!/usr/bin/env python

import re
import os

master_re = re.compile("master_view")
device_re = re.compile("&device_id=")

def parse(raw):
    m = master_re.search(raw)
    if m:
        #print "ignore master view"
        return
    #print raw
    m = device_re.search(raw)
    if m:
        print "find device id", m.groups()
    
    

f = "/data/logs/nginx/api.vod.jamdeocloud.com.access.log-2014090209"
fd = open(f, "r")
for f in fd:
    parse(f)

fd.close()


