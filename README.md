# MicroBlog by Flask

## Deploy
### Heroku
Create app on Heroku:
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
## Init or change project
### Create all tables in DB
```shell script
$ flask init database

All tables has been created
Role 'user' has been added
Role 'administrator' has been added
```
### Create blog administartor or user
User 'create user' command. If set -a flag user will superuser right. 
```shell script
flask create user -a

User's email address: administrator@microblog.local              
User's first name: Administrator
Enter password: 
Repeat for confirmation: 
User administrator@microblog.local added.
```

### Migrate DataBase schema
```shell script
$ export FLASK_APP=run.py
$ flask db migrate
$ flask db upgrade
```
