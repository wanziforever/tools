#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Dec 19, 2011

@author: mengchen
'''
import doctest

STATUS_200 = '200 OK'
STATUS_301 = '301 Moved Permanently'
STATUS_302 = '302 Found'
STATUS_400 = '400 Bad Request'
STATUS_404 = '404 Not Found'
STATUS_500 = '500 Internal Server Error'

class Response(Exception):
    def __init__(self, code, body, headers={}, cookies={}):
        self.code = code
        self.body = body
        self.headers = headers
        self.cookies = cookies
        
class RedirectResponse(Response):
    def __init__(self, url):
        '''
        >>> r = RedirectResponse('/test2')
        >>> r.code
        '302 Found'
        >>> len(r.headers)
        1
        >>> r.headers['Location']
        '/test2'
        '''
        headers = { 'Location': url }
        super(RedirectResponse, self).__init__(STATUS_302, '', headers)
        
if __name__ == '__main__':
    doctest.testmod()
    