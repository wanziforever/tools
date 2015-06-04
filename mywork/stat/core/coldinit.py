#!/usr/bin/env python

import os

from itertools import permutations
from string import ascii_uppercase

from df import data_function
from df.datamodel.schema import SCHEMA
from df.datamodel.schema import DATATYPE
from df.data_descriptor import DataDesc

x3 = permutations(ascii_uppercase, r=3)
x2 = permutations(ascii_uppercase, r=2)
x1 = permutations(ascii_uppercase, r=1)

data_desc = DataDesc(SCHEMA.schema_search,
                     DATATYPE.data_type_query_all)
data_desc.setCached(True)


for x in x1:
    key = "".join(x)
    params = {"start": '0',
          "rows": '200',
          "type": '0',
          "search_key": key}
    print "processing key ", key
    data_desc.setKey(1, params)
    data_function.db_get(data_desc)

for x in x2:
    key = "".join(x)
    params = {"start": '0',
          "rows": '200',
          "type": '0',
          "search_key": key}
    print "processing key ", key
    data_desc.setKey(1, params)
    data_function.db_get(data_desc)

xlist = []
for x in x3:
    xlist.append(x)
print "x3 has %s number"%len(xlist)

process_num = 6
per = len(xlist)/process_num

for i in xrange(0, process_num-1):
    pid = os.fork()
    if pid > 0:
        break

xxlist = xlist[i*per:(i+1)*per]
total = len(xxlist)
count=0
for x in xxlist:
    key = "".join(x)
    params = {"start": '0',
          "rows": '200',
          "type": '0',
          "search_key": key}
    count += 1
    print "processing key %s, --PID# %s--%s%%(%s/%s)"\
          %(key, os.getpid(), count/total, count, total)
    data_desc.setKey(1, params)
    data_function.db_get(data_desc)

