#!/usr/bin/env python
import os
import time

cwd = os.getcwd()
target_dir = os.path.realpath(os.path.join(cwd, "../wasuvod_source"))

def check_file_saving(f):
    ''' check whether the file is saving, because the file always be
    large, and copied from network, after the file saving.

    get the file size twice in seconds, if the file size no difference,
    it means the file was finished saving, if not, the file is in saving.
    return True for in saving, False for not
    '''
    sleeptime = 1 # second
    filesize1 = os.path.getsize(f)
    time.sleep(sleeptime)
    filesize2 = os.path.getsize(f)
    if filesize2 > filesize1:
        return True
    elif filesize2 == filesize1:
        return False
    return False

def moveit(f):
    ''' move file to the target log directory, and change the mode of
    the file for other account to read it, the input should be a full
    path name '''
    fname = os.path.basename(f)
    targetfile = os.path.join(target_dir, fname)
    ret = os.system("mv %s %s"%(f, targetfile))
    if ret != 0:
        print "fail(%s) to move file %s to %s"%(ret, f, targetfile)
        return False
    print "successfully move file %s to %s"%(f, targetfile)
    ret = os.system("chmod 777 %s"%targetfile)
    if ret != 0:
        print "fail(%s) to change mode of file %s"%(ret, targetfile)
        return False
    print "successfully change mode of file %s"%targetfile
    return True

if __name__ == "__main__":
    files = os.listdir(cwd)
    num_handled = 0
    for f in files:
        if not f.endswith('.bz2'):
            continue
        fpath = os.path.join(cwd, f)
        print "handling file %s, size(%s)"%(fpath, os.path.getsize(fpath))
        if check_file_saving(fpath) is True:
            print "file %s is in saving status, just ignore it, "\
                  "and check it later"
            continue
        moveit(fpath)
        num_handled += 1

    print "%s files were handled"%num_handled
