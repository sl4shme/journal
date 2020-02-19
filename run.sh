#!/bin/bash
trap on_sigint SIGINT

killed=0

function on_sigint() {
    killed=1    
}

function watch_file() {
    mdate=`stat -c %y $1`
    while true; do
        sleep 0.1
        last_mdate=`stat -c %y $1`
        if [[ "$mdate" != "$last_mdate" ]] ; then
            mdate=$last_mdate
            kill -s SIGINT $2
        fi
    done
}

watch_file ./app/templates/form.html $$ &
watch_file ./app/routes.py $$ &
watch_file ./journal.py $$ &

flask run >> ./flask.log 2>&1 &
flask_pid=$!

while true ; do
    if [[ "$killed" == "1" ]] ; then
        kill $flask_pid
        flask run >> ./flask.log 2>&1 &
        flask_pid=$!
        echo "Reloaded. Press 'c' again to kill"
        read -rsn 1 -t 2 answer
        if [[ "$answer" == "c" ]] ; then
            kill $flask_pid
            exit 0
        fi
        killed=0
    else
        sleep 0.1
    fi
done
