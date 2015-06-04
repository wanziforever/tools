#!/usr/bin/env python

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation, Node, Document

xml_string1= '''<layout gap="0"><element id="1" x="180" y="200" width="360" height="240" /><element id="2" x="540" y="200" width="360" height="240" /><element id="3" x="900" y="200" width="360" height="240" /><element id="4" x="180" y="440" width="360" height="480" /><element id="5" x="540" y="440" width="720" height="480" /><element id="6" x="1260" y="200" width="480" height="720" /></layout>'''

xml_string2 = '''<layout gap="0"><element id="1" x="180" y="200" width="360" height="240" /><element id="2" x="540" y="200" width="720" height="240" /><element id="3" x="180" y="440" width="360" height="480" /><element id="4" x="540" y="440" width="360" height="480" /><element id="5" x="900" y="440" width="360" height="480" /><element id="6" x="1260" y="200" width="480" height="720" /></layout>'''

xml_string3 = '''<layout gap="0"><element id="1" x="360" y="200" width="360" height="240" /><element id="2" x="720" y="200" width="360" height="240" /><element id="3" x="360" y="440" width="720" height="480" /><element id="4" x="1080" y="200" width="480" height="720" /></layout>'''

xml_string4 = '''<layout gap="0"><element id="1" x="360" y="200" width="360" height="240" /><element id="2" x="720" y="200" width="360" height="240" /><element id="3" x="360" y="440" width="360" height="480" /><element id="4" x="720" y="440" width="360" height="480" /><element id="5" x="1080" y="200" width="480" height="720" /></layout>'''

xml_string5 = '''<layout gap="0"><element id="1" x="360" y="200" width="360" height="360" /><element id="2" x="720" y="200" width="360" height="360" /><element id="3" x="360" y="560" width="360" height="360" /><element id="4" x="720" y="560" width="360" height="360" /><element id="5" x="1080" y="200" width="480" height="720" /></layout>'''

xml_string6 = '''<layout gap="0"><element id="1" x="180" y="200" width="360" height="240" /><element id="2" x="540" y="200" width="360" height="240" /><element id="3" x="900" y="200" width="360" height="240" /><element id="4" x="180" y="440" width="360" height="240" /><element id="5" x="180" y="680" width="360" height="240" /><element id="6" x="540" y="440" width="360" height="480" /><element id="7" x="900" y="440" width="360" height="480" /><element id="8" x="1260" y="200" width="480" height="720" /></layout>'''

xml_string7 = '''<layout gap="0"><element id="1" x="180" y="200" width="360" height="240" /><element id="2" x="540" y="200" width="720" height="240" /><element id="3" x="180" y="440" width="360" height="240" /><element id="4" x="180" y="680" width="360" height="240" /><element id="5" x="540" y="440" width="360" height="480" /><element id="6" x="900" y="440" width="360" height="480" /><element id="7" x="1260" y="200" width="480" height="720" /></layout>'''

xml_string8 = '''<layout gap="0"><element id="1" x="240" y="200" width="240" height="240" /><element id="2" x="480" y="200" width="240" height="240" /><element id="3" x="720" y="200" width="240" height="240" /><element id="4" x="240" y="440" width="240" height="480" /><element id="5" x="480" y="440" width="480" height="480" /><element id="6" x="960" y="200" width="480" height="720" /><element id="7" x="1440" y="200" width="240" height="240" /><element id="8" x="1440" y="440" width="240" height="240" /><element id="9" x="1440" y="680" width="240" height="240" /></layout>'''


class Element(object):
    def __init__(self, id):
        self.id = id
        self.x_pos = 0
        self.y_pos = 0
        self.width = 0
        self.height = 0
        
    def setPosX(self, v):
        self.x_pos = v
    def setPosY(self, v):
        self.y_pos = v
    def setWidth(self, v):
        self.width = v

    def setHeight(self, v):
        self.height = v

    def __repr__(self):
        s = "id=%s, x_pos=%s, y_pos=%s"%\
            (self.id, self.x_pos, self.y_pos)
        return s

