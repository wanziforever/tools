#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2012-1-15

@author: mengchen
'''
import platform

def is_linux():
    return platform.system() == 'Linux'

def is_windows():
    return platform.system() == 'Windows'
