#!/usr/bin/env python
import subprocess

path_of_loadSim = "./wfesim"
content_id_prefix = "2012112900"
content_id_base = 50010
mpe_host_ip = "10.0.64.3"
media_path = "/Media"
counter = 0
MAX_COUNTER = 400
media_file = "6100000882744_dahuaxiyouyueguangbaohe_2M.mpg"
#MAX_COUNTER = 600
#media_file = "4000000769762_minganzhiqindierxilie6_HD_z7.5P.ts"
media_file_full_name = media_path + "/" + media_file

def loadWFE_call():
    global counter, MAX_COUNTER, media_file_full_name
    print "loadSim_call enter ..."
    while (counter < MAX_COUNTER):
        content_id = (
            content_id_prefix + str(content_id_base + counter)
            )
        cmd = (
            "%s -c %s -u %s -m %s -n 1 -o 1"
            %(path_of_loadSim, content_id, media_file_full_name, mpe_host_ip)
            )
        print "execute command " + cmd
        subprocess.call(cmd, shell=True)
        counter = counter + 1;
    print "loadSim_call exit ..."

#//////////// main start //////////////
if __name__ ==  "__main__":
    loadWFE_call()
