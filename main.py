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

# Association tables many-to-many
# Posts-to-Tags
tags = db.Table("post_tag",
                db.Column("post_id", db.Integer(), db.ForeignKey("posts.id")),
                db.Column("tag_id", db.Integer(), db.ForeignKey("tags.id"))
                )


# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship("Post", backref="users", lazy="dynamic")

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"<User '{self.username}'>"


# Post model
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref="posts", lazy="dynamic")
    tags = db.relationship("Tag", secondary=tags, backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Post '{self.title}'>"


# Comment model
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    data = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"))

    def __repr__(self):
        return f"<Comment '{self.text[:15]}'>"


# Tag model
class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Tag '{self.title}'>"


# Root route
@app.route("/")
def home():
    return "<h1>Hello world</h1>"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
