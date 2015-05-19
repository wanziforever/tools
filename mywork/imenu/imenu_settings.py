#!/usr/bin/env python

import os

ITEMS_BASE_DIRECTORY = "./menuitems"
log_stack = []

# following is the envirement passed to command
kernel_path = os.path.realpath(os.path.join(__file__, "../"))
imenu_env = {'kernel': kernel_path}


#imenu display report string definition
key_info_str = ""

