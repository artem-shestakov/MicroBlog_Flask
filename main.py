from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.views import View
from sqlalchemy import func, text
from config import DevConfig
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

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

    # def __init__(self, username):
    #     self.username = username

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


# Base class-view for view DB tables
class TableView(View):
    def __init__(self, model, template='home.html'):
        self.model = model
        self.template = template
        self.columns = self.model.__mapper__.columns.keys()
        super(TableView, self).__init__()

    def render_template(self, context):
        return render_template(self.template, **context)

    def get_object(self):
        return self.model.query.all()

    def dispatch_request(self):
        context = {
            "objects": self.get_object(),
            "columns": self.columns
        }
        return self.render_template(context)


# Forms
# Comment Form
class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255, message="")])
    text = TextAreaField(u'Comment', validators=[DataRequired(message="This fild can't be empty")])


# Functions
def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label("total")).join(tags).group_by(Tag).order_by(text('total DESC')).limit(5).all()
    return recent, top_tags


# Root route
@app.route("/")
@app.route("/<int:page>")
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10, False)
    recent, top_tags = sidebar_data()
    return render_template("home.html", posts=posts, recent=recent, top_tags=top_tags)


# Route to post with ID post_id
@app.route("/post/<int:post_id>", methods=("GET", "POST"))
def get_post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        try:
            db.session.add(new_comment)
            db.session.commit()
        except Exception as err:
            print(f"Error adding comment {err}")
            db.session.rollback()
        else:
            print("Comment added")
        return redirect(url_for("get_post", post_id=post_id))

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template("post.html", form=form, post=post, tags=tags, comments=comments, recent=recent,
                           top_tags=top_tags)


# Show posts by users
@app.route("/posts_by_user/<string:username>")
def post_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template("user.html", user=user, posts=posts, recent=recent, top_tags=top_tags)


@app.route("/posts_by_tag/<string:tag_title>")
def posts_by_tag(tag_title):
    tag = Tag.query.filter_by(title=tag_title).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template("tag.html", tag=tag, posts=posts, recent=recent, top_tags=top_tags)


@app.route("/posts_by_users/<string:username>")
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template("user.html", user=user, posts=posts, recent=recent, top_tags=top_tags)


app.add_url_rule(
    "/admin/users", view_func=TableView.as_view("admin_users", model=User, template="table.html")
)
app.add_url_rule(
    "/admin/tags", view_func=TableView.as_view("admin_tags", model=Tag, template="table.html")
)
app.add_url_rule(
    "/admin/comments", view_func=TableView.as_view("admin_comments", model=Comment, template="table.html")
)


@app.errorhandler(404)
def page_404(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0")
