#!/usr/bin/env python

import time
import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from mymessage import MyMessage
from mydef import MyDef

class MyQueue(object):
    def __init__(self):
        self.array = [Array('c', MyDef.QUEUE_BLOCK_SIZE, lock=False) \
                      for q in range(MyDef.QUEUE_SIZE)]
        self.name = Array('c', MyDef.MAX_QUEUE_NAME, lock=False)
        self.send_pos = Value('i', -1, lock=False)
        self.recv_pos = Value('i', -1, lock=False)
        self.occupied_flag = Value('i', -1, lock=False)
        self.slock = multiprocessing.Lock()
        self.rlock = multiprocessing.Lock()

    def queue_load(self):
        if self.send_pos.value >= self.recv_pos.value:
            return self.send_pos.value - self.recv_pos.value
        else:
            return MyDef.QUEUE_SIZE - self.recv_pos.value + self.send_pos.value
            
        
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

        msg.build()
        try:
            arr[queue.send_pos.value].value = encode + msg.get_body()
        except:
            print "too long body ----------------------encode", encode, "body", msg.get_body()
            exit(0)

        if queue.send_pos.value + 1 >= MyDef.QUEUE_SIZE:
            #print "send pos reach the end of array", MyQueue.queue_size
            queue.send_pos.value = 0
        else:
            queue.send_pos.value += 1
        
        queue.slock.release()
    
    def receive(self, timeout):
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

        start_ts = time.time() * 1000
        while self.send_pos.value == -1 or \
                  self.recv_pos.value == self.send_pos.value:
            self.rlock.release()
            if timeout == 0:
                return None
            elif timeout < 0:
                time.sleep(0.01)
            else: 
                now_ts = time.time() * 1000
                delta = now_ts - start_ts
                if delta > timeout:
                    return None
                time.sleep(0.001)
            self.rlock.acquire()

        msg = arr[self.recv_pos.value].value
        
        if self.recv_pos.value + 1 >= MyDef.QUEUE_SIZE:
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

