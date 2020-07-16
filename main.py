from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import DevConfig

# Init Flask application and app config
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)



# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship("Post", backref="users", lazy="dynamic")

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"<User '{self.username}'>"


#Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Post '{self.title}'>"


# Root route
@app.route("/")
def home():
    return "<h1>Hello world</h1>"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
