#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import Application, make_app_wrappers, request
from core.bottle import template
from core.mydb import Mydb, MySession
#from datetime import datetime, timedelta
import datetime
import time
from time import mktime

app = Application()
get, post = make_app_wrappers(app)
db = Mydb()
db.connect('report')

@get('/')
def index():
    return template('portal')

def compute_days(to_day, intvl):
    ''' here the input parameters changed by this function '''
    intvl = int(intvl)
    if to_day == '':
        to_day = str(datetime.datetime.now())[:10]

    d = datetime.datetime.strptime(to_day, '%Y-%m-%d')

    pre_to_day = str(d - datetime.timedelta(days=intvl))[:10]
    next_to_day = str(d + datetime.timedelta(days=intvl))[:10]

    days = []
    for i in range(int(intvl)):
        days.append(str(d-datetime.timedelta(days=(int(intvl)-i-1)))[:10])

    return next_to_day, pre_to_day, days

def get_hours_for_day(to_day):
    ''' input a day parameter, and return the timestamp for each
    hour in that day '''
    if to_day == '':
        to_day = str(datetime.datetime.now())[:10]
    d = datetime.datetime.strptime(to_day, '%Y-%m-%d')
    hours = []
    for i in range(0, 24):
        h = d + datetime.timedelta(hours=i)
        hours.append(h)
    return hours, to_day

def divide_hours(hours, num):
    if num > 26:
        print "division number can not be more than 26"
        return []
    #mini_labels = ['a', 'b', 'c', 'd', 'e', 'f',
    #               'g', 'h', 'i', 'j', 'k', 'l',
    #               'm', 'n', 'o', 'p', 'q', 'r',
    #               's', 't', 'u', 'v', 'w', 'x',
    #               'y', 'z']
    mini_labels = ['.', '.', '.', '.', '.', '.',
                   '.', '.', '.', '.', '.', '.',
                   '.', '.', '.', '.', '.', '.',
                   '.', '.', '.', '.', '.', '.',
                   '.', '.']
    times = []
    labels = []
    c = 0
    for i in xrange(0, len(hours)-1):
        delta = (hours[i+1] - hours[i]).total_seconds() / num
        times.append(hours[i])
        labels.append(i)
        for j in xrange(1, num):
            times.append(hours[i] + datetime.timedelta(seconds=delta*j))
            labels.append(mini_labels[j-1])
    times.append(hours[-1])
    labels.append(len(hours)-1)
    times = [int(mktime(h.timetuple())) for h in times]
    #return times, labels
    return {'times': times,
            'labels': labels}

@get('/trends')
def play_trends():
    return template("trends")

@get('/tops')
def play_trends():
    return template("tops")

def convert_week_time(date):
    week_day_dict = {
        0 : '星期一',
        1 : '星期二',
        2 : '星期三',
        3 : '星期四',
        4 : '星期五',
        5 : '星期六',
        6 : '星期日',
        }
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    day = d.weekday()
    return week_day_dict[day]
    
@get('/trends_api')
def freq_trends():
    mini_labels_num = 5
    delta = 30 #seconds
    to_day = request.query.to
    hours, to_day = get_hours_for_day(to_day)
    desc = request.query.api
    dbname = 'freq_trends_' + desc
    session = db.open(dbname)
    labels = []
    if session is None:
        print
        return "database is wrong " + dbname
    counts = []
    info = divide_hours(hours, mini_labels_num)
    time_array = info['times']
    labels = info['labels']
    for i in xrange(0, len(time_array)):
        sec = time_array[i] - delta
        start = time_array[i] - delta
        end = time_array[i] + delta
        total = 0
        for sec in xrange(start, end):
            entry = session.select({'timestamp': sec})
            if entry is None:
                continue
            total += int(entry[1][1])
        ave = total / delta
        counts.append(ave)

    d = datetime.datetime.strptime(to_day, '%Y-%m-%d')
    pre_to_day = str(d - datetime.timedelta(days=1))[:10]
    next_to_day = str(d + datetime.timedelta(days=1))[:10]
            
    session.close()
    week_day = convert_week_time(to_day)

    return template('trends_api',
                    hours=labels,
                    data=counts,
                    today = to_day,
                    week = week_day,
                    pre_to_day=pre_to_day,
                    next_to_day=next_to_day,
                    api=desc
                    )
    
@get('/tops_api')
def freq_tops():
    to_day = request.query.to
    intvl = request.query.intvl
    desc = request.query.api
    if intvl == '':
        intvl = 30
    next_to_day, pre_to_day, days = compute_days(to_day, intvl)
    dbname = 'freq_tops_' + desc
    session = db.open(dbname)
    if session is None:
        print
        return "database is wrong " + dbname
    counts = []
    session.close()

    for day in days:
        d = datetime.datetime.strptime(day, '%Y-%m-%d')
        sec = int(mktime(d.timetuple()))
        print day, sec
        entry = session.select({'timestamp': sec})
        if entry is None:
            count = 0
        else:
            count = int(entry[1][1])
        counts.append(count)
            
    days = [day[5:] for day in days]
    print days, counts
    return template('tops_api',
                    days=days,
                    data=counts,
                    interval=intvl,
                    pre_to_day=pre_to_day,
                    next_to_day=next_to_day,
                    api=desc
                    )
                    
    
