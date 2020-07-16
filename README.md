# Flask_project

## Init or change project
### Create all tables in DB
```sh
$ export FLASK_APP=manage.py
$ flask shell
>>> db.create_all()
```
### Migrate DataBase schema
```shell script
$ export FLASK_APP=main.py
$ flask db migrate
$ flask db upgrade
```