#!/usr/bin/env python

import os
import time
import datetime
import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from msgh_def import MsgType

class MyHeader(object):
    def __init__(self):
        self.sender = ""
        self.sender_len = MyQueue.MAX_QUEUE_NAME
        self.receiver = ""
        self.receiver_len = MyQueue.MAX_QUEUE_NAME
        self.type = 0
        self.type_len = 3
        self.fixed_header_len = self.sender_len + self.type_len

    def set_header_params(self, params):
        ''' currently not implemented for very little params '''
        pass

    def get_sender(self):
        return self.sender

    def get_type(self):
        return self.type

    def set_sender(self, sender_qname):
        if len(sender_qname) > MyQueue.MAX_QUEUE_NAME:
            self.sender = sender_qname[:MyQueue.MAX_QUEUE_NAME]
        else:
            self.sender = sender_qname
        return True
    def set_receiver(self, receiver_qname):
        self.receivere = receiver_qname
        
    def set_type(self, msg_type):
        if not isinstance(msg_type, int):
            print "fail to set message type", msg_type
            return False
        self.type = msg_type
        return True
        
    def encode(self):
        ''' encode all the header element into a string base data
        each element data will occupy fix lengh of data, and all
        element will have a sequence to build mesasge:
        type[3]||qname[MAX_QUEUE_NAME]

        return: (True, header_string) '''
        s = ""
        type_str = str(self.type)
        if len(type_str) >= self.type_len:
            type_str = type_str[:self.type_len]
        else:
            type_str += " " * (self.type_len - len(type_str))
        s += type_str
        
        name_str = ""
        if len(self.sender) >= self.sender_len:
            name_str = self.sender[:self.sender_len]
        else:
            name_str = self.sender + " " * (self.sender_len - len(self.sender))
        s += name_str
        return True, s

    def decode(self, header_str):
        if len(header_str) != self.fixed_header_len:
            print "fail to decode header string, len is not %s"%\
                  self.fiexed_header_len
            return False
        type_str = header_str[:self.type_len]
        if not type_str.strip().isdigit():
            print "fail to decode header string, first %s[%s] char should "\
                  "represent a digit"%(self.type_len, type_str)
            print header_str
            return False
        self.type = int(type_str)
        self.sender = header_str[self.type_len:]
        return True

class MyMessage(object):
    def __init__(self, type=MsgType.INVALID):
        self.header = MyHeader()
        self.header.set_type(type)
        self.body = ""

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_header(self, type, qname):
        self.header.set_sender(qname)
        self.header.set_type(type)

    def encode_header(self):
        ret, s = self.header.encode()
        return ret, s

    def decode_header(self, header_str):
        return self.header.decode(header_str)

    def cast(self, MyMessageObject):
        self.header = MyMessageObject.get_header()
        self.body = MyMessageObject.get_body()

    def get_body(self):
        return self.body

    def get_header(self):
        return self.header

class MyQueue(object):
    QUEUE_BLOCK_SIZE = 10000
    MAX_QUEUE_NAME = 50
    QUEUE_SIZE = 2048
    #QUEUE_SIZE = 2

    def __init__(self):
        self.array = [Array('c', MyQueue.QUEUE_BLOCK_SIZE, lock=False) \
                      for q in range(MyQueue.QUEUE_SIZE)]
        self.name = Array('c', MyQueue.MAX_QUEUE_NAME, lock=False)
        self.send_pos = Value('i', -1, lock=False)
        self.recv_pos = Value('i', -1, lock=False)
        self.occupied_flag = Value('i', -1, lock=False)
        self.slock = multiprocessing.Lock()
        self.rlock = multiprocessing.Lock()

    def queue_load(self):
        if self.send_pos.value >= self.recv_pos.value:
            return self.send_pos.value - self.recv_pos.value
        else:
            return MyQueue.QUEUE_SIZE - self.recv_pos.value + self.send_pos.value
            
        
    def __repr__(self):
        s = "Qinfo: name: {0}, send_pos: {1}, recv_pos: {2}, occupied_flag: {3}, size:{4}".\
            format(self.name.value, self.send_pos.value, self.recv_pos.value,
                   self.occupied_flag.value, self.queue_load())
        return s

    def send(self, queue, msg):
        ''' send message to the targe queue, the message should be a text
         format data, and the final message will add sender's queue
         name as prefix, the prefix is a fix length string. prefix
         lengh is MAX_QUEUE_NAME + len("sender: ")

         argument:
            queue     MyQueue type object
            msg       MyMessage type object
         example:
            original message: "denny::test::123456789"
            final message:    "sender: denny_queue   denny::test::123456789"
         return: True/False
        '''

        queue.slock.acquire()
        arr = queue.array
        if queue.send_pos.value == -1: # first time
            queue.send_pos.value = 0
        
        while queue.send_pos.value + 1 == queue.recv_pos.value:
            queue.slock.release()
            #print "process [%s] queue full put_queue wait for 0.2 second"%os.getpid()
            time.sleep(0.001)
            queue.slock.acquire()
        
        msg.header.set_sender(self.name.value)
        msg.header.set_receiver(queue.name.value)
        ret, encode = msg.encode_header()
        
        if ret is False:
            print "fail to encode header "
            return False
        
        arr[queue.send_pos.value].value = encode + msg.get_body()

        if queue.send_pos.value + 1 >= MyQueue.QUEUE_SIZE:
            #print "send pos reach the end of array", MyQueue.queue_size
            queue.send_pos.value = 0
        else:
            queue.send_pos.value += 1
        
        queue.slock.release()
    
    def receive(self, block=True):
        ''' receive the message for the current queue, return the message to
         caller. note that the caller should deep copy the message to
         new place, since the message space in the queue will be override
         currently no protection to protect the message will not be override
         before the data was copied to new place, caller should do it when
         it get the message immediately. later will consider to let caller
         provide a place, and the receive function in charge to do the copy
         in rlock protection
        
         after receive the message, this function will split the sender
         name and message body, return a tuple data whose first item is
         the sender's name, and second one is message body
         '''
        
        self.rlock.acquire()
        arr = self.array

        if self.recv_pos.value == -1:
            self.recv_pos.value = 0

        while self.send_pos.value == -1 or \
                  self.recv_pos.value == self.send_pos.value:
            self.rlock.release()
            if block is False:
                return None
            #print "process [%s] wait to receive message"%os.getpid()
            time.sleep(0.001)
            self.rlock.acquire()

        msg = arr[self.recv_pos.value].value
        
        if self.recv_pos.value + 1 >= MyQueue.QUEUE_SIZE:
            self.recv_pos.value = 0
        else:
            self.recv_pos.value += 1

        self.rlock.release()

        rcvmsg = MyMessage()
        if len(msg) < rcvmsg.header.fixed_header_len:
            print "message length should be more than %s"%\
                  rcvmsg.header.fixed_header_len
            return None
        ret = rcvmsg.decode_header(msg[:rcvmsg.header.fixed_header_len])
        if ret is False:
            print "fail to decode message"
            return None

        rcvmsg.set_body(msg[rcvmsg.header.fixed_header_len:])
        return rcvmsg

