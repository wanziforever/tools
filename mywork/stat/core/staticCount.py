#!/usr/bin/env python
#total count
# time_count = 0
# count = 0
# fail_count = 0
# #flag five minute
# flag = 0
# five_total = 0
# fail_total = 0
# long_flag = 0
# process_long = 0
# process_count = 0
# process_total = 0

class StaticCount(object):
    time_count = 0
    count = 0
    fail_count = 0
    #flag five minute
    five_total = 0
    fail_total = 0
    long_flag = 0
    process_long = 0
    process_count = 0
    process_total = 0

    def __init__(self):
        pass

    def five_initial(self):
        StaticCount.five_total = StaticCount.count
        StaticCount.fail_total = StaticCount.fail_count
        StaticCount.process_total = StaticCount.process_count
        StaticCount.process_long = StaticCount.long_flag
        StaticCount.count = 0
        StaticCount.fail_count = 0
        StaticCount.process_count = 0
        StaticCount.time_count = 0
        StaticCount.long_flag = 0

    def count_add(self):
        StaticCount.count = StaticCount.count + 1

    def process_count_add(self, process_time):
        StaticCount.process_count = StaticCount.process_count + process_time

    def fail_count_add(self):
        StaticCount.fail_count =  StaticCount.fail_count + 1

    def long_add(self, process_time):
        if  process_time > StaticCount.long_flag:
            StaticCount.long_flag = process_time

    def set_time_count(self, t):
        StaticCount.time_count = t

    def get_time_count(self):
        return StaticCount.time_count
