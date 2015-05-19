#!/usr/bin/env python

# SWIG RPM package should be installed before installing the
# M2crypto module

import os
import json
from M2Crypto import RSA, EVP
import base64
import hashlib

cwd = os.path.dirname(__file__)

PRIVATE_KEY = os.path.join(cwd, "private.key")
pkey = RSA.load_key(PRIVATE_KEY)

def signature(content):
    MD5 = hashlib.md5()
    MD5.update(content)
    MD5string = MD5.digest()
    sign = pkey.private_encrypt(MD5string, RSA.pkcs1_padding)
    return base64.b64encode(sign)

def default_encoder(obj):
    return obj.__json__()

def make_signature_response(out):
    if not isinstance(out, dict):
        return out
    d = json.dumps(out, default=default_encoder)
    ret = json.loads(d)
    ret["signature"] = signature(d)
    return ret
    
