#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
root api
@author: Shao Guojian
'''

import logging

from core import Application, make_app_wrappers
from core import request, response

app = Application()
get, post, default_error = make_app_wrappers(app, ['get', 'post', 'default_error'])

@get('/hello')
def hello():
    return "hello"
