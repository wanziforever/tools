#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.log import log_enter
from common.util import pyutil, linuxutil
from subprocess import Popen
import datetime
import doctest
import logging
import time

# Uses Brian's python cron code from
# http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python

log = logging.getLogger(__name__)

@log_enter('create Cron instance with crontab={crontab_path}, concurrent={concurrent}')
def cron(crontab_path, concurrent=False): #use concurrrent to start cron with the same cmd
    events = _parse_file(crontab_path)
    return Cron(events, concurrent)

@log_enter('Running cron with crontab={crontab_path}, concurrent={concurrent}...')
def run(crontab_path, concurrent=False):
    events = _parse_file(crontab_path)
    Cron(events, concurrent).run()
    
def _parse_file(file):
    """Returns a list of Events, one per line."""
    with open(file, 'r') as f:
        events = []
        for line in f:
            line = line.strip()
            logging.debug("Parsing crontab line: %s" % line)
            if len(line) == 0 or line[0] == '#':
                continue
                
            chunks = line.split(None, 5)
            event = Event(make_cmd_runner(chunks[5]),
                          parse_arg(chunks[0]),
                          parse_arg(chunks[1]),
                          parse_arg(chunks[2]),
                          parse_arg(chunks[3]),
                          parse_arg(chunks[4]))
            events.append(event)
        return events

def make_cmd_runner(cmd):
    """
    Takes a path to a cmd and returns a function that when called, will run it.
    """
    def _wrapper():
        Popen(cmd, shell=True, close_fds=True)
    r = _wrapper
    r.cmd = cmd
    return r

def parse_arg(arg):
    """
    Takes a crontab time arg and converts it to a python int, iterable, or set.
    
    >>> parse_arg('0')
    set([0])
    >>> parse_arg('0,30')
    set([0, 30])
    >>> parse_arg('0/10')
    set([0, 40, 10, 50, 20, 30])
    >>> parse_arg('*') == ALL_MATCH
    True
    """
    if arg == '*':
        return ALL_MATCH
    s = set()
    if '/' in arg:
        if len(arg.split('/')) > 2:
            raise NotImplementedError("The crontab line is malformed or isn't supported.")
        start, interval = arg.split('/')
        num = int(start)
        while num < 60:
            s.add(num)
            num += int(interval)
    else:
        for m in arg.split(','):
            s.add(int(m))
    return s

class AllMatch(set):
    """
    Universal set - match everything
    """
    def __contains__(self, item):
        return True

ALL_MATCH = AllMatch()

def conv_to_set(obj):  # Allow single integer to be provided
    if isinstance(obj, (int, long)):
        return set([obj])  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

class Event(object):
    def __init__(self, action, min=ALL_MATCH, hour=ALL_MATCH,
            day=ALL_MATCH, month=ALL_MATCH, dow=ALL_MATCH):
        """
        day: 1 - num days
        month: 1 - 12
        dow: mon = 1, sun = 0/7
        """
        self.action = action
        self.mins = conv_to_set(min)
        self.hours= conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.dow = conv_to_set(dow)
        if 0 in self.dow or 7 in self.dow:
            # both 0 and 7 are considered as Sunday
            self.dow.add(0)
            self.dow.add(7)

    def matchtime(self, t):
        """
        Return True if this event should trigger at the specified datetime.
        
        >>> e = Event(None, min=set([1]), hour=set([2]), day=set([3]), month=set([4]))
        >>> e.matchtime(datetime.datetime(2011, 4, 3, 2, 1, 0))
        True
        >>> e.matchtime(datetime.datetime(2011, 5, 3, 2, 1, 0))
        False
        >>> e.matchtime(datetime.datetime(2011, 4, 4, 2, 1, 0))
        False
        >>> e.matchtime(datetime.datetime(2011, 4, 3, 4, 1, 0))
        False
        >>> e.matchtime(datetime.datetime(2011, 4, 3, 2, 4, 0))
        False
        """
        return ((t.minute        in self.mins) and
                (t.hour          in self.hours) and
                (t.day           in self.days) and
                (t.month         in self.months) and
                (t.isoweekday()  in self.dow))

    def check(self, t, concurrent=False):
        if self.matchtime(t):
            processes = linuxutil.list_processes(self.action.cmd)
            if len(processes) > 0 and not concurrent:
                # use cocurrent to start cron with the same cmd 
                pids = [p.pid for p in processes]
                log.info('Task "%s" is scheduled, but is still running with pid=%s. Ignore this schedule.' % (self.action.cmd, pids))
            else:
                log.info('Starting "%s" ...' % self.action.cmd)
                self.action()
    
class Cron(object):
    def __init__(self, events, concurrent=False):
        self.events = events
        self.concurrent = concurrent

    def run(self):
        cur_minute = prev_minute = datetime.datetime(*datetime.datetime.now().timetuple()[:5])
        while True:
            # check events
            for e in self.events:
                e.check(cur_minute, self.concurrent)
                
            # wait until next minute
            prev_minute = cur_minute
            while cur_minute == prev_minute:
                time.sleep(1)
                cur_minute = datetime.datetime(*datetime.datetime.now().timetuple()[:5])

if __name__ == '__main__':
    doctest.testmod()
    