#!/usr/bin/env python

from common.tmtags import enum, TMtagsComm


TMTAGS = enum(TMtagsComm.STAT_PLAY_TIMES,
              "SEND_REPORT",
              "PRINT_REPORT")
