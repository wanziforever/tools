# -*- coding: UTF-8 -*-
from common.error.errors import BadArgValueError
from common.log import log_enter, log_return
from common.transcode.errors import TranscodeError
from common.transcode.ffmpegutil import FFmpegWrapper
from common.transcode.metadata import keyframe
from common.transcode.metadata.ffmpegparser import FFmpegOutputParser
from common.transcode.metadata.keyframe import FrameParser, generate_meta_xml
import doctest
import logging
import os

log = logging.getLogger(__name__)

def extract_media_meta(path, type):
    if type == 'video':
        return extract_video_meta(path)
    elif type == 'audio':
        return extract_audio_meta(path)
    else:
        raise BadArgValueError('type', type)
        
def extract_video_meta(path):
    meta = extract_meta(path)
    _verify_video_meta(meta)
    return meta

def extract_audio_meta(path):
    meta = extract_meta(path)
    _verify_audio_meta(meta)
    return meta

@log_enter('Extracting metadata from {path}.')
@log_return('Metadata is {ret}.')
def extract_meta(path):
    try:
        ffmpeg = FFmpegWrapper(path)
        ffmpeg.run() #@UnusedVariable
        log.debug('FFmpeg output: ' + ffmpeg.stderr)
        meta = FFmpegOutputParser().parse(ffmpeg.stderr)
        if meta is not None:
            meta.fileSize = os.path.getsize(path)
        _fix_meta(meta)
        return meta
    except TranscodeError:
        raise
    except Exception:
        log.exception('Failed to extract metadata from "%s".' % path)
        raise TranscodeError('Failed to extract metadata from source video file')
    
def _fix_meta(meta):
    '''
    metadata is None
    should not fix anything
    >>> _fix_meta(None)
    '''
    if meta is None:
        return
    if meta.videoStream is not None:
        if meta.videoStream.kbps == 0:
            _fix_video_kbps(meta)
    
def _fix_video_kbps(meta):
    '''
    >>> from common.types import Dict
    
    1000KB file for 10 seconds
    total bps is 800k
    minus audio bps 100k
    final video bps is 700k
    >>> meta = Dict(kbps=100, duration=10000, fileSize=1024000)
    >>> meta.videoStream = Dict(kbps=0)
    >>> meta.audioStream = Dict(kbps=100)
    >>> _fix_video_kbps(meta)
    >>> meta.videoStream.kbps
    700
    
    1000KB file for 10 seconds
    total bps is 800k
    and there is not audio stream
    final video bps is 800k
    >>> meta = Dict(kbps=100, duration=10000, fileSize=1024000)
    >>> meta.videoStream = Dict(kbps=0)
    >>> meta.audioStream = None
    >>> _fix_video_kbps(meta)
    >>> meta.videoStream.kbps
    800
    '''
    if meta.duration == 0:
        seconds = 2 #fix length is 0, default length is 2 seconds
    else:
        seconds = meta.duration / 1000.0
    meta.kbps = int(meta.fileSize * 8.0 / 1024 / seconds)
    akbps = 0 if meta.audioStream is None else meta.audioStream.kbps
    meta.videoStream.kbps = meta.kbps - akbps
    
def _verify_media_meta(meta):
    '''
    >>> from common.types import Dict
    
    normal situation
    >>> meta = Dict(duration=10000, kbps=800)
    >>> _verify_media_meta(meta)
    
    metadata is None
    >>> _verify_media_meta(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 无法解析上传文件的元数据。
    
    metadata has no duration
    >>> meta = Dict(kbps=800)
    >>> _verify_media_meta(meta) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 上传文件缺少时长元数据。
    
    metadata has no kbps
    >>> meta = Dict(duration=10000)
    >>> _verify_media_meta(meta) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 上传文件缺少码率元数据。
    '''
    if meta is None:
        raise TranscodeError(u'无法解析上传文件的元数据。')
    if meta.get('duration') is None:
        raise TranscodeError(u'上传文件缺少时长元数据。')
    if meta.get('kbps') is None:
        raise TranscodeError(u'上传文件缺少码率元数据。')
    
def _verify_video_meta(meta):
    '''
    >>> from common.types import Dict
    
    video stream is None
    >>> meta = Dict(videoStream=None)
    >>> _verify_video_meta(meta) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 文件不是有效的视频文件。
    
    audio stream is aac and more than 2 channels
    >>> meta = Dict(videoStream={}, audioStream=Dict(type='aac', channels=6))
    >>> _verify_video_meta(meta) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 不支持超过2声道的AAC音频流。
    '''
    _verify_media_meta(meta)
    if meta.videoStream is None:
        raise TranscodeError(u'文件不是有效的视频文件。')
    if meta.audioStream is not None and meta.audioStream.type == 'aac' and meta.audioStream.channels > 2:
        raise TranscodeError(u'不支持超过2声道的AAC音频流。')
    
def _verify_audio_meta(meta):
    '''
    >>> from common.types import Dict
    
    video stream is None
    >>> meta = Dict(audioStream=None)
    >>> _verify_audio_meta(meta) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 文件不是有效的音频文件。
    
    audio stream is aac and more than 2 channels
    >>> meta = Dict(videoStream={}, audioStream=Dict(type='aac', channels=6))
    >>> _verify_audio_meta(meta) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TranscodeError: 不支持超过2声道的AAC音频流。
    '''
    _verify_media_meta(meta)
    if meta.audioStream is None:
        raise TranscodeError(u'文件不是有效的音频文件。')
    if meta.audioStream.type == 'aac' and meta.audioStream.channels > 2:
        raise TranscodeError(u'不支持超过2声道的AAC音频流。')
    
if __name__ == '__main__':
    doctest.testmod()
    