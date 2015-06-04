#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Dec 19, 2011

@author: mengchen
'''
from common.log import log_enter, log_error, log_return
from common.util import stringutil, modutil
from common.web import handlers, resps
from common.web.context import Context
from common.web.resps import Response
import logging
import os
import sys

log = logging.getLogger(__name__)

def coor_maker(base_class=object):
    class _Coor(base_class):
        context_class = Context
        
        @log_enter('Handling url {path} ...')
        @log_return('Handle url {path} successfully.', 'ret.code == "200 OK"')
        @log_return('Failed to handle url {path}.', 'ret.code != "200 OK"')
        @log_return('Response is "{ret.body}".')
        @log_error('Failed to handle url {path}.', exc_info=True)
        def handle(self, path):
            try:
                path = stringutil.u2s(path)
                handler = self._load_handler(path)
                headers = self._read_headers()
                cookies = self._read_cookies()
                fields = self._read_fields()
                for k, v in fields.items():
                    log.info('Arg %s=%s' % (k, v))
                with self._build_context(path, fields, headers, cookies) as ctx:
                    ctx.header('Cache-Control', 'max-age=0,no-cache,no-store')
                    return handler.handle(fields)
            except Response, resp:
                return resp

        def _build_context(self, path, fields, headers, cookies):
            ctx = self.context_class()
            ctx.request_headers = headers
            ctx.request_cookies = cookies
            return ctx
        
        def _extract_mod_name(self, path):
            path = path.lstrip('/')
            path = path.replace('/', '.')
            parts = path.rsplit('.', 1)
            return 'handlers' if len(parts) == 1 else parts[0] + '.handlers'
        
        def _import_mod(self, path):
            modname = self._extract_mod_name(path)
            return modutil.import_module(modname)
        
        @log_error('Handler for {path} cannot be found.')
        def _load_handler(self, path):
            try:
                self._import_mod(path)
                return handlers.get_handler(path)
            except:
                if path.endswith('/'):
                    raise Response(resps.STATUS_404, '')
                else:
                    try:
                        self._load_handler(path + '/')
                    except:
                        raise Response(resps.STATUS_404, '')
                    raise Response(resps.STATUS_301, '', { 'Location': path + '/' })
                
        def _read_cookies(self):
            return {}

        def _read_fields(self):
            raise NotImplementedError()
        
        def _read_headers(self):
            return {}
        
        def _read_headers_from_dict(self, d):
            headers = {}
            for k, v in d.items():
                if k.startswith('HTTP_'):
                    k = k[len('HTTP_'):].replace('_', '-').upper()
                    headers[k] = v
            return headers
    return _Coor

if modutil.exists('web'):
    import web
    class WebPyCoor(coor_maker()):
        def GET(self, path):
            resp = self.handle(path)
            return self._process_resp(resp)
    
        def POST(self, path):
            resp = self.handle(path)
            return self._process_resp(resp)
        
        def _read_fields(self):
            return web.input()
        
        def _read_headers(self):
            return self._read_headers_from_dict(web.ctx.env)
        
        def _process_resp(self, resp):
            web.ctx.status = resp.code
            for k, v in resp.headers.items():
                web.header(k, v)
            return resp.body
    
if modutil.exists('django'):
    from django.conf.urls.defaults import patterns, url
    from django.core.management import ManagementUtility
    from django.http import HttpResponse
    import django.core.handlers.wsgi
    import threading
    from common.util import vtxutil

    class DjangoCoor(coor_maker()):
        data = threading.local()
        
        @property
        def request(self):
            return DjangoCoor.data.value
        
        @request.setter
        def request(self, value):
            DjangoCoor.data.value = value
        
        def __call__(self, request):
            self.request = request
            resp = self.handle(request.path)
            return self._process_resp(resp)
        
        def _read_fields(self):
            fields = dict(self.request.REQUEST)
            fields.update(self.request.FILES.items())
            return fields
        
        def _read_headers(self):
            return self._read_headers_from_dict(self.request.META)
        
        def _process_resp(self, resp):
            r = HttpResponse(resp.body)
            r.status_code = resp.code
            for k, v in resp.headers.items():
                r[k] = v
            return r

    DEBUG = False
    FORCE_SCRIPT_NAME = ''
    MIDDLEWARE_CLASSES = ()
    ROOT_URLCONF = __name__
    urlpatterns = None
    FILE_UPLOAD_TEMP_DIR = vtxutil.get_file_from_fs('tmp')
    if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
        os.makedirs(FILE_UPLOAD_TEMP_DIR)
    FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.TemporaryFileUploadHandler",)

    def run_server(coor=None):
        _run(coor, ['runserver', '8080'])
        
    def run_fcgi(coor=None):
        _run(coor, ['runfcgi', 'socket=/tmp/fastcgi.socket-0'])
        
    def _run(coor, argv):
        global urlpatterns
        urlpatterns = patterns('',
            url('.*', coor or DjangoCoor())
        )
        os.environ['DJANGO_SETTINGS_MODULE'] = __name__
        utility = ManagementUtility(sys.argv[:1] + argv)
        utility.execute()
    
    def create_wsgi_app(coor=None):
        global urlpatterns
        urlpatterns = patterns('',
            url('.*', coor or DjangoCoor())
        )
        os.environ['DJANGO_SETTINGS_MODULE'] = __name__
        return django.core.handlers.wsgi.WSGIHandler()
    