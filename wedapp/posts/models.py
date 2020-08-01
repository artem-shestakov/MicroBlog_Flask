from .. import db
from datetime import datetime


# Association tables many-to-many
# Posts-to-Tags
tags = db.Table("post_tag",
                db.Column("post_id", db.Integer(), db.ForeignKey("posts.id")),
                db.Column("tag_id", db.Integer(), db.ForeignKey("tags.id"))
                )


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

    # def __init__(self, title):
    #     self.title = title

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

    # def __init__(self, title):
    #     self.title = title

    def __repr__(self):
        return f"<Tag '{self.title}'>"
