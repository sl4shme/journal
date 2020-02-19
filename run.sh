#!/bin/bash
trap on_sigint SIGINT
trap on_sigusr SIGUSR1

killed_int=0
killed_usr=0

function on_sigint() {
    killed_int=1
}

function on_sigusr() {
    killed_usr=1
}

function watch_file() {
    mdate=`stat -c %y $1`
    while true; do
        sleep 0.1
        last_mdate=`stat -c %y $1`
        if [[ "$mdate" != "$last_mdate" ]] ; then
            mdate=$last_mdate
            kill -s $3 $2
        fi
    done
}

watch_file ./app/templates/form.html $$ SIGINT &
watch_file ./app/routes.py $$ SIGINT &
watch_file ./journal.py $$ SIGINT &

watch_file ./flask.log $$ USR1 &

flask run >> ./flask.log 2>&1 &
flask_pid=$!

while true ; do
    if [[ "$killed_int" == "1" ]] ; then
        kill $flask_pid
        flask run >> ./flask.log 2>&1 &
        flask_pid=$!
        echo -e "\n\nReloaded. Press 'c' again to kill"
        read -rsn 1 -t 2 answer
        if [[ "$answer" == "c" ]] ; then
            kill $flask_pid
            exit 0
        fi
        killed_int=0
        killed_usr=1
    fi
    if [[ "$killed_usr" == "1" ]] ; then
        clear
        tail -n 5 flask.log
        killed_usr=0
    fi
    sleep 0.1
done
