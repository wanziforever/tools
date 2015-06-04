#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jul 6, 2011

@author: mengchen
'''
from PIL import Image #@UnresolvedImport
import doctest
import math
import os

MATCH_BOTH = 0
MATCH_WIDTH = 1
MATCH_HEIGHT = 2
MATCH_LARGER = 3
MATCH_SMALLER = 4

def crop_image(infile, outfile, size):
    im = Image.open(infile)
    if size[0] > im.size[0] or size[1] > im.size[1]:
        raise Exception('Specified size exceeds image size.')
    left = (im.size[0] - size[0]) / 2
    right = left + size[0]
    top = (im.size[1] - size[1]) / 2
    bottom = top + size[1]
    im = im.crop((left, top, right, bottom))
    format = _decide_format_from_ext(os.path.splitext(outfile)[1])
    im.save(outfile, format)
    
def get_image_size(file):
    im = Image.open(file)
    return im.size

def scale_image(infile, outfile, size, strategy):
    im = Image.open(infile)
    if strategy != MATCH_BOTH:
        xratio = size[0] * 1.0 / im.size[0]
        yratio = size[1] * 1.0 / im.size[1]
        if strategy == MATCH_WIDTH:
            ratio = xratio
        elif strategy == MATCH_HEIGHT:
            ratio = yratio
        elif strategy == MATCH_LARGER:
            ratio = min(xratio, yratio)
        elif strategy == MATCH_SMALLER:
            ratio = max(xratio, yratio)
        size = [int(math.ceil(e * ratio)) for e in im.size]
    im = im.resize(size, Image.ANTIALIAS)
    format = _decide_format_from_ext(os.path.splitext(outfile)[1])
    im.save(outfile, format)
    
def _decide_format_from_ext(ext):
    '''
    >>> _decide_format_from_ext('.bmp')
    'BMP'
    >>> _decide_format_from_ext('.jpeg')
    'JPEG'
    >>> _decide_format_from_ext('.jpg')
    'JPEG'
    '''
    format = ext[1:].upper()
    if format == 'JPG':
        format = 'JPEG'
    return format

if __name__ == '__main__':
    doctest.testmod()
    