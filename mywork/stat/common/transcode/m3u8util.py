#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.util import fileutil
from mako.template import Template
import os

def generate_m3u8(m3u8_path, segments, segment_seconds, end=True):
    template_path = os.path.join(os.path.dirname(__file__), 'template.m3u8')
    m3u8 = Template(filename=template_path).render(segments=segments, segmentSeconds=segment_seconds, end=end)
    fileutil.writefile(m3u8_path, m3u8)
    