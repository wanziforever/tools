#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import request
from common.errors import ApiNotFoundError
from core.bottle import make_http_error

api_error_handlers = {}
page_error_handlers = {}
api_default_error_handler = None
page_default_error_handler = None

def default_error(types=['api']):
    def wrapper(handler):
        global api_default_error_handler
        global page_default_error_handler
        if 'api' in types:
            api_default_error_handler = handler
        if 'page' in types:
            page_default_error_handler = handler
        return handler
    return wrapper

def error(types=['api'], code=500):
    def wrapper(handler):
        global api_error_handlers
        global page_error_handlers
        if 'api' in types:
            api_error_handlers[int(code)] = handler
        if 'page' in types:
            page_error_handlers[int(code)] = handler
        return handler
    return wrapper

@default_error()
def default_error_handler(e):
    vr = request.viewresolver
    return vr.resolve(e)

@error(code=404)
def api_not_found(e):
    vr = request.viewresolver
    return vr.resolve(make_http_error(ApiNotFoundError(request.fullpath)))






