#!/usr/bin/env python

import struct

def log(string):
    # sys.stdout.write(string)
    print string
    
def open_file(file_name, mode = "r"):
    """ open file, return None if fail, capture the system exception,
    and handle open file fail by self """
    try:
        fp = open(file_name, mode)
        return fp
    except:
        return None

def call_read_bin():
    fd = open_file("/home/denny/fsdesc", "rb")
    if fd is None:
        log("open file fail")
        exit()
    (a, b, c) = struct.unpack("@Ii256s", fd.read(4 + 4 + 256))
    print a
    print b
    print c

if __name__ == "__main__":
    call_read_bin()
