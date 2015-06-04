#!/usr/bin/env python
''' a very simple text based database implementation, and used to
store the final report data, all the data and table structure was
defined in text format, each table is related to a single file, and
no session concept support, so this means it cannot support multiple
threads or processes operation concurrently, you can only just connect
to the table, and do your work, and then close the table

the table definition is like the following:
  the first line is the column definition, and the line should be
  started with '#', each column definition was divided by '|', each
  data was divided by '|', here is a example:
  table name: active_users_day, related file: data/report/{active_users_total.in
  #k_model|k_date|count
  K370|2014-10-01|17839
  K370|2014-10-02|32130
  K370|2014-10-03|21670
'''

''' currently not support multiple key, should be the first field '''

import os
from common.echo import err, warn

suffix = ".in"
db_path = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(
        os.path.abspath(__file__)), os.pardir)), "data")

def hash_key(params):
    if not isinstance(params, dict):
        return None
    s = []
    for key, value in params.items():
        s.append("{0}::{1}".format(key, value))
    return "||".join(s)

class MySession(object):
    ''' the db operation object, link to a table instance, provide
    the table related operations '''
    def __init__(self, dbname, tbname):
        self.dbname = dbname
        self.tbname = tbname
        f = os.path.join(db_path, self.dbname, self.tbname+".in")
        try:
            self.fd = open(f, 'r+')
            self.opened = True
        except Exception, e:
            err("fail to open file")
            self.opened = False
        #self._lock()
        self.kfields = []
        self.fields = []
        self.knum = 0
        self._init_fields()
        self.entries = {}
        self._init_entries()
        self.buffers = []
        #self.num_not_flush = 0
        #self.num_need_flush = 100000

    def _lock(self):
        lf = os.path.join(db_path, self.dbname, ".lock_"+self.tbname)
        if os.path.exists(lf):
            return False
        with open(lf, "w") as f:
            f.write('')
            
    def _release(self):
        lf = os.path.join(db_path, self.dbname, ".lock_"+self.tbname)
        if os.path.exists(lf):
            return True
        os.remove(lf)

    def _init_fields(self):
        line = self.fd.readline()
        if line[0] != '#':
            return False
        i = 0
        for f in line[1:].split('|'):
            f = f.strip()
            if f[:2] == 'k_':
                f = f[2:]
                self.kfields.append(f)
                self.knum += 1
            self.fields.append(f)
            i += 1
        #print "all key fields", self.kfields
        #print "all fields", self.fields

    def _dump(self):
        if not self.fd.closed:
            self.fd.closed()
        f = os.path.join(db_path, self.dbname, self.tbname+".in")
        self.fd = open(f, 'w')
        self.fd.write("#%s\n"%('|'.join(self.fields)))
        for key, values in self.entries:
            self.fd.write('|'.join([key]+values)+"\n")
        self.fd.close()

    def _make_key(self, values):
        k = {}
        for i in range(self.knum):
            k[self.kfields[i]] = values[i]

        key = hash_key(k)
        return key
            
    def close(self):
        if self.opened == False:
            err("session %s already closed"%self.tbname)
            return False
        self.fd.close()
        self.opened = False
        #self._release()

    def _init_entries(self):
        line = self.fd.readline()
        while line:
            if len(line.strip()) == 0:
                line = self.fd.readline()
                continue
            values = line.strip().split('|')
            key = self._make_key(values)
            
            self.entries[key] = values
            line = self.fd.readline()

    def _append_entry(self, values):
        if self.opened is False:
            err("MySession::_append_entry() session is not opened")
            return False
        self.buffers.append(values)

    def commit(self):
        s = ""
        for entry in self.buffers:
            s += '|'.join(entry)+"\n"
            #self.num_not_flush += 1
        self.fd.write(s)
        self.buffers = []
        #if self.num_not_flush >= self.num_need_flush:
        #    self.num_not_flush = 0
        #    self._flush_data()
        self._flush_data()

    def _flush_data(self):
        if self.opened is False:
            err("MySession::_append_entry() session is not opened")
            return False
        self.fd.flush()

    def insert(self, kwargs, to_update=True):
        if not isinstance(kwargs, dict):
            err("invalid data format for insert opeation")
            return -1

        for keyf in self.kfields:
            if keyf not in kwargs:
                err("required key(%s) not in input data"%(keyf))
                return -1

        params = {}
        for keyf in self.kfields:
            params[keyf] = kwargs[keyf]

        key = hash_key(params)
            
        if key in self.entries:
            #err("MySession::insert() key already exist for \"%s\""%key)
            if to_update is True:
                self.update(kwargs)
            return 1

        values = []
        for field in self.fields:
            if field not in kwargs:
                err("field (%s) not provided"%field)
                return 2
            values.append(str(kwargs[field]))
        self.entries[key] = values
        self._append_entry(values)
        return 0
        
    def update(self, kwargs):
        if not isinstance(kwargs, dict):
            err("invalid data format for update opeation")
            return -1

        for keyf in self.kfields:
            if keyf not in kwargs:
                err("required key(%s) not in input data"%(keyf))
                return -1
        params = {}
        for keyf in self.kfields:
            params[keyf] = kwargs[keyf]

        key = hash_key(params)

        if key not in self.entries:
            err("key field not found (%s)"%key)
            return -1
        
        values = self.entries[key]
        need_update = False
        for i in range(len(self.fields)):
            field = self.fields[i]
            if field in self.kfields:
                continue
            if field not in kwargs:
                continue
            value = kwargs[field]
            if str(value) == values[i]:
                #warn('MySession::update() data no change for (%s)'%str(kwargs))
                continue
            values[i] = str(value)
            need_update = True
        if need_update is True:
            self._append_entry(values)
        return 0
        

    def _show_fields(self):
        s = "|".join(self.fields)
        return s

    def select(self, key='*', printable=False):
        entries = {}
        if key == '*':
            entries = self._select_all()
        else:
            entries = self._select(key)

        if printable == True:
            for key, values in entries:
                print "|".join(values)
                
        #return entries
        return entries
        

    def _select_all(self):
        if len(self.entries) == 0:
            return None
        return self.entries.items()

    def _select(self, key):
        if not isinstance(key, dict):
            err("MySession::_select() invalid key type, dict is required")
            return None
        key = hash_key(key)
        value = self.entries.get(key, None)
        if value is None:
            return None
        return [key, value]

    def __repr__(self):
        s = "table: %s, key="%self.tbname
        s += self.kfield + "\n"
        s += 'fields:' + ','.join(self.fields)
        return s
        
    
class Mydb(object):
    def __init__(self):
        self.name = ""
        self.connected = False

    def connect(self, db_name):
        f = os.path.join(db_path, self.name)
        if not os.path.exists(f):
            err("cannot open database %s"%db_name)
            self.connected = False
            return False
        self.name = db_name
        self.connected = True

    def open(self, table_name):
        if self.connected is False:
            err("database is not connected")
            return False
        f = os.path.join(db_path, self.name, table_name+".in")
        fd = None
        try:
            fd = open(f, "ra")
            fd.close()
        except Exception,e :
            print repr(e)
            return None
        return MySession(self.name, table_name)
