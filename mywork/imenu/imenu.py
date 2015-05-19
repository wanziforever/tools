#!/usr/bin/env python

import os
import sys
import imenu_settings
from utils import info, debug, err, errtrace, warn

current_label = None
current_items = []

def setup_env():
    for variable, value in imenu_settings.imenu_env.items():
        os.environ[variable] = value

class Item(object):
    def __init__(self, label, name, path):
        self.path = path
        self.label = label
        self.name = name

    def display_name(self):
        return self.name

    def show_info(self):
        return "(Iterm) Label: %s, name: %s"%(self.label, self.name)

class MenuItem(Item):
    def __init__(self, label, name, path):
        Item.__init__(self, label, name, path)
        self.build_items()
    def build_items(self):
        self.items = get_items_for_dir(self.path, self.label)

    def show_info(self):
        return "(Menu) Label: %s, name: %s"%(self.label, self.name)

class CommandItem(Item):
    def __init__(self, label, name, path):
        Item.__init__(self, label, name, path)

    def show_info(self):
        return "(Command) Label: %s, name: %s"%(self.label, self.name)

    def execute(self):
        setup_env()
        os.system(self.path)
    
menu_items = {}
def append_item(label, item):
    global menu_items
    if label is None:
        err("append_item() label is None, exit")
        exit(0)
    if label in menu_items:
        err("append_item() duplicate item found for label:%s, item:%s"%\
            (label, item.display_name()))
        exit(0)
    if item is None:
        err("append_item() item is None, exit")
        exit(0)
    menu_items[label] = item
        
def get_items_for_dir(path, label=None):
    files = os.listdir(path)
    p = ""
    item = None
    items = []
    new_label = ""
    
    for f in files:
        num, name = f.split("_", 1)
        if not num.isdigit():
            continue
        if label is None:
            new_label = num
        else:
            new_label = label + "." + num
            
        p = os.path.join(path, f)
        if os.path.isfile(p):
            item = CommandItem(new_label, name, p)
        elif os.path.isdir(p):
            item = MenuItem(new_label, name, p)
        else:
            continue
        append_item(new_label, item)
        items.append(item)
    return items
            
def filter_menu(plabel):
    ''' if parent label is None, it means it is the root menu '''
    max_item = 20
    count = 1
    to_show = []
    label = ""
    for i in xrange(1, max_item+1):
        if plabel is None:
            label = str(i)
        else:
            label = plabel + "." + str(i)
        if label not in menu_items:
            break
        else:
            to_show.append(menu_items[label])
        
    return to_show
        
def display_menu(items):
    global current_label
    if current_label is not None:
        print "\n\tCURRENT MENU: <%s> %s\n"%\
              (current_label, menu_items[current_label].display_name().upper())
    else:
        print "\n\tCURRENT MENU: MAIN MENU\n"
    menu = sorted(items, key=lambda items:items.label)
    index = 1
    if len(menu) == 0:
        print "\t<empty>\n"
        print "type 'u' to return to up menu"
        return 
    for i in menu:
        if i.__class__.__name__ == "MenuItem":
            print "\t%s %s"%(index, i.display_name().upper())
        else:
            print "\t%s %s"%(index, i.display_name())
        index += 1

def validate_label(label):
    if label.lower() == "q":
        return True, ""
    
    if label.isdigit():
        return True, ""
    try:
        digits = label.split('.')
        for d in digits:
            if not d.isdigit():
                raise
    except:
        return False, '''input should be digit or digits separeted by "."'''
    return True, ""

def show_current_menu():
    global current_items
    items = filter_menu(current_label)
    display_menu(items)
    current_items = items
    
def up_label(label):
    ''' return uplevel of label '''
    if label is None:
        return None
    if label.find(".") == -1:
        return None
    m = label.split('.')
    return ".".join(m[:-1])

def go_to_label(inp):
    global current_label
    if inp.find(".") == -1:
        if current_label is None:
            return inp
        else:
            return current_label + "." + str(inp)
    return inp

def navigate():
    global current_label
    while(True):
        inp = raw_input("Enter your choice: ")
        inp = inp.strip()
        if inp.lower() == "q":
            exit(0)
        if inp == "":
            show_current_menu()
            continue
        if inp.lower() == "u":
            current_label = up_label(current_label)
            show_current_menu()
            continue
        succ, msg = validate_label(inp)
        if succ is False:
            err(msg)
            continue
        print "your choice is %s"%inp
        label = go_to_label(inp)
        if label not in menu_items:
            err("label is out of range")
            continue
        item = menu_items[label]
        if item.__class__.__name__ == "CommandItem":
            item.execute()
            show_current_menu()
        else:
            current_label = label
            show_current_menu()
        continue
    
#cache_management_menu = MenuItem("CACHE MANAGEMENT")

if __name__ == "__main__":
    cwd = os.getcwd()
    root_items_path = os.path.join(cwd, imenu_settings.ITEMS_BASE_DIRECTORY)
    root_items_path = os.path.realpath(root_items_path)
    get_items_for_dir(root_items_path)
    
    #for label, i in menu_items.items():
    #    print "%s %s"%(label, i.display_name())

    display_menu(filter_menu(None))
    navigate()
