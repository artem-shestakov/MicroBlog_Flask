from flask import Blueprint, current_app, render_template, abort
import sqlalchemy
from webapp.posts.models import Post
from .utils import sidebar_data
from webapp import cache

# Blueprint for main module
main_blueprint = Blueprint(
    "main",
    __name__,
    template_folder="../templates/main",
)


# Base 404 handler
@main_blueprint.app_errorhandler(404)
def page_not_found(error):
    """ Return error 404 html page"""
    return render_template("404.html", title="Page Not Found"), 404


# 500 error handler
@main_blueprint.app_errorhandler(500)
def page_not_found(error):
    """ Return error 500 html page"""
    return render_template("500.html", title="Error 500"), 500


# Route to index page or page with number "page", by default 1
@main_blueprint.route("/")
@main_blueprint.route("/<int:page>")
@cache.cached(timeout=60)
def home(page=1):
    try:
        posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, current_app.config.get("POSTS_PER_PAGE", 10),
                                                                       False)
        recent, top_tags = sidebar_data()
        return render_template('home.html', posts=posts, recent=recent, top_tags=top_tags, title="Web blog - Home page")
    except sqlalchemy.exc.OperationalError as err:
        if err.orig.args[0] == 1045:
            print("Access Denied")
        elif err.orig.args[0] == 2003:
            print("Connection Refused")
        raise abort(500)
