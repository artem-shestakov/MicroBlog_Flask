#!/usr/bin/env bash

echo --------------------
echo Starting Celery
echo --------------------
/usr/bin/supervisord --nodaemon --user=root
