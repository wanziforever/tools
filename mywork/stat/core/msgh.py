#!/usr/bin/env python

'''
MSGH(Message Host) concept was introduced for the message sender and
receiver, it is the foundation of all the messaging system, MSGH
actually is logic component with a message queue, and all the message
received stored in its queue, sending message has no send buffer, it
directly put the message into the receiver's queue.

Currently the MSGH cannot support Machine to Machine message, and will
support it later for becoming a real distributing messaging system.
'''

import os
import time
import datetime
import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from mymessage import MyMessage
from myqueue import MyQueue

class MsghMgr(object):
    ''' MSGH manager was desiend to manage all the MSGH queue, and the
    instance will be only created in the master process, and after
    create, no data in the class should be changed, since it will keep
    the same data for all its child process (for copy-on-write, it will
    be different after a process change something)
    '''
    MAX_MSGH = 15
    def __init__(self):
        ''' firstly initialize all the queues spaces'''
        self.queues = [ MyQueue() for i in range(MsghMgr.MAX_MSGH) ]
        self.pos = Value('i', -1, lock=False)
        self.msgh_log_file = "msgh.txt"
        self.msgh_log_fd = None
            
    def getQueue(self, indx):
        ''' get a queue by a index '''
        if indx < 0:
            return None
        return self.queues[indx]

    def registerQueue(self, qname):
        ''' register a queue by a given name, a queue which has not
        been occupied will be selected, every queue user should firstly
        regist a queue, and a related queue id will be returned'''
        # there is no lock protect for this operation, it has risk, but low
        if self.pos.value == -1:
            # first time
            self.pos.value = 1
            queue = self.queues[0]
            queue.name.value = qname
            queue.occupied_flag.value = 1
            return 0
        if self.pos.value >= MsghMgr.MAX_MSGH:
            print "registerQueue no enough slot for MSGH queue"
            return -1

        queue = self.queues[self.pos.value]
        queue.name.value = qname
        queue.occupied_flag.value = 1
        self.pos.value += 1
        return self.pos.value - 1

    def removeQueue(self, indx):
        ''' currently not implemented, will do it later '''
        pass

    def write_all_info(self):
        ''' write all the queue status information to a file, this is
        used to monitor the MSGH queues status in run time '''
        s = ""
        for q in self.queues:
            s += repr(q) + '\n'
        s += "current queue pos is %s\n"%self.pos.value
        if self.msgh_log_fd is None:
            self.msgh_log_fd = open(self.msgh_log_file, "w")
        self.msgh_log_fd.write(s)
        self.msgh_log_fd.flush()

    def show_all_info(self):
        ''' return the status of all the queues, string format result,
        this is API for getting queue status information '''
        s = ""
        for q in self.queues:
            s += repr(q) + '\n'
        s += "current queue pos is %s\n"%self.pos.value
        return s
        
    def findQueue(self, msgh_name):
        ''' find a queue by a given name, the name is the name which
        has been registed before'''
        for i in range(len(self.queues)):
            if self.queues[i].name.value == msgh_name:
                return i
        return -1

