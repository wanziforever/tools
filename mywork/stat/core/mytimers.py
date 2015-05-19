#!/usr/bin/env python

import os
import time
import threading
from mymessage import MyMessage
from eventype import EVENTYPE
from msgtype import MsgTypeBase

TMtimes = None

def TMTIMEADD(go_off, interval):
    go_off.time += interval.time

def LEFTME(a, b):
    return a.time <= b.time

def LTIME(a, b):
    return a.time < b.time

def TMITIMEDIFF(a, b):
    if a.time < b.time:
        return b.time - a.time
    else:
        return a.time - b.time

def TMTIMINCR(now, diff):
    now.time += diff

def LINK2HEAP(heap, tcb, h, t):
    heap.theap[h] = t
    tcb[t].thi = h

class MyTime(object):
    def __init__(self):
        self.hi_time = 0
        self.lo_time = 0
        self.time = 0

class MyTMState(object):
    TEMPTY = 0
    ORTIMER = 1
    CRTIMER = 2
    TLIMBO = 3
    def __init__(self):
        pass

class MyTMCB(object):
    def __init__(self):
        self.llink = 0
        self.rlink = 0
        self.thi = 0
        self.tstate = MyTMState.TLIMBO
        self.go_off = MyTime()
        self.period = MyTime()
        self.tag = 0

class TMheap(object):
    def __init__(self):
        self.fftheap = 0
        self.theap = None

