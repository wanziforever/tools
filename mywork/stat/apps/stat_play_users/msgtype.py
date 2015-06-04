#!/usr/bin/env python

from core.msgtype import enum, MsgTypeBase

MsgType = enum(MsgTypeBase.STAT_PLAY_USER,
               "MsgPlayUserCalc",
               "MsgPlayUserReport"
               )
