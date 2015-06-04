#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
page api
@author: Shao Guojian
'''

import os
from core import Application, make_app_wrappers, static_file, redirect
from core.settings import settings
from core import request
from apps import get_app_names, get_app_dirs_dict, get_root_dir
#from common.auth import no_auth, get_token_from_request

app = Application()
get, post, default_error = make_app_wrappers(app, ['get', 'post', 'default_error'])

app_dir_dict = get_app_dirs_dict()
root_dir = get_root_dir()
app_names = get_app_names()

# useless in production mode, because nginx will override these rules
if settings.ENV_MODE == 'development':
    print "development mode start"
    @get('/static/<filename:path>')
    def serve_static(filename):
        return static_file(filename, root=os.path.join(root_dir, 'static'))


    @get('/')
    @get('/index')
    @get('/index.html')
    def serve_index():
        #token = get_token_from_request(request)
        #if token is None:
        #    return static_file('index.html', root=os.path.join(root_dir, 'html'))
        #else:
        #    redirect('/device/', 302)
        return "500"
    
    @get('/<page>.html')
    def serve_page(page):
        return static_file('{0}.html'.format(page), root=os.path.join(root_dir, 'html'))

    @get('/<app>/static/<filename:path>')
    def serve_app_static(app, filename):
        return static_file(filename, root=os.path.join(app_dir_dict.get(app, root_dir), 'static'))

    @get('/<app>/')
    @get('/<app>/index')
    @get('/<app>/index.html')
    def serve_app_index(app):
        return static_file('index.html', root=os.path.join(app_dir_dict.get(app, root_dir), 'html'))
    
    @get('/<app>/<page>.html')
    def serve_app_page(app, page):
        return static_file('{0}.html'.format(page), root=os.path.join(app_dir_dict.get(app, root_dir), 'html'))
    
    # deprecate: this will generate dynamic rules other than static rules
    # only redirect apps request, do not redirect all one-depth request like /abc, /hello
    @get('/<app:re:({0})>'.format('|'.join(get_app_names())))
    def redirect_app_index(app):
        return redirect('/{0}/'.format(app), 302)
    
    @get('/hello')
    def hello():
        return 'hello from root page'
            
    @get('/upload')
    def show_upload():
        return '''<html>
        <body>
            <form action="/api/upload" method="post" enctype="multipart/form-data">
                <input name="file" type="file"/>
                <input type="submit" value="submit"/>
            </form>
        </body>
        </html>
        '''


    @get('/testlogin')
    def show_login():
        return '''
        <html>
            <body>
                <form action="/api/login" method="post">
                    <input name="username" type="text"/>
                    <input name="password" type="password"/>
                    <input type="submit" value="Submit" />
                </form>
            </body>
        </html>
        '''
