#!/usr/bin/env python

from mydb import Mydb, MySession

mdb = Mydb()
mdb.connect("report")

session = mdb.open("active_users")

print "select all recoreds "
data = session.select('*', True)

print "-------- select * ---------------"
data = session.select('*', True)

print "-------- select key -------------"
data = session.select({'vender':'HISENSE',
                       'date': '5'})

print data

#session.insert({'vender':"test",
#                'date': "7",
#                'count': 20})

#session.update({'vender': 'test',
#                'date': "9",
#                'count': 50})
