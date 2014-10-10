#!/usr/bin/env python

import re
import os
import sys
import time
import threading
import datetime
import multiprocessing
from multiprocessing.sharedctypes import Value, Array

from pymongo import MongoClient
from bson.objectid import ObjectId

user_field_name = "deviceId"

mongo_host = "127.0.0.1"
mongo_port = 27017

mongocli = MongoClient(mongo_host, mongo_port)
logdb = mongocli.vodlog
player_startup = logdb.player_startup


#---- code to calc days -----
def mkDateTime(dateString,strFormat="%Y-%m-%d"):
    # Expects "YYYY-MM-DD" string
    # returns a datetime object
    eSeconds = time.mktime(time.strptime(dateString,strFormat))
    return datetime.datetime.fromtimestamp(eSeconds)

def formatDate(dtDateTime,strFormat="%Y-%m-%d"):
    # format a datetime object as YYYY-MM-DD string and return
    return dtDateTime.strftime(strFormat)

def mkFirstOfMonth2(dtDateTime):
    #what is the first day of the current month
    ddays = int(dtDateTime.strftime("%d"))-1 #days to subtract to get to the 1st
    delta = datetime.timedelta(days= ddays)  #create a delta datetime object
    return dtDateTime - delta                #Subtract delta and return

def mkFirstOfMonth(dtDateTime):
    #what is the first day of the current month
    #format the year and month + 01 for the current datetime, then form it back
    #into a datetime object
    return mkDateTime(formatDate(dtDateTime,"%Y-%m-01"))

def mkLastOfMonth(dtDateTime):
    dYear = dtDateTime.strftime("%Y")        #get the year
    dMonth = str(int(dtDateTime.strftime("%m"))%12+1)#get next month, watch rollover
    dDay = "1"                               #first day of next month
    nextMonth = mkDateTime("%s-%s-%s"%(dYear,dMonth,dDay))#make a datetime obj for 1st of next month
    delta = datetime.timedelta(seconds=1)    #create a delta of 1 second
    return nextMonth - delta                 #subtract from nextMonth and return

#---- end of code to calc days

class ProducerConfig(object):
    def __init__(self, start, end):
        self.start = str(start)
        self.end = str(end)

class Task(object):
    def __init__(self, userid, vender, ts):
        self.userid = userid
        self.vender = vender
        self.ts = ts

    def __repr__(self):
        s = "userid:{0}, vender:{1}, ts:{2}".format(self.userid, self.vender, self.ts)
        return s

producer_num = 16
class DataProducer(multiprocessing.Process):
    def __init__(self, config, task_queue, queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.queue = queue
        self.config = config
        self.count = 0
        self.current = 0
        self.mongocli = MongoClient(mongo_host, mongo_port)
        self.logdb = mongocli.vodlog
        self.player_startup = logdb.player_startup
        
    def run(self):
        # find all the entries in the range
        print "process [%s] going to find records betwen %s and %s"%\
              (self.pid, self.config.start, self.config.end)
        
        cursor = self.player_startup.find(
            {'ts': {'$gt': self.config.start, '$lte': self.config.end}})
        self.count = cursor.count()
        print "process [%s] %s record has been found"%(self.pid, self.count)
        for record in cursor:
            self.process(record)
        print "DataProducer process [%s] exit"%self.pid

    def process(self, doc):
        userid, vender, ts = \
                self.get_userid(doc), self.get_vender(doc), self.get_ts(doc)
        t = Task(userid, vender, ts)
        #print "process [%s] put task (%s) to queue"%(self.pid, repr(t))
        #self.task_queue.put(t)
        put_queue(self.queue, ts)
        

    def get_userid(self, doc):
        return doc['deviceId']

    def get_vender(self, doc):
        return doc['sourceId']

    def get_ts(self, doc):
        return doc['ts']

consumer_num = 1
class DataConsumer(multiprocessing.Process):
    def __init__(self, task_queue, queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.queue = queue

    def run(self):
        print "DataConsumer process [%s] start"%self.pid
        while True:
            #task = self.task_queue.pop()
            #task = self.queue.get()
            #if task is None:
            #    break
            msg = pull_queue(self.queue)
            #print "process [%s] get task (%s) from queue"%(self.pid, repr(task))
            #print "process [%s] get task (%s) from queue"%(self.pid, msg)

        print "DataConsumer process [%s] exit"%(self.pid)

def put_queue(queue, msg):
    # the send pos point to the buffer means the buffer has been
    # write successfully, read to receive
    queue_rear_lock.acquire()
    arr = queue[0]
            
    if queue[1].value == -1: # first time
        queue[1].value = 0

    while  queue[1].value + 1 == queue[2].value:
        #print "----send_pos----", queue[1].value
        queue_rear_lock.release()
        #print "process [%s] queue full put_queue wait for 0.2 second"%os.getpid()
        time.sleep(0.001)
        queue_rear_lock.acquire()

    arr[queue[1].value].value = msg

    if queue[1].value + 1 >= queue_size:
        #print "send pos reach the end of array", queue_size
        queue[1].value = 0
    else:
        queue[1].value += 1
        
    queue_rear_lock.release()
    

def pull_queue(queue):
    # rcv_pos point to the buffer means going to receive, should
    # not be override
    queue_front_lock.acquire()
    arr = queue[0]

    if queue[2].value == -1:
        queue[2].value = 0

    while queue[1].value == -1 or queue[2].value == queue[1].value:
        #print "rcv_pos", queue[2].value, "send_pos", queue[1].value
        queue_front_lock.release()
        #print "process [%s] queue empty pull_queue wait for 0.2 second"%os.getpid()
        time.sleep(0.001)
        queue_front_lock.acquire()

    msg = arr[queue[2].value].value
    #print "process [%s] pull_queue has index to "%os.getpid(), queue[2].value
    #print "process [%s] get message as "%os.getpid(), msg
        

    if queue[2].value + 1 >= queue_size:
        queue[2].value = 0
    else:
        queue[2].value += 1

    queue_front_lock.release()
    return msg
    
    
queue_size = 100
queue_block_size = 10000
queue_rear_lock = multiprocessing.Lock()
queue_front_lock = multiprocessing.Lock()
def calc():
    # calc the first ts and last ts for 9th month
    year, month, day = '2014', '9', '2'
    d = mkDateTime("%s-%s-%s"%(year, month, day))
    start_ts = int(time.mktime(mkFirstOfMonth(d).timetuple()) * 1000)
    end_ts = int(time.mktime(mkLastOfMonth(d).timetuple()) * 1000 + 999)

    # the first item is the string arrary, second item is the send pos
    # the third item is the receive pos
    queue = ([Array('c', queue_block_size, lock=False) for i in range(queue_size)],
             Value('i', -1, lock=False), Value('i', -1, lock=False))
    
    pc = ProducerConfig(start_ts, end_ts)
    
    tasks = multiprocessing.Queue(100)

    producers = [DataProducer(pc, tasks, queue) for i in range(producer_num)]
    consumers = [DataConsumer(tasks, queue) for i in range(consumer_num)]

    for c in consumers:
        c.start()

    for p in producers:
        p.start()
        
    
if __name__ == "__main__":
    calc()

    while True:
        time.sleep(2)
