#!/usr/bin/env python

from core.msgtype import MsgTypeBase, enum

MsgType = enum(MsgTypeBase.COMMON,
               "MsgCalcStart",
               "MsgCalcExit",
               "MsgWorkerQuit",
               "MsgGrabberQuit",
               "MsgProgressReport",
               "MsgTest")

