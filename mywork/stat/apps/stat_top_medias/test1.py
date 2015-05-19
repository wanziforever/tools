#!/usr/bin/env python

from core.mydb import Mydb

db = Mydb()
db.connect('repository')
session = db.open("all_medias")

entries = session.select("*")

for key, values in entries:
    print "--title--", values[0], values[1], values[2]
