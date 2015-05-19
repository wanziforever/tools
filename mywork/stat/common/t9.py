#!/usr/bin/python
# -*- coding: utf-8 -*-
import itertools
import re

t9_dict = {'2':'\'abc\'', '3':'\'def\'', '4':'\'ghi\'', '5':'\'jkl\'', '6':'\'mno\'', '7':'\'pqrs\'', '8':'\'tuv\'', '9':'\'wxyz\''}

def get_cartesian_products_by_t9num(t9num):
    t9num = re.sub('[^2-9]', '', t9num)
    if t9num == '':
        return None
    else:
        t9num = ','.join([char for char in t9num])
        func = 'itertools.product(' + multiple_replace(t9num, t9_dict) + ')'
        cartesian_products = eval(func)
        return ["".join(product) for product in cartesian_products]

def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)
