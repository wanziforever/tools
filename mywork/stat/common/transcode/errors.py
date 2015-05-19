#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jan 9, 2012

@author: mengchen
'''
from common.error.errors import CodedError

class TranscodeError(CodedError):
    def __init__(self, msg='Transcode error.'):
        super(TranscodeError, self).__init__('TRANSCODE_ERROR', msg)
        
class FFmpegError(TranscodeError):
    def __init__(self, msg='FFmpeg error.'):
        super(FFmpegError, self).__init__(msg)
        self.code = 'FFMPEG_ERROR'

class FlvtoolError(TranscodeError):
    def __init__(self, msg='Flvtool++ error.'):
        super(FlvtoolError, self).__init__(msg)
        self.code = 'FLVTOOL_ERROR'

class QtfaststartError(TranscodeError):
    def __init__(self, msg='Qtfaststart error.'):
        super(QtfaststartError, self).__init__(msg)
        self.code = 'QTFASTSTART_ERROR'

class SegmenterError(TranscodeError):
    def __init__(self, msg='Segmenter error.'):
        super(SegmenterError, self).__init__(msg)
        self.code = 'SEGMENTER_ERROR'
        