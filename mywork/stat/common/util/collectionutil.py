#!/usr/bin/env python
# -*- coding: utf-8 -*-
import doctest

def categorize(objects, attr):
    '''
    >>> from common.types import Dict
    >>> l = [Dict(type=1), Dict(type=1), Dict(type=2)]
    >>> categories = categorize(l, 'type')
    >>> len(categories[1])
    2
    >>> len(categories[2])
    1
    '''
    categories = {}
    for o in objects:
        key = getattr(o, attr)
        if key in categories:
            categories[key].append(o)
        else:
            categories[key] = [o]
    return categories

if __name__ == '__main__':
    doctest.testmod()
    