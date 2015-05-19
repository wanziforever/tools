#!/usr/bin/env python

import inspect

#debug_flag = True
debug_flag = False

def echo(text):
    print "%s | %s"%("INFO", text)

def debug(text):
    if debug_flag is False:
        return 
    print "DEBUG | %s \n%s"%(inspect.stack()[1], text)


def warn(text):
    print "WARN!! %s"%text

def err(text):
    print "ERROR!! %s"%text
