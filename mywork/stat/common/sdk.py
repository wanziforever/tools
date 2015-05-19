#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Nov 10, 2011

@author: mengchen
'''
from common import json2
from common.error.errors import CodedError, AuthError
from common.log import log_enter, log_return, log_error
from common.types import Dict
from common.util import httputil
import doctest
import urllib

class Client(object):
    def __init__(self, url='http://api.video-tx.com/', token=None, oauth_token=None):
        '''
        Create a Client object.
        
        Args:
          url: API url, default to 'http://api.video-tx.com/'.
          token: Token string, default to None.
          
        >>> c = Client()
        >>> c.url
        'http://api.video-tx.com/'
        
        >>> c = Client('http://api.video-tx.com')
        >>> c.url
        'http://api.video-tx.com/'
        
        >>> c = Client('http://api.video-tx.com/', '123')
        >>> c.token
        '123'
        '''
        if not url.endswith('/'):
            url = url + '/'
        self.url = url
        self.token = token
        self.oauth_token = oauth_token

    def __getattr__(self, attr):
        def _wrapper(**kw):
            if 'file' in kw:
                return self._call_upload(attr, **kw)
            else:
                return self._call(attr.replace('_', '/'), **kw)
        return _wrapper
    
    @log_return('Token requested: {self.token}.')
    def request_token(self, email, passwd):
        resp = self._call('login', email=email, passwd=passwd)
        self.token = resp.token
        if not self.token:
            raise CodedError('LOGIN_FAILED', 'Invalid email or password.')
        
    @log_enter('Uploading file {file} ...')
    @log_return('Upload video succeeded. Video id is {ret.id}.')
    @log_error('Failed to upload video.')
    def upload_video(self, file, folder_id, title):
        r = self.createVideo(folderId=folder_id, title=title)
        rslt = httputil.upload(r.uploadUrl, file)
        if 'error' in rslt:
            raise CodedError(rslt.error, rslt.message)
        return json2.loads(r.media)

    def _call(self, api, **fields):
        resp_headers = Dict.get_and_del_from_dict(fields, 'resp_headers', {})
        if api.startswith('public/'):
            # should use GET
            url = self.url + api + '?' + urllib.urlencode(fields)
            fields = None
        else:
            # should use POST
            url = self.url + api
        headers = self._get_token_header(api)
        resp = httputil.curl(url, fields, headers, use_json=True, resp_headers=resp_headers)
        self._check_error(resp)
        return resp

    def _call_upload(self, api, **fields):
        file = fields['file']
        del fields['file']
        headers = self._get_token_header(api)
        ret = httputil.upload(self.url + api, file, fields, headers, True)
        self._check_error(ret)
        return ret
        
    def _check_error(self, ret):
        if hasattr(ret, 'error'):
            if hasattr(ret, 'location') and ret.location is not None:
                raise CodedError(ret.error, ret.message, location=ret.location)
            else:
                raise CodedError(ret.error, ret.message)

    def _get_token_header(self, api):
        '''
        should use vtx token if presented
        >>> c = Client('http://api.video-tx.com/', '111')
        >>> c._get_token_header('createVideo')
        {'Authorization': 'Token 111'}
        
        should use oauth2 token if:
        a) vtx token is missing
        b) oauth2 token is available
        >>> c = Client('http://api.video-tx.com/', oauth_token='222')
        >>> c._get_token_header('createVideo')
        {'Authorization': 'OAuth2 222'}
        
        should raise error if neither token is available
        >>> c = Client('http://api.video-tx.com/')
        >>> c._get_token_header('createVideo')
        Traceback (most recent call last):
        ...
        AuthError: [AUTH_FAILED] No token found.
        
        for public apis,
        no token header is needed
        >>> c._get_token_header('public/video') is None
        True
        '''
        if api == 'login' or api.startswith('public/'):
            return None
        if self.token is not None:
            return { 'Authorization' : 'Token %s' % self.token }
        elif self.oauth_token is not None:
            return { 'Authorization' : 'OAuth2 %s' % self.oauth_token }
        else:
            raise AuthError('No token found.')

if __name__=='__main__':
    doctest.testmod()
    