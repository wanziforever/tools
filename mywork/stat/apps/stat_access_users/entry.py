#!/usr/bin/env python

from common.echo import echo, debug, warn, err

def gen_entry(raw):
    code = raw[4:8]
    if code == "5010":
        return Log_5010_Entry(raw)
    elif code == "5049":
        return Log_5049_Entry(raw)
    elif code == "5054":
        return Log_5054_Entry(raw)
    elif code == "5011":
        return Log_5011_Entry(raw)
    elif code == "5042":
        return Log_5042_Entry(raw)
    elif code == "5001":
        return Log_5001_Entry(raw)
    else:
        return None

class Entry(object):
    def __init__(self, raw):
        self.doc = raw.split('|')
        self.version = self.doc[0]
        self.code = raw[4:8]
        self._init()

    def _init(self):
        self.userid = ''
        self.ts = ''
        self.navid = ''
        self.retention = ''
        self.vender = self.__class__.__name__ + "_vender"
        self.typecode = self.__class__.__name__ + "_typecode"

    def parse(self):
        pass

    def get_code(self):
        return self.code

    def get_vender(self):
        return self.vender

    def get_userid(self):
        return self.userid

    def get_typecode(self):
        return self.typecode

    def get_version(self):
        return self.version

    def get_ts(self):
        return self.ts

    def get_navid(self):
        return self.navid

    def get_retention(self):
        return self.retention
        
class Log_5010_Entry(Entry):
    def __init__(self, raw):
        Entry.__init__(self, raw)

    def parse(self):
        try:
            self.userid = self.doc[4]
            self.ts = self.doc[-5]
            if self.version == '1.0':
                self.vender = self.doc[-4]
            elif self.version == "1.1":
                self.vender = self.doc[-2]
            else:
                err('Log_5010_Entry::parse() invalid version %s'%self.version)
                return False
        except Exception, e:
            import traceback
            debug(traceback.format_exc())
            debug("exception meet for Log_5010_Entry %s"%self.doc)
            return False
        return True
    def __repr__(self):
        s = "Log_5010_Entry(%s) userid:{0}, vender: {1}, ts:{2}".\
            format(self.version, self.userid, self.vender, self.ts)
        return s

class Log_5049_Entry(Entry):
    def __init__(self, raw):
        Entry.__init__(self, raw)

    def parse(self):
        try:
            self.userid = self.doc[4]
            self.ts = self.doc[9]
            self.typecode = self.doc[10]
        except Exception, e:
            import traceback
            debug(traceback.format_exc())
            debug("exception meet for Log_5040_Entry %s"%self.doc)
            return False
        return True
                
    def get_userid(self):
        return self.userid

    def get_ts(self):
        return self.ts

    def __repr__(self):
        s = "Log_5049_Entry(%s) userid:{0}, vender: {1}, ts:{2}".\
            format(self.version, self.userid, self.vender, self.ts)
        return s

class Log_5054_Entry(Entry):
    def __init__(self, raw):
        Entry.__init__(self, raw)

    def parse(self):
        try:
            self.userid = self.doc[4]
            self.ts = self.doc[9]
            self.navid = self.doc[10]
        except Exception, e:
            import traceback
            debug(traceback.format_exc())
            debug("exception meet for Log_5054_Entry %s"%self.doc)
            return False
        return True
                
    def get_userid(self):
        return self.userid

    def get_ts(self):
        return self.ts

    def __repr__(self):
        s = "Log_5049_Entry(%s) userid:{0}, vender: {1}, ts:{2}".\
            format(self.version, self.userid, self.vender, self.ts)
        return s

class Log_5011_Entry(Entry):
    def __init__(self, raw):
        Entry.__init__(self, raw)

    def parse(self):
        try:
            self.userid = self.doc[4]
            self.ts = self.doc[9]
            if self.version == "1.1":
                self.retention = int(self.doc[14])/1000
            elif self.version == "1.0":
                self.retention = int(self.doc[13])/1000
            else:
                err('Log_5010_Entry::parse() invalid version %s'%self.version)
                return False
                
            if int(self.retention) > 10800:
            #if int(self.retention) > 86400:
                # invalid retention, maybe the retention was set to ts
                return False

        except Exception, e:
            import traceback
            debug(traceback.format_exc())
            debug("exception meet for Log_5011_Entry %s"%self.doc)
            #print traceback.format_exc()
            #print "exception meet for Log_5011_Entry %s"%self.doc
            return False
        return True
                
    def get_userid(self):
        return self.userid

    def get_ts(self):
        return self.ts

    def __repr__(self):
        s = "Log_5049_Entry(%s) userid:{0}, vender: {1}, ts:{2}".\
            format(self.version, self.userid, self.vender, self.ts)
        return s

class Log_5042_Entry(Log_5011_Entry):
    def __init__(self, raw):
        Log_5011_Entry.__init__(self, raw)

class Log_5001_Entry(Entry):
    def __init__(self):
        Entry.__init__(self, raw)

    def parse(self):
        try:
            self.userid = self.doc[4]
            self.ts = self.doc[9]
            
