#!/usr/bin/env bash

echo --------------------
echo Starting Celery
echo --------------------
#celery worker -A celery-runner --loglevel=info
/usr/bin/supervisord --nodaemon --user=root
