#!/usr/bin/env python

entry = "1.1|5010|com.jamdeo.tv.vod|1|8610030090000110000000597dc34283|0|1001|17%%mt5399%%LED50K680X3DU%%LED50K680X3DU%%Hisense|1000|1416054372956|{0}|40010030215|1004|SD\n"

log_file = "/data/testlogs/vod_20141115130617_221525.log"

def gen(fd, num, id):
    for i in range(num):
        fd.write(entry.format(id))

def call_gen(fname):
    fd = open(fname, "w")

    gen(fd, 10000, 40010013033)
    gen(fd, 9999, 40010013307)
    gen(fd, 9998, 40010001244)
    gen(fd, 9997, 40010013384)
    gen(fd, 9996, 40010013378)
    gen(fd, 9995, 40010008277)
    gen(fd, 9994, 40010013397)
    gen(fd, 9993, 40010013497)
    gen(fd, 9992, 40010012562)
    gen(fd, 9991, 40010005225)
    gen(fd, 9990, 40010002840)
    gen(fd, 9989, 40010003573)
    gen(fd, 9988, 40010003502)
    gen(fd, 9987, 40010013193)
    gen(fd, 9986, 40010002851)
    gen(fd, 9985, 40010012144)
    gen(fd, 9984, 20010993033)
    gen(fd, 9983, 40010013315)
    gen(fd, 9982, 60010003831)
    gen(fd, 9981, 40010002747)
    
    fd.close()

if __name__ == "__main__":
    call_gen(log_file)
