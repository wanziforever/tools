#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
hash utility
@author: Guojian Shao
"""

import hashlib
import doctest

_SALT = r'*$&)(*&Q#RSDFJLj;asdf-'

def md5(raw, salt=''):
    m = hashlib.md5()
    m.update(raw + salt)
    return m.hexdigest()


def encode_password(raw, salt=_SALT):
    password = raw
    for i in range(10):
        p = md5(password, salt)
        password = p
    return password

