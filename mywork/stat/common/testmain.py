#!/usr/bin/env python

from grabber_manager import GrabberManager
from grabber_worker import GrabberWorker
from calc_manager import CalcManager
from calc_worker import CalcWorker

from core.msgh import MsghMgr

msgh = MsghMgr()

if __name__ == "__main__":
    gmgr = GrabberManager(msgh)
    gmgr.set_worker('grabberworker', GrabberWorker,
                    {'start':0, 'end': 1})
    gmgr.start()

    cmgr = CalcManager(msgh)
    cmgr.set_worker('calcworker', CalcWorker,
                    {'start':0, 'end': 1})
    cmgr.start()
    
