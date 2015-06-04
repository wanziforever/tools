#!/usr/bin/env python

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation, Node, Document

class Element(object):
    def __init__(self, id, url):
        self.id = id
        self.url= url
        
    def setId(self, id):
        self.id = id

    def setUrl(self, u):
        self.url = u

    def getId(self):
        return self.id
    def getUrl(self):
        return self.url

xml_string = '''<?xml version="1.0" ?><pics><pic id="2" url="http://10.0.64.231/images/20131216084907030176.png"/><pic id="1" url="http://10.0.64.231/images/20131216084915982977.jpg"/></pics>'''

def shortPicsById(pics):
    def short_by_id(p):
        return int(p["id"])
    pics.sort(key=short_by_id)
    
def url_get(xml_string):
    doc = minidom.parseString(xml_string)
    pic_nodes = doc.getElementsByTagName("pic")
    pics = []
    for node in pic_nodes:
        pic = {}
        pic["id"] = node.getAttribute("id")
        pic["url"] = node.getAttribute("url")
        pics.append(pic)
    shortPicsById(pics)
    return pics

if __name__ == "__main__":
    url_get(xml_string)
