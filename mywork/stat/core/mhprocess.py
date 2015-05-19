#!/usr/bin/env python
''' the base class for all the processes, meas the process that need
to work in the system should inherit from this class, the base class
regist a msgh queue defaultly, and also defined some utils like the
_process and _final, the child class should just implement these
internal functions '''

import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from ehandler import EHandler
from common.echo import echo

class MyProcess(multiprocessing.Process):
    def __init__(self, msgh, msgh_name):
        multiprocessing.Process.__init__(self)
        self.msgh = msgh
        self.msgh_name = msgh_name
        self.queueid = self.msgh.registerQueue(self.msgh_name)
        self.queue = self.msgh.getQueue(self.queueid)
        self.ecode = 0
        self.eh = EHandler()
        self.eh.set_queue(self.queue)
        self.finish = False

    # totall control the process start and end
    def run(self):
        echo("process [%s/%s] start ..."%(self.pid, self.msgh_name))
        try:
            ret = self._process()
            ret = self._final()
        except Exception, e:
            print repr(e)
            import traceback
            traceback.print_exc()

    # should implemented by child process
    def _process(self):
        pass
    # should implemented by child process
    def _final(self):
        pass
