#!/usr/bin/env python

import sys
import pycurl
import StringIO
import json
from utils import info, err, errtrace, debug

recom_fresh_url = '''http://api.wasuvod.hismarttv.com/recom/api/multirecom?uuid={0}&cnum={1}'''

def recom_refresh(user, cnum):
    url = recom_fresh_url.format(user, cnum)
    info("going to refresh recom data through %s"%url)
    data = ""
    try:
        c = pycurl.Curl()
        b = StringIO.StringIO()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.CONNECTTIMEOUT, 10)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.perform()
        data = b.getvalue()
    except Exception,e :
        errtrace("site::recom_refresh() exception when getting data "
                 "from %s, err(%s)"%(url, str(e)))
        data = ""
        return False
    return True
    
if __name__ == "__main__":
    user = sys.argv[1]
    cnum = sys.argv[2]
    recom_refrersh(user, cnum)
