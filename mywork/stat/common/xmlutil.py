#!/usr/bin/python
# -*- coding: utf-8 -*-
def get_attrvalue(node, attrname):
    return node.getAttribute(attrname).strip() if node else ''

def get_nodevalue(node, index = 0):
    if node and node.hasChildNodes():
        return node.childNodes[index].nodeValue.encode('utf-8','ignore').strip()
    return None

def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []

def get_xmlnode0(node, name):
    child_node = get_xmlnode(node, name)
    if len(child_node) > 0:
        return child_node[0]
    return None
