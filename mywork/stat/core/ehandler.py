#!/usr/bin/env python
''' event handler is a centralized function to handle all the event
currently two types of event are supported(timer event, socket
message event). the getEvent() interface is the only method to get
event, events are represented by a event type field. '''

import os
import msgh
from mytimers import MyTimers, MsgTimerExp

class EVENTYPE(object):
    TIMEREXPIRE = 1
    NORMALMSG = 2

class EHandler(object):
    ''' event handler definition '''
    def __init__(self):
        self.myqueue = None
        self.mytimer = MyTimers()
        self.mytimer.tmrInit(10000)
        self.msg_first = False

    def set_queue(self, queue):
        ''' distinctly set the queue which will generate the socket
        message event'''
        self.myqueue = queue
        
    def register_timer(self, time, tag, c_flag):
        ''' distinctly add a expired timer '''
        self.mytimer.setlRtmr(time, tag, c_flag)

    def getEvent(self, block=True):
        ''' get the latest expired event, the logic will roundrobin
        firstly check the timer and socket message queue to avoid two
        many socket message block the timer event, if the block flag
        is set, the function will block the calling until the next
        event occur '''
        self.msg_first = not self.msg_first
        rcv_flg = False
        wait = 0
        if self.msg_first is True:
            msg = self.myqueue.receive(timeout=0)
            if msg is not None:
                return msg
            rcv_flg = True

        ret, tag, exp_time = self.mytimer.tmrExp()
        if ret is True and exp_time == 0:
            wait = 0
            tmsg = MsgTimerExp()
            tmsg.set_tag(tag)
            tmsg.build()
            return tmsg

        if block is False and rcv_flg is False:
            msg = self.myqueue.receive(timeout=0)
            if msg is not None:
                return msg
            return None

        # if the exp_time is -1 just means the receive will block
        # if the exp_time is more than 0, just wait for a while
        # and if expired, go on to check the timer
        # add more expect time to receive to make sure the next timer
        # will expect successfully
        if exp_time > 0:
            exp_time += 2
        msg = self.myqueue.receive(timeout=exp_time)

        if msg is not None:
            return msg
        ret, tag, exp_time = self.mytimer.tmrExp()
        if ret is True and exp_time == 0:
            wait = 0
            tmsg = MsgTimerExp()
            tmsg.set_tag(tag)
            tmsg.build()
            return tmsg
        else:
            return None
