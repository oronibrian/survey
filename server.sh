#!/bin/bash

pid=$(ps aux | grep "./manage.py runserver" | grep -v grep | head -1 | xargs | cut -f2 -d" ")

if [[ -n "$pid" ]]; then
    kill $pid
fi

fuser -k 8006/tcp
python manage.py runserver 127.0.0.1:8006

#python manage.py runserver 0.0.0.0:8006
