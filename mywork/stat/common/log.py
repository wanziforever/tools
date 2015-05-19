#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on Oct 28, 2011

@author: mengchen
'''
from common.types import Dict, Function
from common.util import fileutil
from logging import Filter
import doctest
import logging
import logging.handlers
import os
import re

logging.getLogger().setLevel(logging.INFO) # defaults to INFO level

def add_console_handler(level, format='%(message)s'):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(format))
    logging.getLogger().addHandler(handler)
    
def add_file_handler(file, level, need_rotate=False, format='[%(asctime)s] [%(levelname)s] [%(process)d:%(threadName)s] [%(name)s:%(funcName)s:%(lineno)d]\n%(message)s'):
    # create parent dir if not exist
    dir = os.path.dirname(file)
    fileutil.create_dir_if_not_exist(dir)
        
    # add handler
    logger = logging.getLogger()
    if not need_rotate:
        info_file_handler = logging.FileHandler(file)
    else:
        info_file_handler = logging.handlers.TimedRotatingFileHandler(file, 
            when='D', interval=1, backupCount=30)
    info_file_handler.setLevel(level)
    info_file_handler.setFormatter(logging.Formatter(format))
    logger.addHandler(info_file_handler)

def set_level(level):
    logger = logging.getLogger()
    logger.setLevel(level)
    
class LogDecorator(Function):
    DEFAULT_LEVEL = logging.DEBUG
    LEVEL_MAPPING = {
            'DEBUG' : logging.DEBUG,
            'INFO' : logging.INFO,
            'WARN' : logging.WARN,
            'ERROR' : logging.ERROR,
            'CRITICAL' : logging.CRITICAL,
            'D' : logging.DEBUG,
            'I' : logging.INFO,
            'W' : logging.WARN,
            'E' : logging.ERROR,
            'C' : logging.CRITICAL,
    }
    
    def __init__(self, expression, condition='True', **kw):
        super(LogDecorator, self).__init__()
        self._level, self._msg = self._parse_expression(expression)
        self._condition = condition
        self._extra_kw = kw
    
    def _evaluate(self, vars):
        '''
        >>> LogDecorator('aaa')._evaluate({})
        (True, 'aaa')
        >>> LogDecorator('aaa', '1 == 2')._evaluate({})
        (False, None)
        '''
        vars = Dict(vars)
        vars.os = os
        condition = eval(self._condition, vars)
        if condition:
            return True, self._evaluate_message(vars)
        else:
            return False, None
    
    def _evaluate_message(self, vars):
        '''
        >>> LogDecorator('aaa')._evaluate_message({})
        'aaa'
        >>> LogDecorator('Id is {id}.')._evaluate_message({'id':1})
        'Id is 1.'
        >>> LogDecorator('Id is {user.id}.')._evaluate_message({'user':Dict(id=1)})
        'Id is 1.'
        >>> LogDecorator('Id is {user.id}.')._evaluate_message({'user':Dict(id=1)})
        'Id is 1.'
        >>> LogDecorator('File existance: {os.path.exists(path)}.')._evaluate_message({'path':'.','os':os})
        'File existance: True.'
        >>> LogDecorator('Id is {!@#$%}.')._evaluate_message({})
        'Id is {error:!@#$%}.'
        '''
        def _evaluate(matcher):
            expression = matcher.group(1)
            try:
                value = eval(expression, vars)
                return str(value)
            except:
                return '{error:%s}' % expression
        return re.sub('\\{(.+?)\\}', _evaluate, self._msg)
    
    def _log(self, vars):
        condition, msg = self._evaluate(vars)
        if condition:
            logger = logging.getLogger(self._func.__module__)
            self._add_filter(logger)
            logger.log(self._level, msg, **self._extra_kw)
            
    def _add_filter(self, logger):
        decorator = self
        class _Filter(Filter):
            def filter(self, record):
                record.funcName = decorator.__name__
                record.lineno = decorator.get_original_lineno()
                return 1
        logger.addFilter(_Filter())
            
    def _parse_expression(self, expression):
        m = re.match('\\[(\\w+)\\](.*)', expression)
        if m is None:
            return self.DEFAULT_LEVEL, expression.strip()
        level, msg = m.groups()
        level = LogDecorator.LEVEL_MAPPING.get(level.upper(), logging.WARN) # default to warn if level is invalid
        msg = msg.strip()
        return level, msg
        
class log_enter(LogDecorator):
    def _call(self, *args, **kw):
        vars = self._convert_to_arg_dict(*args, **kw)
        self._log(vars)
        return super(log_enter, self)._call(*args, **kw)
    
class log_exit(LogDecorator):
    LOG_ON_RETURN = True
    LOG_ON_ERROR = True
    
    def _call(self, *args, **kw):
        vars = self._convert_to_arg_dict(*args, **kw)
        try:
            ret = super(log_exit, self)._call(*args, **kw)
            if self.LOG_ON_RETURN:
                vars.ret = ret
                self._log(vars)
            return ret
        except Exception, e:
            if self.LOG_ON_ERROR:
                vars.e = e
                self._log(vars)
            raise
    
class log_return(log_exit):
    LOG_ON_RETURN = True
    LOG_ON_ERROR = False
    
class log_error(log_exit):
    LOG_ON_RETURN = False
    LOG_ON_ERROR = True
    DEFAULT_LEVEL = logging.WARN

if __name__ == '__main__':
    doctest.testmod()
    