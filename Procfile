web: export PORT=3000; export FLASK_APP=run.py; export WEBAPP_ENV=Heroku; flask db init; flask db migrate; flask db upgrade; uwsgi wsgi.ini
celery: celery worker -A celery-runner --loglevel=info