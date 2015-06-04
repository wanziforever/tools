#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
package start
'''
import functools

from bottle import Bottle as Application, run, static_file, redirect, HTTPError
from bottle import get, post, install
from bottle import jinja2_view as view
from bottle import request, response
# from settings import settings
# from redis_util import create_redis_session
# # from db import db_plugin, engine, Base, create_session
# from callbacks import all_callback
# import util
# import validation


def make_app_wrappers(app, actions = ['get', 'post']):
    wrappers = []
    for action in actions:
        wrappers.append(make_app_wrapper(app, action))
    return wrappers

def make_app_wrapper(app, action):
    @functools.wraps(getattr(Application, action))
    def wrapper(*args, **kwargs):
        return getattr(app, action)(*args, **kwargs)
    return wrapper

class status(dict):
    def __init__(self, s, **kwargs):
        self.status = s
        for k, v in kwargs.items():
            self[k] = v
