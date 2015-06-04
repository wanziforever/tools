#!/usr/bin/env python


import time

class entry(object):
    def __init__(self):
        self.i = self.__class__.__name__


class aaa(entry):
    def __init__(self):
        entry.__init__(self)

e = aaa()
print e.i
