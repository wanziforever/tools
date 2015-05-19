#!/usr/bin/env python

import time

ts_str0 = "02/Sep/2014:09:01:02"
ts_str1 = "02/09/2014"
ts0 = int(time.mktime(time.strptime(ts_str0, "%d/%b/%Y:%H:%M:%S")) * 1000)
#ts1 = int(time.mktime(time.strptime(ts_str1, "%d/%m/%Y")) * 1000)
print ts0