def getAllElements(xml_string, elements):
    global cell_gap
    doc = minidom.parseString(xml_string)
    layout_node = doc.getElementsByTagName("layout")[0]
    cell_gap = int(layout_node.getAttribute("gap"))

    element_nodes = doc.getElementsByTagName("element")
    for node in element_nodes:
        id = node.getAttribute("id")
        e = Element(id)
        e.setPosX(int(node.getAttribute("x")))
        e.setPosY(int(node.getAttribute("y")))
        e.setWidth(int(node.getAttribute("width")))
        e.setHeight(int(node.getAttribute("height")))
        #print repr(e)
        elements.append(e)

def genJson(elements):
    layout = {}
    layout["gap"] = cell_gap
    layout["total_elements"] = len(elements)

    element_list = []
    for e in elements:
        element = {}
        element["id"] = str(e.id)
        element["xpos"] = str(e.x_pos)
        element["ypos"] = str(e.y_pos)
        element["width"] = str(e.width)
        element["height"] = str(e.height)
        element_list.append(element)

    layout = {"gap": cell_gap,
              "total_element": len(element),
              "element_list": element_list}
    #print layout
    return layout

def initializeGlobals():
    global elements
    elements = []
    
def generateFullLayoutJson(xml_string):
    global elements
    initializeGlobals()
    getAllElements(xml_string, elements)
    return genJson(elements)

cell_gap = 6
elements = []

if __name__ == "__main__":
    generateFullLayoutJson(xml_string1)
    generateFullLayoutJson(xml_string2)
    generateFullLayoutJson(xml_string3)
    generateFullLayoutJson(xml_string4)
    generateFullLayoutJson(xml_string5)
    generateFullLayoutJson(xml_string6)
    generateFullLayoutJson(xml_string7)
    generateFullLayoutJson(xml_string8)
    
#class Element(object):
#    def __init__(self, index, id):
#        self.id = id
#        self.x_len = 0
#        self.y_len = 0
#        self.x_pos = 0
#        self.y_pos = 0
#        self.index = 0
#        self.type = 0
#        self.width = 0
#        self.height = 0
#        self.x_gap = 0
#        self.y_gap = 0
#        self.occupy_point_list = []
#        
#    def setX(self, v):
#        self.x_len = v
#    def setY(self, v):
#        self.y_len = v
#    def setPosX(self, v):
#        self.x_pos = v
#    def setPosY(self, v):
#        self.y_pos = v
#    def setType(self, type):
#        self.type = type
#    
#
#    def repr(self):
#        s = "id=%s, xlen=%s, ylen=%s, x_pos=%s, y_pos=%s"%\
#            (self.id, self.x_len, self.y_len, self.x_pos, self.y_pos)
#        return s
#    
#xml_string = '''<layout xpos="200" ypos="200" cell_width="102" cell_x_width="113" cell_y_width="125" cell_gap="5"><element id="1" xlen="3" ylen="2" type="1"/><element id="2" xlen="3" ylen="2" type="1"/><element id="3" xlen="3" ylen="2" type="1"/><element id="4" xlen="3" ylen="2" type="1"/><element id="5" xlen="3" ylen="4" type="1"/><element id="6" xlen="3" ylen="2" type="2"/><element id="7" xlen="3" ylen="4" type="1"/><element id="8" xlen="4" ylen="6" type="1"/></layout>'''


