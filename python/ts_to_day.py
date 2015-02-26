#!/usr/bin/env python

import time
from datetime import datetime
import sys

def usage():
    print "%s <timestamp>"%sys.argv[0]

def call_convert(ts):
    dd = datetime.fromtimestamp(ts)
    return str(dd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit(1)
    ts = float(sys.argv[1]) / 1000
    date_str = call_convert(ts)
    print date_str
