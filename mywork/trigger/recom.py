#!/usr/bin/env python

import pycurl
import StringIO

recom_refresh_url = """http://api.wasuvod.hismarttv.com/recom/api/develop/multirecom?start={start}&rows={rows}&outtime={timeout}"""
start = 0
end = 0 # rows currently represent end
timeout = 60
rows = 20

class MultiTrigger(object):
    def __init__(self):
        self.m = pycurl.CurlMulti()
        self.triggers = []
        
    def add_trigger(self, trigger):
        print "MultiTrigger::add_trigger() %s"%repr(trigger)
        self.m.add_handle(trigger.curl)
        self.triggers.append(trigger)

    def perform(self):
        print "MultiTrigger::perform() enter"
        while True:
            ret, num_handles = self.m.perform()
            print ret, num_handles
            if ret != pycurl.E_CALL_MULTI_PERFORM: break
        while num_handles:
            ret = self.m.select(1.0)
            if ret == -1:  continue
            while 1:
                ret, num_handles = self.m.perform()
                # E_CALL_MULTI_PERFORM returned, always meed to recall
                # select function
                if ret != pycurl.E_CALL_MULTI_PERFORM: break
        print "MultiTrigger::perform() exit"

    def show_all_info(self):
        for t in self.triggers:
            print t.show_response()

class Trigger(object):
    def __init__(self, url):
        self.curl = pycurl.Curl()
        self.data = StringIO.StringIO()
        self.url = url
        self._setup()

    def _setup(self):
        self.curl.setopt(pycurl.URL, self.url)
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 60)
        self.curl.setopt(pycurl.WRITEFUNCTION, self.data.write)

    def __repr__(self):
        return "Trigger: %s"%self.url

    def show_response(self):
        s = ("url: {url}\n"
             "response: {data}")
        return s.format(url=self.url, data=self.data.getvalue())

total = 30
def call_recom_fresh():
    delta = 20
    start = 0
    end = start + delta
    timeout = 100
    m = MultiTrigger()
    while start < total:
        url = recom_refresh_url.format(start=start,
                                       rows=end,
                                       timeout=timeout)
        t = Trigger(url)
        m.add_trigger(t)
        start = end
        end = end + delta

    m.perform()
    m.show_all_info()
        
if __name__ == "__main__":
    call_recom_fresh()
