#!/usr/bin/env python
#-*- coding: utf-8 -*-

import textwrap
teststr = "asdfasdf asdfasdfad a asdfasdf adsfasdf asdfa sdf\n adfadfasdfadf asdfa34u' afasdfa"
teststr = "fail to verify ++++<Facet> title:铁甲舰上的男人们, typecode=1003, id=90010237192, pic=http://picture.cntv.hismarttv.com/images/20150504081147165814.jpg"

s = textwrap.wrap(teststr, width=80, replace_whitespace=False)
print "\n".join(s)

lines = teststr.splitlines()

print lines

s = []
for l in lines:
    s += textwrap.wrap(l, drop_whitespace=True)
print "\n".join(s)

print
print
for l in lines:
    print textwrap.fill(l.strip(), width=80)
