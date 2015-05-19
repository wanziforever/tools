#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
db related utility
@author: Guojian Shao
"""

from sqlalchemy.orm.query import Query
from common.errors import BadArgTypeError
from common.types import Dict


def slice_query(q, start, length):
    if not isinstance(q, Query):
        raise BadArgTypeError('q', q.__class__, Query)
    return q.slice(start, start + length)

def page(q, start, length, process_data=True):
    data = slice_query(q, start, length).all()
    count = q.count()
    d = Dict()
    if process_data:
        d.data = rs2dict(data)
    else:
        d.data = data
    d.count = count
    d.start = start
    d.len = length
    return d

def row2dict(row):
    if row is None:
        return None
    d = Dict()
    for c in row.__table__.columns:
        d[c.name] = getattr(row, c.name)
    return d


def rs2dict(rs):
    if rs is None:
        return None
    if isinstance(rs, (list, tuple)):
        ret = []
        for row in rs:
            ret.append(row2dict(row))
        return ret
    else:
        return row2dict(rs)

