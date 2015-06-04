#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Sep 15, 2011

@author: mengchen
'''
from common.transcode import ffmpegutil
from common.transcode.errors import TranscodeError
from common.types import Dict
import doctest
import logging
import re

log = logging.getLogger(__name__)

class FFmpegOutputParser(object):
    def parse(self, output):
        lines = output.split('\n')
        meta = Dict(videoStream=None, audioStream=None)
        for line in lines:
            line = line.strip()
            input = self._parse_input(line)
            if input is not None:
                meta.update(input)
            duration = self._parse_duration(line, meta)
            if duration is not None:
                meta.update(duration)
            if meta.videoStream is None:
                meta.videoStream = self._parse_vs(line)
            if meta.audioStream is None:
                meta.audioStream = self._parse_as(line)
        return meta
    
    def _parse_input(self, line):
        '''
        >>> p = FFmpegOutputParser()
        
        not matched:
        >>> p._parse_input('') is None
        True
        
        flv
        >>> p._parse_input("Input #0, flv, from '1.flv':")
        {'type': 'flv'}
        
        mp4
        >>> p._parse_input("Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '1.mp4':")
        {'type': 'mp4'}
        
        mpeg
        >>> p._parse_input("Input #0, mpeg, from '2.mpg':")
        {'type': 'mpeg'}
        
        unknown type
        >>> p._parse_input("Input #0, image2, from 'logo.png':")
        {'type': 'n/a'}
        '''
        m = re.match('Input #0, (.*), from .*', line)
        if m is None:
            return None
        types = m.group(1)
        known_types = ['asf', 'avi', 'flv', 'mp4', 'mpeg', 'rm']
        for t in known_types:
            if t in types:
                return Dict(type=t)
        else:
            return Dict(type='n/a')
            
    def _parse_duration(self, line, meta):
        '''
        >>> p = FFmpegOutputParser()
        >>> meta = Dict()

        not matched:
        >>> m = p._parse_duration('', meta)
        >>> hasattr(meta, 'duration')
        False
        >>> hasattr(meta, 'bitrate')
        False

        normal situation:
        >>> p._parse_duration('Duration: 01:30:15.66, start: 3.000000, bitrate: 99 kb/s', meta)
        >>> meta.duration
        5415660
        >>> meta.kbps
        99
        
        no start:
        >>> p._parse_duration('Duration: 00:01:40.03, bitrate: 705 kb/s', meta)
        >>> meta.duration
        100030
        >>> meta.kbps
        705
        
        bitrate not available
        >>> p._parse_duration('Duration: 00:00:15.70, start: 0.000000, bitrate: N/A', meta)
        >>> meta.kbps
        0
        '''
        m = re.match('Duration: ([^,]*),.*bitrate: (\\d*).*', line)
        if not m:
            return None
        duration = m.group(1)
        bitrate = m.group(2)

        if re.match('\\d{2}:\\d{2}:\\d{2}.\\d{1,2}', duration):
            meta.duration = ffmpegutil.str_to_millis(duration)
        else:
            meta.duration = 0
        meta.kbps = 0 if bitrate == '' else int(bitrate)
    
    def _parse_vs(self, line):
        '''
        >>> p = FFmpegOutputParser()
        
        not matched:
        >>> vs = p._parse_vs('')
        >>> vs is None
        True
        
        normal situation:
        >>> vs = p._parse_vs('Stream #0.1: Video: rv30, yuv420p, 200x164, 36 kb/s, 12.05 fps, 12 tbr, 1k tbn, 12 tbc')
        >>> vs.type
        'rv30'
        >>> vs.width
        200
        >>> vs.height
        164
        >>> vs.kbps
        36
        >>> vs.frameRate == 12.05
        True
        
        no frame rate
        >>> vs = p._parse_vs('Stream #0.1(chi): Video: wmv3, yuv420p, 320x240, 65 kb/s, 15 tbr, 1k tbn, 1k tbc')
        >>> vs.frameRate
        0
        
        video type has space and braces
        >>> vs = p._parse_vs('Stream #0.0(und): Video: h264 (Constrained Baseline), yuv420p, 480x320, 252 kb/s, 24.01 fps, 24 tbr, 30k tbn, 59.94 tbc')
        >>> vs.type
        'h264'
        
        video type has 0x1 which may be mistaken as wi/hi
        >>> vs = p._parse_vs('Stream #0.0[0x1e0]: Video: mpeg1video, yuv420p, 352x288 [PAR 178:163 DAR 1958:1467], 1150 kb/s, 31.52 fps, 25 tbr, 90k tbn, 25 tbc')
        >>> vs.type
        'mpeg1video'
        >>> vs.width
        352
        >>> vs.height
        288
        '''
        m = re.match('Stream #.*?: Video: (?P<type>.+?), (?P<remain>.+)', line)
        if m is None:
            return None
        
        vs = Dict()
        
        # type may contain spaces and braces, e.g., "h264 (Constrained Baseline)"
        vs.type = m.group('type').split(' ')[0]
        remain = m.group('remain')
        
        m = re.search(', (\\d+)x(\\d+)[, ]', remain)
        vs.width = int(m.group(1))
        vs.height = int(m.group(2))
        
        m = re.search(', (\\d+) kb/s,', remain)
        vs.kbps = int(m.group(1)) if m else 0
        
        m = re.search(', ([\\.\\d]+) fps,', remain)
        vs.frameRate = 0 if m is None else float(m.group(1))
        
        return vs
    
    def _parse_as(self, line):
        '''
        >>> p = FFmpegOutputParser()
        
        not matched:
        >>> s = p._parse_as('')
        >>> s is None
        True
        
        normal situation:
        >>> s = p._parse_as('Stream #0.0: Audio: wmav2, 44100 Hz, 2 channels, s16, 64 kb/s')
        >>> s.type
        'wmav2'
        >>> s.channels
        2
        >>> s.kbps
        64
        >>> s.sampleRate
        44100
        
        mono channel
        >>> s = p._parse_as('Stream #0.1: Audio: aac, 44100 Hz, mono, s16, 64 kb/s')
        >>> s.channels
        1
        
        2 channels
        >>> s = p._parse_as('Stream #0.1: Audio: aac, 44100 Hz, 2 channels (FC), s16, 32 kb/s')
        >>> s.channels
        2
        
        stereo channels
        >>> s = p._parse_as('Stream #0.0: Audio: wmav2, 44100 Hz, 2 channels, s16, 64 kb/s')
        >>> s.channels
        2
        
        5.1 channels
        >>> s = p._parse_as('Stream #0.1: Audio: ac3, 48000 Hz, 5.1, s16, 384 kb/s')
        >>> s.channels
        6
        
        channels with braces
        >>> s = p._parse_as('Stream #0.1: Audio: aac, 44100 Hz, 2 channels (FC), s16, 47 kb/s')
        >>> s.channels
        2
        
        no kbps
        >>> s = p._parse_as('Stream #0.1(eng): Audio: mp3, 11025 Hz, 1 channels, s16')
        >>> s.kbps
        0
        
        invalid audio stream caused by flvtool++
        >>> s = p._parse_as('Stream #0.0: Audio: [0][0][0][0] / 0x0000, 0 channels')
        >>> s is None
        True
        
        default audio stream
        >>> s = p._parse_as('Stream #0.1(eng): Audio: dca (DTS), 48000 Hz, 5.1, s16, 1536 kb/s (default)')
        >>> s.kbps
        1536
        '''
        m = re.match('Stream #.*?: Audio: (.+)', line)
        if m is None:
            return None
        fields = m.group(1)
        if '0 channels' in fields:
            # invalid metadata caused by flvtool++
            return None
        fields = fields.split(', ')
        
        s = Dict()
        s.type = fields[0]
        s.sampleRate = int(fields[1][:-3]) # 44100 Hz
        if len(fields) == 5:
            end = fields[4].find(' kb/s')
            s.kbps = int(fields[4][:end])
        else:
            s.kbps = 0
        channels = fields[2]
        if channels == 'mono':
            s.channels = 1
        elif channels == 'stereo':
            s.channels = 2
        elif channels.find(' channel')!=(-1):
            s.channels = int(channels[:1])
        elif re.match('\\d\\.\\d', channels):
            s.channels = int(channels[:1]) + int(channels[2:3])
        else:
            logging.warn('Failed to get audio channels from source video metadata.')
            raise TranscodeError('Failed to get audio channels from source video metadata.')
        
        return s
    
if __name__ == '__main__':
    doctest.testmod()
    