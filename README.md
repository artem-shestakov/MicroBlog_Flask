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

## Deploy
### Heroku
Create app om Heroku:
```shell script
$ heroku create
Creating app... done, ⬢ rocky-brushlands-98089
https://rocky-brushlands-98089.herokuapp.com/ | https://git.heroku.com/rocky-brushlands-98089.git
```
Go to Heroku -> Your app -> Installed add-ons. Select your PostgreSQL add-on and copy Database Credentials from settings page. Write it on config.py file.

![Heroku Database Credentials](https://i.ibb.co/8xt4QVB/Heroku-Database-Credentials.png)

Add CloudAMQP add-on. Go to Heroku -> Your app -> Installed add-ons. Select your CloudAMQP add-on and copy Database Credentials from detail page. Write it on config.py file.

![Herolu CloudAMQP](https://i.ibb.co/fNkjS2F/Heroku-AMQP.png)

Deploy your code to Heroku git:
```shell script
$ git push heroku master
Counting objects: 100% (1364/1364), done.
Delta compression using up to 12 threads
Compressing objects: 100% (1297/1297), done.
Writing objects: 100% (1364/1364), 1.22 MiB | 920.00 KiB/s, done.
Total 1364 (delta 629), reused 0 (delta 0)
remote: Compressing source files... done.
remote: Building source:
remote: 
remote: -----> Python app detected
remote: -----> Installing python-3.8.5
...
remote:        https://rocky-brushlands-98089.herokuapp.com/ deployed to Heroku
remote: 
remote: Verifying deploy... done.
To https://git.heroku.com/rocky-brushlands-98089.git
 * [new branch]      master -> master
```
