from flask import Blueprint, render_template, flash, redirect, url_for, abort, request, get_flashed_messages, session
from flask_login import login_required, current_user
from datetime import datetime
from webapp.main.utils import sidebar_data, cache
from .models import Post, Tag, Comment, db
from webapp.auth.models import User
from webapp.auth import has_role
from .forms import CommentForm, PostForm

# Blueprint for posts
posts_blueprint = Blueprint(
    "posts",
    __name__,
    template_folder="../templates/posts",
    url_prefix="/post",
    static_folder="../static"
)


def make_chache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    message = str(hash(frozenset(get_flashed_messages())))
    if current_user.is_authenticated:
        roles = str(current_user.roles)
    else:
        roles = ""
    return str((path + args + roles + session.get("locale", "") + message).encode("utf-8"))


@posts_blueprint.app_errorhandler(404)
def page_not_found(error):
    """ Return error 404 """
    return render_template('404.html'), 404


@posts_blueprint.app_errorhandler(403)
def page_not_found(error):
    """ Return error 404 """
    return render_template('403.html'), 403


@posts_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
@cache.cached(timeout=60, key_prefix=make_chache_key)
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
        except Exception as e:
            flash('Error adding your comment: %s' % str(e), 'error')
            db.session.rollback()
        else:
            flash('Comment added', 'info')
        return redirect(url_for('posts.get_post', post_id=post_id))

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html', post=post, tags=tags, comments=comments, recent=recent, top_tags=top_tags,
                           form=form)


@posts_blueprint.route("/new", methods=("GET", "POST"))
@login_required
@has_role("author")
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post()
        new_post.title = form.title.data
        new_post.text = form.text.data
        new_post.user_id = current_user.id
        db.session.add(new_post)
        db.session.commit()
        flash("New post added", category="info")
        return redirect(url_for(".get_post", post_id=new_post.id))
    return render_template("new.html", form=form)


@posts_blueprint.route("/edit/<int:post_id>", methods=("GET", "POST"))
@login_required
@has_role("author")
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.now()
            db.session.merge(post)
            db.session.commit()
            return redirect(url_for(".get_post", post_id=post.id))
        form.title.data = post.title
        form.text.data = post.text
        return render_template("edit.html", form=form, post=post)
    abort(403)


@posts_blueprint.route('/tag/<string:tag_title>')
@cache.cached(timeout=60, key_prefix=make_chache_key)
def posts_by_tag(tag_title):
    tag = Tag.query.filter_by(title=tag_title).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@posts_blueprint.route('/user/<string:username>')
@cache.cached(timeout=60, key_prefix=make_chache_key)
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
