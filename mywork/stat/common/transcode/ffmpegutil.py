#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Oct 13, 2011

@author: mengchen
'''
from common.error import validation
from common.transcode.errors import FFmpegError
from common.util import vtxutil, imageutil
from common.util.wrapper import Wrapper
import doctest
import re

class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def left(self):
        return self.x
    
    def right(self):
        return self.x + self.width
    
    def top(self):
        return self.y
    
    def bottom(self):
        return self.y + self.height
    
    def contains(self, r):
        '''
        >>> r = Rect(0, 0, 100, 100)
        
        rect is within r
        >>> r.contains(Rect(30, 30, 10, 10))
        True
        
        rect is out of r
        >>> r.contains(Rect(1000, 1000, 100, 100))
        False
        
        rect intersects with r
        >>> r.contains(Rect(50, 50, 100, 100))
        False
        '''
        return r.left() > self.left() and r.right() < self.right() \
                and r.top() > self.top() and r.bottom() < self.bottom()
        
    def intersect(self, r):
        '''
        calc intersection
        >>> r1 = Rect(0, 0, 200, 100)
        >>> r2 = Rect(100, 50, 200, 100)
        >>> r3 = r1.intersect(r2)
        >>> (r3.x, r3.y, r3.width, r3.height)
        (100, 50, 100, 50)
        
        no intersection
        >>> r4 = r1.intersect(Rect(1000, 1000, 100, 100))
        >>> r4 is None
        True
        '''
        intersects = self.left() < r.right() and self.right() > r.left() \
                and self.top() < r.bottom() and self.bottom() > r.top()
        if intersects:
            left = max(self.left(), r.left())
            right = min(self.right(), r.right())
            top = max(self.top(), r.top())
            bottom = min(self.bottom(), r.bottom())
            return Rect(left, top, right - left, bottom - top)
        else:
            return None
        
class FFmpegWrapper(Wrapper):
    @validation.required('infile')
    def __init__(self, infile, outfile=None):
        '''
        >>> w = FFmpegWrapper('in.avi')
        >>> w.cmd
        "ffmpeg -i 'in.avi'"
        '''
        super(FFmpegWrapper, self).__init__(None, None if outfile is None else FFmpegError)
        self.infile = infile
        self.outfile = outfile
        self.overwrite = True
        self.threads = 1
        self.start_time = None
        self.video_codec = None
        self.width = None
        self.height = None
        self.frame_rate = None
        self.video_kbps = None
        self.video_filter = None
        self.key_frame_rate = None
        self.h264_profile = None
        self.audio_codec = None
        self.audio_kbps = None
        self.audio_channels = None
        self.audio_sample_rate = None
        self.extra = None
        
    def run(self):
        self.cmd = self._build_cmd()
        super(FFmpegWrapper, self).run()
        
    def _build_arg(self, format, value):
        '''
        >>> w = FFmpegWrapper('in.avi', 'out.mp4')
        >>> w._build_arg('-c:v %s', 'libx264')
        ' -c:v libx264'
        >>> w._build_arg('-c:v %s', None)
        ''
        '''
        if value is None:
            return ''
        else:
            format = ' ' + format
            return format % value
        
    def _build_audio_args(self):
        '''
        >>> w = FFmpegWrapper('in.avi', 'out.mp4')
        >>> w.audio_codec = 'libfaac'
        >>> w.audio_kbps = 64
        >>> w.audio_channels = 2
        >>> w.audio_sample_rate = 44100
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:a libfaac -b:a 64k -ac 2 -ar 44100 out.mp4"
        '''
        cmd = ''
        if self.audio_codec:
            cmd += self._build_arg('-c:a %s', self.audio_codec)
            cmd += self._build_arg('-b:a %dk', self.audio_kbps)
            cmd += self._build_arg('-ac %d', self.audio_channels)
            cmd += self._build_arg('-ar %d', self.audio_sample_rate)
        return cmd

    def _build_video_args(self):
        '''
        >>> w = FFmpegWrapper('in.avi', 'out.mp4')
        
        basic args
        >>> w.video_codec = 'libx264'
        >>> w.video_kbps = 700
        >>> w.frame_rate = 15
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:v libx264 -b:v 700k -r 15.000 out.mp4"

        + width/height
        >>> w.width = 640
        >>> w.height = 480
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 out.mp4"
        
        + key frame rate
        >>> w.key_frame_rate = 1
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 -g 15 out.mp4"
        
        + H.264 profile
        >>> w.h264_profile = 'baseline'
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 -g 15 -vprofile baseline out.mp4"
        
        + video filter
        >>> w.video_filter = 'video filter here'
        >>> w._build_cmd()
        'ffmpeg -i \\\'in.avi\\\' -sn -y -threads 1 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 -g 15 -vprofile baseline -filter:v "video filter here" out.mp4'
        '''
        cmd = ''
        if self.video_codec:
            cmd += self._build_arg('-c:v %s', self.video_codec)
            cmd += self._build_arg('-b:v %dk', self.video_kbps)
            if self.width and self.height:
                cmd += ' -s %dx%d' % (self.width, self.height)
            cmd += self._build_arg('-r %.3f', self.frame_rate)
            if self.key_frame_rate:
                cmd += self._build_arg('-g %d', self.key_frame_rate * self.frame_rate)
            cmd += self._build_arg('-vprofile %s', self.h264_profile)
            cmd += self._build_arg('-filter:v "%s"', self.video_filter)
        return cmd

    def _build_cmd(self):
        '''
        >>> w = FFmpegWrapper('in.avi', None)
        
        no output file
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi'"
        
        audio only
        >>> w.outfile = 'out.mp4'
        >>> w.audio_codec = 'libfaac'
        >>> w.audio_kbps = 64
        >>> w.audio_channels = 2
        >>> w.audio_sample_rate = 44100
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:a libfaac -b:a 64k -ac 2 -ar 44100 out.mp4"
        
        video + audio
        >>> w.video_codec = 'libx264'
        >>> w.video_kbps = 700
        >>> w.width = 640
        >>> w.height = 480
        >>> w.frame_rate = 15
        >>> w.key_frame_rate = 1
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 -g 15 -c:a libfaac -b:a 64k -ac 2 -ar 44100 out.mp4"
        
        with start time
        >>> w.start_time = 60000
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -ss 00:01:00.00 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 -g 15 -c:a libfaac -b:a 64k -ac 2 -ar 44100 out.mp4"
        
        with extra
        >>> w.extra = '-bt 1000000'
        >>> w._build_cmd()
        "ffmpeg -i 'in.avi' -sn -y -threads 1 -ss 00:01:00.00 -c:v libx264 -b:v 700k -s 640x480 -r 15.000 -g 15 -c:a libfaac -b:a 64k -ac 2 -ar 44100 -bt 1000000 out.mp4"
        '''
        cmd = "ffmpeg -i '%s'" % self.infile
        if self.outfile:
            cmd += ' -sn'
            if self.overwrite:
                cmd += ' -y'
            cmd += self._build_arg('-threads %d', self.threads)
            if self.start_time:
                cmd += self._build_arg('-ss %s', millis_to_str(self.start_time))
        cmd += self._build_video_args()
#        cmd += " -vf yadif=0:-1:0 " #for video deinterlace
        cmd += self._build_audio_args()
        cmd += self._build_arg('%s', self.extra)
        cmd += self._build_arg('%s', self.outfile)
        return cmd
    
def build_watermark_arg(watermark, vsize):
    # calc video rect & watermark rect
    wfile = vtxutil.get_file_from_fs(watermark.fileKey)
    wsize = imageutil.get_image_size(wfile)
    vrect = Rect(0, 0, vsize[0], vsize[1])
    offsetx, offsety = _calc_offset(watermark, wsize, vsize)
    wrect = Rect(offsetx, offsety, wsize[0], wsize[1])
    
    # build arg string
    source = _build_watermark_source(wrect, vrect, wfile)
    if source is None:
        return None
    overlay = _build_watermark_overlay(offsetx, offsety)
    return source + overlay
    
def _build_watermark_source(wrect, vrect, wfile):
    '''
    >>> vrect = Rect(0, 0, 480, 360)

    watermark completely within video rect
    >>> wrect = Rect(8, 8, 32, 32)
    >>> _build_watermark_source(wrect, vrect, 'logo.png')
    'movie=logo.png [wm];'
    
    watermark completely outside of video rect
    >>> wrect = Rect(500, 500, 32, 32)
    >>> _build_watermark_source(wrect, vrect, 'logo.png') is None
    True
    
    watermark intersects with video rect
    >>> wrect = Rect(460, 350, 32, 32)
    >>> _build_watermark_source(wrect, vrect, 'logo.png')
    'movie=logo.png, crop=20:10:0:0 [wm];'
    >>> wrect = Rect(-10, -20, 32, 32)
    >>> _build_watermark_source(wrect, vrect, 'logo.png')
    'movie=logo.png, crop=22:12:10:20 [wm];'
    '''
    intersection = wrect.intersect(vrect)
    if intersection is None:
        # watermark has no intersection with video, ignore it
        return None
    elif vrect.contains(wrect):
        # watermark completely within video rect
        return 'movie=%s [wm];' % wfile
    else:
        # watermark intersects with video rect
        cropx = intersection.left() - wrect.left()
        cropy = intersection.top() - wrect.top()
        return 'movie=%s, crop=%d:%d:%d:%d [wm];' % (wfile, intersection.width, intersection.height, cropx, cropy)

def _build_watermark_overlay(offsetx, offsety):
    '''
    >>> _build_watermark_overlay(10, 8)
    '[in][wm] overlay=10:8 [out]'
    >>> _build_watermark_overlay(-10, -8)
    '[in][wm] overlay=0:0 [out]'
    '''
    offsetx = max(offsetx, 0)
    offsety = max(offsety, 0)
    return '[in][wm] overlay=%d:%d [out]' % (offsetx, offsety)
    
def _calc_offset(watermark, wsize, vsize):
    '''
    >>> from common.types import Dict
    >>> w = Dict(alignment='TOP_LEFT', xmargin = 25, ymargin = 5)
    >>> _calc_offset(w, [30, 20], [400, 300])
    (25, 5)
    
    >>> w = Dict(alignment='TOP_RIGHT', xmargin = 25, ymargin = 5)
    >>> _calc_offset(w, [30, 20], [400, 300])
    (345, 5)

    >>> w = Dict(alignment='BOTTOM_LEFT', xmargin = 25, ymargin = 5)
    >>> _calc_offset(w, [30, 20], [400, 300])
    (25, 275)

    >>> w = Dict(alignment='BOTTOM_RIGHT', xmargin = 25, ymargin = 5)
    >>> _calc_offset(w, [30, 20], [400, 300])
    (345, 275)
    '''
    if 'LEFT' in watermark.alignment:
        xoffset = watermark.xmargin
    else:
        xoffset = vsize[0] - wsize[0] - watermark.xmargin
    if 'TOP' in watermark.alignment:
        yoffset = watermark.ymargin
    else:
        yoffset = vsize[1] - wsize[1] - watermark.ymargin
    return (xoffset, yoffset)

def str_to_millis(str):
    '''
    >>> str_to_millis('01:30:15.66')
    5415660
    '''
    m = re.match('(?P<hour>\\d{2}):(?P<min>\\d{2}):(?P<sec>\\d{2})\\.(?P<fraction>\\d{1,2})', str)
    hour = int(m.group('hour'))
    min = int(m.group('min'))
    sec = int(m.group('sec'))
    fraction = int(m.group('fraction').ljust(3, '0'))
    return hour * 3600 * 1000 + min * 60 * 1000 + sec * 1000 + fraction

def millis_to_str(millis):
    '''
    >>> millis_to_str(5415660)
    '01:30:15.66'
    '''
    hour = millis / 3600 / 1000
    millis -= hour * 3600 * 1000
    min = millis / 60 / 1000
    millis -= min * 60 * 1000
    sec = millis / 1000
    millis -= sec * 1000
    fraction = millis / 10
    return '%02d:%02d:%02d.%02d' % (hour, min, sec, fraction)

def parse_ffmpeg_error(stderr):
    u'''
    >>> stderr = '\\n'.join(['[mjpeg @ 0x25f23c0] Found EOI before any SOF, ignoring', '[image2 @ 0x25f0d40] Could not find codec parameters (Video: mjpeg, yuv420p)', '[movie @ 0x25f0ba0] Failed to find stream info'])
    >>> msg = parse_ffmpeg_error(stderr)
    >>> msg == u'无法解析视频水印，水印文件可能不是有效的图片'
    True
    '''
    for line in stderr.split('\n'):
        line = line.strip()
        if re.match('''\[image2 @ 0x.*\] Could not find codec parameters \(Video: .*\)''', line):
            return u'无法解析视频水印，水印文件可能不是有效的图片'
    return u'未知的FFmpeg错误'

if __name__ == '__main__':
    doctest.testmod()
    