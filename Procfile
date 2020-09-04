web: flask db init; flask db migrate; flask db upgrade; uwsgi wsgi.ini
worker: celery worker -A celery-runner --loglevel=info