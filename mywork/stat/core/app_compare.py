#!/usr/bin/env python
'''
     compare two app.properties, then console result to file  'app_compare_result'
'''
import sys

def generate(result1, result2):
    former = []
    last = []
    for i in result1:
        r1 = i.strip()
        if(r1 and r1[0] != '#'):
            former.append(r1 + '\n')
    for j in result2:
        r2= j.strip()
        if(r2 and r2[0] != '#'):
            last.append(r2 + '\n')
    former = set(former)
    last = set(last)
    same = former & last
    delete = list(former ^ same)
    add = list(last ^ same)
    if delete:
        delete = ['#THIS IS FORMER, SO NEED TO  -- DELETE --!\n\n'] +delete
    if add:
        add = ['\n\n\nTHIS IS NOW, SO NEED TO  -- ADD -- !\n\n'] + add
    return delete + add

if __name__ == "__main__":
    f1=open(sys.argv[1], "r")
    f2=open(sys.argv[2], "r")
    result1=f1.readlines()
    result2=f2.readlines()
    f1.close()
    f2.close()

    writedifferent = generate(result1, result2)
    if not writedifferent:
        writedifferent.append("ALL IS ''SAME'' WITH LAST!!")

    f = open('./app_compare_result', "w")
    f.write("".join(writedifferent))
    f.close()
    print "\nCompare App.properties Done!\n" 