class MsghMgr(object):
    ''' MSGH manager was desiend to manage all the MSGH queue, and the
    instance will be only created in the master process, and after create,
    no data in the class should be changed, since it will keep the same
    data for all its child process (for copy-on-write, it will be different
    after a process change something)
     '''
    MAX_MSGH = 10
    def __init__(self):
        self.queues = [ MyQueue() for i in range(MsghMgr.MAX_MSGH) ]
        self.pos = Value('i', -1, lock=False)
            
    def getQueue(self, indx):
        return self.queues[indx]

    def registerQueue(self, qname):
        # there is no lock protect for this operation, it has risk, but low
        #print "registerQueue enter with qname", qname
        if self.pos.value == -1:
            # first time
            #print "registerQueue:first time registerQueue"
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
        ''' currently not implemented, will do it later'''
        pass

    def show_all_info(self):
        for q in self.queues:
            print repr(q)
        print "current queue pos is ", self.pos.value

    def findQueue(self, msgh_name):
        for i in range(len(self.queues)):
            if self.queues[i].name.value == msgh_name:
                return i
        return -1

class MsgMyTest(MyMessage):
    def __init__(self):
        MyMessage.__init__(self)

class MyProcess(multiprocessing.Process):
    def __init__(self, msgh_mgr, msgh_name):
        multiprocessing.Process.__init__(self)
        self.msgh_mgr = msgh_mgr
        self.msgh_name = msgh_name
        self.queueid = self.msgh_mgr.registerQueue(self.msgh_name)
        self.queue = self.msgh_mgr.getQueue(self.queueid)

    def run(self):
        print "process [%s/%s] start ..."%(self.pid, self.msgh_name)
        ret = self._process()
        print "process [%s/%s] exit with return code [%s]"%\
              (self.pid, self.msgh_name, ret)

    def _process(self):
        pass
        
class MysProcess(MyProcess):
    def __init__(self, msgh_mgr):
        MyProcess.__init__(self, msgh_mgr, "mysend")
        
    def _process(self):
        peer_msgh_name = 'myreceive'
        peerqid = self.msgh_mgr.findQueue(peer_msgh_name)
        if peerqid == -1:
            print "cannot find queue name with %s"%(peer_msgh_name)
            return
        queue = self.msgh_mgr.getQueue(peerqid)

        while True:
            #msg = "a test message with timestamp %s"%datetime.datetime.now()
            msg = "a test message with no timestamp"
            mymsg = MsgMyTest()
            mymsg.set_body(msg)
            
            self.queue.send(queue, mymsg)
            #time.sleep(0.01)
            
        return True
        
class MyrProcess(MyProcess):
    def __init__(self, msgh_mgr):
        MyProcess.__init__(self, msgh_mgr, "myreceive")
        
    def _process(self):
        queue = self.msgh_mgr.getQueue(self.queueid)
        while True:
            msg = queue.receive()
            if msg is None:
                continue
            #print "Process [%s] sender: %s, body: %s"%\
            #      (self.pid, msg.header.get_sender().strip(), msg.get_body())


if __name__ == "__main__":
    msgh_mgr = MsghMgr()
    rprocess1 = MyrProcess(msgh_mgr)
    rprocess1.start()
    time.sleep(1)
    sprocess1 = MysProcess(msgh_mgr)
    sprocess1.start()
    #sprocess2 = MysProcess(msgh_mgr)
    #sprocess2.start()

    while True:
        print "+---------------- QUEUE STATUS --------------------------------"
        msgh_mgr.show_all_info()
        print "---------------------------------------------------------------+"
        print
        time.sleep(3)
