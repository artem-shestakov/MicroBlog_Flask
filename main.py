from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func, text
from config import DevConfig
from datetime import datetime

# Init Flask application and app config
app = Flask(__name__)
app.config.from_object(DevConfig)

# SQLAlchemy DB object
db = SQLAlchemy(app)

# Alembic migrate object
migrate = Migrate(app, db)

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
    username = db.Column(db.String(255), nullable=False, unique=True)
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
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default=datetime.now)
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
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default=datetime.now)
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"))

    def __repr__(self):
        return f"<Comment '{self.text[:15]}'>"


# Tag model
class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Tag '{self.title}'>"


# Functions
def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label("total")).join(tags).group_by(Tag).order_by(text('total DESC')).limit(5).all()
    return recent, top_tags


# Root route
@app.route("/")
@app.route("/<int:page>")
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).pagination(page, 10, False)
    recent, top_tags = sidebar_data()
    return render_template("home.html", posts=posts, recent=recent, top_tags=top_tags)


@app.route("/post/<ind:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post


if __name__ == '__main__':
    app.run(host="0.0.0.0")