class MyTimers(object):
    TMmaxTCBs = 10000000
    def __init__(self):
        self.init_flg = False
        self.TMbtcb = None
        self.TMrtheap = TMheap()
        self.TMoffset = MyTime()
        self.TMfftcb = 0
        self.TMlftcb = 0
        self.TMidletcb = 0
        self.TMnow = MyTime()
        self.TMthen = MyTime()
        self.TMlastupd = MyTime()
        self.pid = 0
        self.nTCBs = 0
        self.tmrlock = threading.Lock()
        self.state_mapping = {MyTMState.ORTIMER: self.handle_ortimer,
                              MyTMState.CRTIMER: self.handle_crtimer}
    def __repr__(self):
        s = "fftheap: {0} , theaps:[1]".format(self.TMrtheap.fftheap,
                                               self.TMrtheap.theap)
        return s
        
    def tmrInit(self, allocTCBs=100):
        if allocTCBs > MyTimers.TMmaxTCBs or allocTCBs < 1:
            print "MyTimers::tmrInit invalid initialize number %s"%allocTCBs
            return False

        if self.init_flg == True:
            print "MyTimers::tmrInit already init"
            return False

        self.pid = os.getpid()
        self.nTCBs = allocTCBs

        if self.TMbtcb is None:
            self.TMbtcb = [MyTMCB() for i in range(self.nTCBs)]
        if self.TMrtheap.theap is None:
            self.TMrtheap.theap = [0 for i in range(self.nTCBs+1)]
        t = 0

        while t < self.nTCBs:
            tcbptr = self.TMbtcb[t]
            tcbptr.tstate = MyTMState.TEMPTY
            tcbptr.llink = t-1
            tcbptr.rlink = t+1
            tcbptr.thi = None
            t += 1

        TMfftcb = 0
        TMlftcb = self.nTCBs - 1
        self.TMbtcb[TMfftcb].llink = None
        self.TMbtcb[TMlftcb].rlink = None

        TMidletcb = self.nTCBs

        self.TMrtheap.fftheap = 1
        t = 0
        while t <= self.nTCBs:
            self.TMrtheap.theap[t] = None
            t += 1

        self.inittime()
        self.init_flg = True

    def inittime(self):
        if TMtimes is not None:
            self.TMthen = TMtimes
        else:
            self.TMthen = int(time.time() * 1000)

        self.TMnow.time = self.TMthen
        self.TMlostupd = self.TMnow

    def tmrReinit(self):
        self.init_flg = False
        if self.TMrtheap.theap is None:
            #free(self.TMrtheap.theap)
            self.TMrtheap.theap = None

        if self.TMbtcb is not None:
            #free(TMbtcb)
            TMbtcb = None

    def setlRtmr(self, time, tag, c_flag):
        #print "MyTimers::setlRtmr with", time, tag, c_flag
        if self.init_flg is False:
            return False

        if time <= 0:
            print "MyTimers::setlRtmr invalid time", time
            return False

        interval = MyTime()
        interval.time = time
        #print "MyTimers::setlRtmr interval.time ", time
        self.tmrlock.acquire()
        t = self.gettcb()
        if t < 0:
            print "MyTimers::setlRtmr invalid cb from gettcb"
            self.tmrReinit()
            self.tmrInit()
            self.tmrlock.release()
            return False
        tcbptr = self.TMbtcb[t]
        tcbptr.tag = tag
        if c_flag is True:
            tcbptr.tstate = MyTMState.CRTIMER
            tcbptr.period = interval
        else:
            tcbptr.tstate = MyTMState.ORTIMER

        ret = self.updtime(False)
        if ret is False:
            print "MyTimers::setlRtmr fail to updtime"
            self.tmrReinit()
            self.tmrInit()
            self.tmrlock.release()
            return False

        go_off = MyTime()
        go_off.time = self.TMnow.time
        #print "MyTimers::setlRtmr going to add ", go_off.time, interval.time
        TMTIMEADD(go_off, interval)
        
        #print "MyTimers::setlRtmr ", go_off.time
        tcbptr.go_off.time = go_off.time
        #print "MyTimers::setlRtmr go_off is", tcbptr.go_off.time

        ret = self.tsched(t)
        if ret is False:
            self.tmrReinit()
            self.tmrInit()
            self.tmrlock.release()
            
        self.tmrlock.release()

    def handle_ortimer(self, t, tcbptr):
        ret = self.tunsched(t)
        if ret is False:
            self.tmrReinit()
            self.tmrInit()
            return ret
        freetcb(t)
        return True

    def handle_crtimer(self, t, tcbptr):
        ret = self.tunsched(t)
        if ret is False:
            self.tmrReinit()
            self.tmrInit()
            return ret

        while True:
            TMTIMEADD(tcbptr.go_off, tcbptr.period)
            if not LTIME(tcbptr.go_off, self.TMnow):
                break
        tcbptr.tstate = MyTMState.CRTIMER
        self.tsched(t)
        return True


    def tmrExp(self):
        '''return status and left time'''
        tag, exp_time = -1, -1
        if self.init_flg is False:
            return False, tag, expt_time

        self.tmrlock.acquire()

        t = self.TMrtheap.theap[1]
        #print "-----------------------", t, os.getpid()
        # is the heap empty
        if t is None:
            #print "the timer heap is empty"
            self.tmrlock.release()
            return False, tag, exp_time

        tcbptr = self.TMbtcb[t]
        self.updtime(False)

        offset = MyTime()

        TMTIMEADD(offset, self.TMnow)
        #print "tcbptr.go_of:", tcbptr.go_off.time, "offset:", offset.time
        if LEFTME(tcbptr.go_off, offset):
            tag = tcbptr.tag
            exp_time = 0
            if not tcbptr.tstate in self.state_mapping:
                print "MyTimers::tmrExp no state defined", tcbptr.tstate
                self.tmrReinit()
                self.tmrInit()
                return False, tag, exp_time
            fun = self.state_mapping[tcbptr.tstate]
            ret = fun(t, tcbptr)
            self.tmrlock.release()
            return ret, tag, exp_time
        else:
            delta = TMITIMEDIFF(offset, tcbptr.go_off)
            self.tmrlock.release()
            return True, tag, delta

    def tsched(self, t):
        h = self.TMrtheap.fftheap
        self.TMrtheap.fftheap += 1
        LINK2HEAP(self.TMrtheap, self.TMbtcb, h, t)
        key = self.TMbtcb[t].go_off
        ph = h >> 1
        while ph > 0:
            pt = self.TMrtheap.theap[ph]
            pkey = self.TMbtcb[pt].go_off
            if LTIME(key, pkey):
                LINK2HEAP(self.TMrtheap, self.TMbtcb, h, pt)
                LINK2HEAP(self.TMrtheap, self.TMbtcb, ph, t)
            else:
                return True
            h = ph
            ph >> 1
        return True

    def tunsched(self, t):
        self.TMbtcb[t].tstate = MyTMState.TLIMBO
        h = self.TMbtcb[t].thi
        self.TMrtheap.fftheap -= 1
        lastheap = self.TMrtheap.fftheap
        replacement = self.TMrtheap.theap[lastheap]
        LINK2HEAP(self.TMrtheap, self.TMbtcb, h, replacement)
        self.TMrtheap.theap[lastheap] = None

        if h == lastheap:
            return True

        key = self.TMbtcb[replacement].go_off

        nh = h >> 1
        while nh > 0:
            nt = self.TMrtheap.theap[nh]
            nkey = self.TMbtcb[nt].go_off
            if LTIME(key, nkey):
                LINK2HEAP(self.TMrtheap, self.TMbtcb, h, nt)
                LINK2HEAP(self.TMrtheap, self.TMbtcb, nh, replacement)
            else:
                break
            h = nh
            nh >> 1

        while True:
            nh = h * 2
            if nh >= lastheap:
                return True

            nt = self.TMrtheap.theap[nh]
            nkey = self.TMbtcb[nt].go_off

            rh = nh + 1
            if rh < lastheap:
                rt = self.TMrtheap.theap[rh]
                rkey = self.TMbtcb[rt].go_off
                if LTIME(rkey, nkey) :
                    nh = rh
                    nt = rt
                    nkey = rkey

            if LTIME(nkey, key):
                LINK2HEAP(self.TMrtheap, self.TMbtcb, h, nt)
                LINK2HEAP(self.TMrtheap, self.TMbtcb, nh, replacement)
            else:
                return True
            h = nh
        
    def gettcb(self):
        t = self.TMfftcb
        tcbptr = self.TMbtcb[t]
        self.TMfftcb = tcbptr.rlink
        if self.TMfftcb is None:
            self.TMbtcb[self.TMfftcb].llink = None
        else:
            self.TMlftcb = None

        tcbptr.rlink = None
        tcbptr.llkin = None

        tcbptr.tstate = MyTMState.TLIMBO

        self.TMidletcb -= 1
        return t
        
    def freetcb(self, t):
        tcbptr = self.TMbtcb[t]
        if tcbptr.tstate == MyTMState.TEMPTY:
            print "MyTimers::freetcb invalid state"
            return False
        ret = tunsched(t)
        if ret is False:
            return False
        tcbptr.thi = None
        tcbptr.tstate = TEMPTY

        tcbptr.llink = self.TMlftcb
        tcbptr.rlink = None
        if TMlftcb is not None:
            self.TMbtcb[TMlftcb].rlink = t
        else:
            TMfftcb = t
        TMlftcb = t
        TMidletcb += 1
        return True

    def updtime(self, flag):
        if TMtimes is not None:
            newtime = TMtimes
        else:
            newtime = int(time.time() * 1000)

        timediff = 0
        #print "TMthen", self.TMthen, "newtime", newtime
        if self.TMthen > newtime:
            timediff = self.TMthen - newtime
        else:
            timediff = newtime - self.TMthen

        TMTIMINCR(self.TMnow, timediff)
        self.TMthen = newtime

        return True


class MsgTimerExp(MyMessage):
    def __init__(self):
        MyMessage.__init__(self,
                           evtype=EVENTYPE.TIMEREXPIRE,
                           msgtype=MsgTypeBase.TIMEREXP)
        self.tag = 0

    def set_tag(self, tag):
        self.tag = tag

    def get_tag(self):
        return self.tag

    def build(self):
        self.body = str(self.tag)

    def parse(self):
        self.tag = int(self.body)
        
     
if __name__ == "__main__":
    timer = MyTimers()
    timer.tmrInit()
    timer.setlRtmr(10 * 1000, 11, True)
    timer.setlRtmr(14 * 1000, 14, True)
    timer.setlRtmr(12 * 1000, 12, True)
    timer.setlRtmr(18 * 1000, 18, True)
    timer.setlRtmr(19 * 1000, 19, True)
    timer.setlRtmr(25 * 1000, 25, True)

    while True:
        ret, tag, interval = timer.tmrExp()
        if ret is False:
            #print "timer queue is empty"
            break
        elif interval > 0:
            #print "timer found, but wait for %s mseconds"%interval
            time.sleep(interval/1000.0)
        elif interval == 0:
            print "timer expired found, tag is %s"%tag

    print "done"
