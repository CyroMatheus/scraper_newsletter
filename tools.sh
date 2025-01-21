#!/bin/bash
RESTORE='\033[0m'
RED='\033[00;31m'
GREEN='\033[00;32m'
YELLOW='\e[0;33m'

readonly root_folder=$(pwd)
export PROJ_BASE="$(dirname "${BASH_SOURCE[0]}")"
CD=$(pwd)
cd $PROJ_BASE
export PROJ_BASE=$(pwd)
cd $CD

function development_tools() {
    echo -e "${YELLOW}\n\n---------------------------------${RESTORE}\n"
    echo -e "${GREEN}        development tools${RESTORE}\n"
    echo -e "${YELLOW}---------------------------------${RESTORE}\n"
    echo -e "${YELLOW}runserv${RESTORE}                Start the ${GREEN}django${RESTORE} server\n"
    echo -e "${GREEN}dkup${RESTORE}                    Starts a dockerized ${RED}full development environment${RESTORE}\n"
}

function runserv(){
    cd $root_folder/app

    python3 ./back/app/manage.py migrate --run-syncdb
    python3 ./back/app/manage.py collectstatic --noinput
    python3 ./back/app/manage.py makemigrations --noinput
    python3 ./back/app/manage.py migrate --noinput
    python3 ./back/app/manage.py runserver 0.0.0.0:8000
    
    exitcode=$?
    cd $root_folder
    return $exitcode
}

# function dkbuild {
#     CD=$(pwd)
#     cd $PROJ_BASE
#     docker build -t app_news .
#     exitcode=$?
#     cd $CD
#     return $exitcode
# }

function dkup {
    CD=$(pwd)
    cd $PROJ_BASE
    docker-compose -f docker-compose.yml up
    exitcode=$?
    cd $CD
    return $exitcode
}

development_tools