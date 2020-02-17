#!/bin/bash
trap stop SIGINT

on_stop=0

function stop() {
    on_stop=1
    killall watch
}

while true ; do 
    export FLASK_APP=journal_web.py
    flask run >> ./flask.log 2>&1 & 
    if [[ "$on_stop" -eq "1" ]] ; then
        echo "Press 'c' again to kill"
        read -rsn 1 -t 2 answer
        if [[ "$answer" == "c" ]] ; then
            killall flask
            tail ./flask.log
            exit 0
        fi
        on_stop=0
    fi
    watch -t -g "ls -l ./app/templates/form.html"
    killall flask
done
