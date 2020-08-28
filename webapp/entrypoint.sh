#!/usr/bin/env bash

echo --------------------
echo Going to wait for Mysql
echo --------------------
while ! mysqladmin ping -h"db" -u "root" -p"${MYSQL_ROOT_PASSWORD}" --silent; do
    echo "MySQL not available waiting"
    sleep 1
done
if [ ! -d "migrations" ]; then
    echo --------------------
    echo INIT THE migrations folder
    echo --------------------
    export FLASK_APP=run.py; flask db init
fi
echo --------------------
echo Generate migration
echo --------------------
flask db migrate
echo --------------------
echo --------------------
echo Database upgrade
echo --------------------
flask db upgrade
echo --------------------
echo --------------------
echo Start App
echo --------------------
python3 gserver.py
