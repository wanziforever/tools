#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
application server

@author: Shao Guojian
"""

from core import log

# init log
log.init_log('vod', 'app')

import importlib
from core import Application, run
from core.settings import settings
from apps import get_app_names, get_root_name
from core import handler
from core.settings import get_version
import logging

log = logging.getLogger(__name__)

__root__ = None


def get_application(api_module_name):
    try:
        api_module = importlib.import_module(api_module_name)
    except ImportError, e:
        #this is only import error, not necessary to log the trace
        log.exception(e)
        log.warn('module {0} is not found'.format(api_module_name))
        return None
    for attr_name in dir(api_module):
        app = getattr(api_module, attr_name)
        if isinstance(app, Application):
            log.info('{0} found in {1}'.format(attr_name, api_module_name))
            app.module_name = api_module_name
            return app
    log.warn('no application found in {0}'.format(api_module_name))
    return None


def init_app(app, app_type='api'):
    if app is None:
        return None
    if app_type == 'api':
        app.isapi = True
        default_error_handler = handler.api_default_error_handler
        error_handlers = handler.api_error_handlers
    else:
        app.isapi = False
        default_error_handler = handler.page_default_error_handler
        error_handlers = handler.page_error_handlers
    if default_error_handler is not None and not hasattr(app, '_default_error_handler'):
        app._default_error_handler = default_error_handler
    app.error_handler.update(error_handlers or {})
    return app


def find_applications(base_module_name):
    api_app = get_application('{0}.api'.format(base_module_name))
    page_app = get_application('{0}.page'.format(base_module_name))
    api_app = init_app(api_app, app_type='api')
    page_app = init_app(page_app, app_type='page')
    return api_app, page_app


def get_root_app():
    api_app, page_app = find_applications('apps.{0}'.format(get_root_name()))
    if api_app is None and page_app is None:
        return Application()
    if api_app is None:
        return page_app
    if page_app is None:
        page_app = Application()
    page_app.mount('/api', api_app)
    return page_app

def mount_sub_apps(root):
    app_names = get_app_names()
    version = get_version()
    if len(version) != 0:
        version = "/" + version
    for app_name in app_names:
        api_app, page_app = find_applications('apps.{0}'.format(app_name))
        
        if api_app is not None:
            root.mount('{1}/{0}/api'.format(app_name, version), api_app)
        if page_app is not None:
            root.mount('{1}/{0}'.format(app_name, version), page_app)


def init_root_app():
    root = get_root_app()
    mount_sub_apps(root)
    if hasattr(root, '__post_init__'):
        root.__post_init__()
    return root


def main():
    root = init_root_app()
    run(app=root,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reloader=settings.SERVER_RELOAD,
        debug=settings.SERVER_DEBUG)


if __name__ == '__main__':
    main()
else:
    application = init_root_app()
