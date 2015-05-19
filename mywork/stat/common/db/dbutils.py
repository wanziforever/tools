#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
created on 1th,June by wujintao
'''
import web
import time
from common import settings

KERNEL_DB = web.database( \
        dbn = 'mysql', \
        host = settings.DB_HOST, \
        db = settings.DB_KERNEL, \
        user = settings.DB_USER, \
        pw = settings.DB_PASSWORD)


class IdGenerator():
    def __init__(self, server_id):
        self.server_id = server_id
        self.time_reduction = 1262275200000
        self.last_time = self.__get_current_time()
        self.auto_increase = 0
    
    def __get_current_time(self):
        return long((time.time() * 1000 - self.time_reduction)) >> 8

    def get_next_id(self):
        current = self.__get_current_time()
        if current < self.last_time:
            current = self.last_time
            self.auto_increase = 0
        elif current > self.last_time:
            self.auto_increase = 0
        elif (current == self.last_time) and ((self.auto_increase & 0x1fffff) == 0x100000):
            current += 1
            self.auto_increase = 0
        self.last_time = current
        next = (current << 28) | (0xfffff00L & (self.auto_increase << 8)) | self.server_id
        self.auto_increase += 1
        return str(next)
    
    