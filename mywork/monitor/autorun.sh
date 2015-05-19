#!/bin/bash

while true; do
    d=$(date)
    echo "$d generate wasu3 snapshot for user 1234"
    ./html_export3.py wasu3 1234
    echo "$d generate wasu3 snapshot for user 5678"
    ./html_export3.py wasu3 5678
    d=$(date)
    echo "$d generate cntv snapshot"
    ./html_export.py cntv
    d=$(date)
    echo "$d generate wasu snapshot"
    d=$(date)
    ./html_export.py wasu
    echo "$d generate edu snapshot"
    ./html_export.py edu
    d=$(date)
    sleep 60
done