#def getAllElements(xml_string, elements):
#    global global_xpos, global_ypos, cell_width, cell_x_width, cell_y_width, cell_gap
#    doc = minidom.parseString(xml_string)
#    layout_node = doc.getElementsByTagName("layout")[0]
#    global_xpos = int(layout_node.getAttribute("xpos"))
#    global_ypos = int(layout_node.getAttribute("ypos"))
#    cell_width = int(layout_node.getAttribute("cell_width"))
#    cell_x_width = int(layout_node.getAttribute("cell_x_width"))
#    cell_y_width = int(layout_node.getAttribute("cell_y_width"))
#    cell_gap = int(layout_node.getAttribute("cell_gap"))
#
#    element_nodes = doc.getElementsByTagName("element")
#    index = 0;
#    for node in element_nodes:
#        id = node.getAttribute("id")
#        e = Element(index, id)
#        e.setX(int(node.getAttribute("xlen")))
#        e.setY(int(node.getAttribute("ylen")))
#        #print "ylen for ", id, "is ", e.y_len
#        e.setType(int(node.getAttribute("type")))
#        elements.append(e)
#        index += 1
#
#def findNextValid(start):
#    global layout_free_array
#    found = False
#    for x in range(start, len(layout_free_array)):
#        if layout_free_array[x] == 0:
#            found = True
#            break
#    if found:
#        return x
#    return -1
#
#def mark_x_gap_point(width, start):
#    global x_gap_point
#    p = start / width
#    #print "----mark x :", start, p
#    if p not in x_gap_point:
#        x_gap_point.append(p)
#
#def mark_y_gap_point(width, start):
#    global y_gap_point
#    p = start % width
#    #print "----mark y :", start, p
#    if p not in y_gap_point:
#        y_gap_point.append(p)
#    
#def occupy(array_width, start, element):
#    global layout_free_array
#    global occupy_magic
#
#    mark_x_gap_point(array_width, start)
#    mark_y_gap_point(array_width, start)
#    pos = []
#    for m in range(start, start+element.y_len):
#        pos += [m]
#        pos = pos + [m+n*array_width for n in range(1, element.x_len)]
#    for p in pos:
#        layout_free_array[p] = occupy_magic
#    occupy_magic += 1
#    element.occupy_point_list = pos
#
#def findXGapDelta(array_width, start):
#   pos_list = [i-array_width for i in xrange(0,start,array_width) if i-array_width>0]
#   how_many_gap = 0
#   num = 0
#   for pos in pos_list:
#       if not num == layout_free_array[pos]:
#           how_many_gap +=1
#           num = layout_free_array[pos]
#   return how_many_gap
#
#def findYGapDelta(array_width, start):
#   pos_list = []
#   for i in xrange(0, start%array_width):
#       pos_list.append(start-1-i)
#   how_many_gap = 0
#   num = 0
#   for pos in pos_list:
#       if not num == layout_free_array[pos]:
#           how_many_gap +=1
#           num = layout_free_array[pos]
#   return how_many_gap
#
#def makeXYlen(width, point):
#    x = point / width
#    y = point % width
#    return x, y
#
#def makeElementXYlens(width, element):
#    x_lens = []
#    y_lens = []
#    for point in element.occupy_point_list:
#        x, y = makeXYlen(width, point)
#        if x not in x_lens:
#            x_lens.append(x)
#        if y not in y_lens:
#            y_lens.append(y)
#    return x_lens, y_lens
#
#def genPosition(array_width, start):
#    #print "---------start--", start
#    global cell_gap, cell_width, cell_x_width, cell_y_width,  global_xpos, global_ypos
#    x_cell_delta = start / array_width
#    y_cell_delta = start % array_width
#    x = global_xpos + x_cell_delta * cell_x_width
#    x_gap_delta = findXGapDelta(array_width, start)
#    x += x_gap_delta * cell_gap
#    y = global_ypos + y_cell_delta * cell_y_width
#    y_gap_delta = findYGapDelta(array_width, start)
#    y += y_gap_delta * cell_gap
#    
#    return (x, y)
#    
#def genPosterPosition(width, elements):
#    global layout_free_array, global_xpos, global_ypos
#    for e in elements:
#        start = findNextValid(e.index)
#        occupy(width, start, e)
#        e.x_pos, e.y_pos = genPosition(width, start)
#
#def computeGapNumber(element_points, gap_points):
#    min = int(element_points[0])
#    max = int(element_points[len(element_points)-1])
#    gap_num = 0
#    for point in gap_points:
#        if point > min and point <=max:
#            gap_num +=1
#    return gap_num
#
#def genPosterSize(width, elements):
#    global cell_x_width, cell_y_width, cell_gap
#    for e in elements:
#        x_lens, y_lens = makeElementXYlens(width, e)
#        #print "999999999 ",x_lens, y_lens
#        e.x_gap = computeGapNumber(x_lens, x_gap_point)
#        e.y_gap = computeGapNumber(y_lens, y_gap_point)
#        e.width = e.x_gap * cell_gap + e.x_len * cell_x_width
#        e.height = e.y_gap * cell_gap + e.y_len * cell_y_width
#    
#        
#def genXML(elements):
#    global global_xpos, global_ypos, cell_width, cell_x_width, cell_y_width, cell_gap
#    doc = Document()
#    layout = doc.createElement("layout")
#    #layout.setAttribute("xpos", str(global_xpos))
#    #layout.setAttribute("ypos", str(global_ypos))
#    layout.setAttribute("cell_width", str(cell_width))
#    layout.setAttribute("cell_x_width", str(cell_x_width))
#    layout.setAttribute("cell_y_width", str(cell_y_width))
#    layout.setAttribute("cell_gap", str(cell_gap))
#    doc.appendChild(layout)
#
#    for e in elements:
#        element = doc.createElement("element")
#        element.setAttribute("id", str(e.id))
#        element.setAttribute("xpos", str(e.x_pos))
#        element.setAttribute("ypos", str(e.y_pos))
#        element.setAttribute("x_len", str(e.x_len))
#        element.setAttribute("y_len", str(e.y_len))
#        layout.setAttribute("width", str(e.width))
#        layout.setAttribute("height", str(e.height))
#        #element.setAttribute("type", str(e.type))
#        layout.appendChild(element)
#    return doc.toxml()
#
#def genJson(element):
#    global global_xpos, global_ypos, cell_width, cell_x_width, cell_y_width, cell_gap
#    layout = {}
#    #layout["xpos"] = global_xpos
#    #layout["ypos"] = global_ypos
#    layout["cell_width"] = cell_width
#    layout["cell_x_width"] = cell_x_width
#    layout["cell_y_width"] = cell_y_width
#    layout["cell_gap"] = cell_gap
#    layout["total_elements"] = len(elements)
#
#    element_list = []
#    for e in elements:
#        #print "============", e.occupy_point_list
#        element = {}
#        element["id"] = str(e.id)
#        element["xpos"] = e.x_pos
#        element["ypos"] = e.y_pos
#        element["x_len"] = e.x_len
#        element["y_len"] = e.y_len
#        element["width"] = e.width
#        element["height"] = e.height
#        #element["type"] = e.type
#        element_list.append(element)
#
#    layout["element_list"] = element_list
#    return layout
#
#def generateFullLayoutXML(width, xml_string):
#    global elements
#    initializeGlobals()
#    getAllElements(xml_string, elements)
#    genPosterPosition(width, elements)
#    genPosterSize(width, elements)
#    return genXML(elements)
#
#def generateFullLayoutJson(width, xml_string):
#    global elements
#    initializeGlobals()
#    getAllElements(xml_string, elements)
#    genPosterPosition(width, elements)
#    genPosterSize(width, elements)
#    return genJson(elements)
#
#def initializeGlobals():
#    global elements, global_xpos, global_ypos, layout_free_array, \
#           array_width, cell_width, cell_x_width, cell_y_width, cell_gap, occupy_magic
#    elements = []
#    global_xpos = 0
#    global_ypos = 0
#    layout_free_array = [0,]*100
#    occupy_magic = 1
# #   array_width = 3
#    cell_width = 0
#    cell_x_width = 0
#    cell_y_width = 0
#    cell_gap = 0
#    
#elements = []
#global_xpos = 0
#global_ypos = 0
#layout_free_array = [0,]*100
#occupy_magic = 1
##array_width = 3
#cell_width = 0
#cell_x_width = 0
#cell_y_width = 0
#cell_gap = 0
#x_gap_point = []
#y_gap_point = []
#
#if __name__ == "__main__":
#    #print generateFullLayoutXML(6, xml_string)
#    print generateFullLayoutJson(6, xml_string)
#    print "x_gap_point:", x_gap_point
#    print "y_gap_point:", y_gap_point
    
