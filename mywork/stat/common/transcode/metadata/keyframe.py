#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.types import Dict
from common.util import fileutil
from mako.template import Template
import os
import subprocess

class FrameParser(object):
    def parse(self, path):
        process = subprocess.Popen('ffprobe -show_frames -print_format csv -i %s|grep "frame,video,1"' % path,
                shell=True, stdout=subprocess.PIPE)
        return self._parse_output(process.stdout)
    
    def _parse_output(self, stdout):
        keyframes = []
        for line in stdout.readlines():
            line = line.rstrip('\r\n')
            ss = line.split(',')
            time = long(float(ss[4]) * 1000)
            bytes = long(ss[7])
            keyframes.append(Dict(time=time, bytes=bytes))
        return keyframes
    
def _parse_flvtool_output(output):
    in_bytes = False
    in_time = False
    bytes_list = []
    time_list = []
    for line in output.splitlines():
        line = line.strip()
        if line == 'filepositions: {':
            in_bytes = True
        elif line == 'times: {':
            in_time = True
        elif line == '}':
            in_bytes = False
            in_time = False
        elif in_bytes:
            bytes_list.append(long(float(line)))
        elif in_time:
            time_list.append(long(float(line) * 1000))
    return [Dict(bytes=bytes_list[i], time=time_list[i]) for i in range(len(bytes_list))]

def _generate_xml(rendition_id, keyframes, xml_path):
    template_path = os.path.join(os.path.dirname(__file__), 'metadata.xml')
    xml = Template(filename=template_path).render(renditionId=rendition_id, keyframes=keyframes)
    fileutil.writefile(xml_path, xml)
    
def generate_meta_xml(rendition_id, flvtool_output, xml_path):
    keyframes = _parse_flvtool_output(flvtool_output)
    _generate_xml(rendition_id, keyframes, xml_path)
