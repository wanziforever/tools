#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re

def match_file(path):
    match_re = re.compile(s'')
    d = os.path.dirname(path)
    f = os.path.basename(path)
    #--------------------------------------------------
    # some work for match file for special requirement
    #--------------------------------------------------
    if os.path.islink(path):
        return True
    return False

def op_file(path):
    print path
        
if __name__ == "__main__":
    pwd = os.path.dirname(os.path.abspath(__file__))
    for p, d ,files in os.walk(pwd):
        for f in files:
            path = os.path.join(p, f)
            if not match_file(path):
                continue
            op_file(path)

            
