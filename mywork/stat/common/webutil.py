#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Dec 18, 2013
@author: wjj
'''
import logging
logger = logging.getLogger("webutil")


def webFuncDecorator(func):
    def _decorator():
        result = {"success": True}
        try:
            execResult = func()
            if execResult:
                if type(execResult) == dict:
                    result = dict(result, **execResult)
                else:
                    result["result"] = execResult
        except Exception as e:
            logger.exception(e)
            raise e
            #result["success"] = False
            #result["fail_reason"] = str(e)
        return result
    return _decorator
