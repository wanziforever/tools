#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

entry_format = '''{title}|{id}|{description}'''
file_name = "media_desc.dat"

class DescEntry(object):
    def __init__(self, title, mid):
        self.title = title
        self.mid = mid
        self.desc = ""

    def set_desc(self, desc):
        self.desc = desc

    def __repr__(self):
        return "title: {title}, mediaId: {mid}, desciption: {desc}".\
               format(self.title, self.mid, self.desc)

# currently only support query by title
entry_hash = {}

def get_desc_by_title(title):
    #for t, value in entry_hash.items():
    #    print t, value
    #print "going to match title ", title,
    if title not in entry_hash:
    #    print "[no match]"
        return None
    #print '[match]'
    return entry_hash[title]

def data_initialize():
    with open(file_name) as fd:
        for line in fd:
            if line[0] == '#':
                continue
            if len(line.strip()) == 0:
                continue
            try:
                title, mid, desc = line.split("|", 2)
                entry_hash[title.strip().decode()] = desc.strip()
            except:
                continue

if __name__ == "__main__":
    data_initialize()

    query_title = "虎妈猫爸"
    print get_desc_by_title(query_title.decode())
