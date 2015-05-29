#!/bin/bash

if [ $# -lt 2 ]; then
    echo "usage: $0 [pidfile] [command]" 1>&2
    exit 1
fi

PIDFILE=$1
shift 1
#SLEEPTIME=$1
#shift 1
COMMAND=$1
shift 1

SLEEPTIME=1

#check pid file for process
if [ -a $PIDFILE ]; then
    c=$(ps -p $(cat $PIDFILE) | wc -l)
    if [ $c -eq 2 ]; then
        echo 'already running' 1>&2
        ls -l $PIDFILE 1>&2
        exit 1
    fi
fi

#dump pid
echo "$$" > $PIDFILE

while true; do
    #run command
    $COMMAND "$@"
    if [ $? -ne 0 ]; then
        exit 2
    fi

    #remove pid file
    echo "sleep ${SLEEPTIME} minutes ..."
    sleep $((SLEEPTIME))m
done
