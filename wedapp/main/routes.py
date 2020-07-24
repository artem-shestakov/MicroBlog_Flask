from flask import Blueprint, current_app, render_template
from wedapp.posts.model import Post
from .utils import sidebar_data

# Blueprint for main module
main_blueprint = Blueprint(
    "main",
    __name__,
    template_folder="../templates/main",
)


# Route to root
@main_blueprint.route("/")
@main_blueprint.route("/<int:page>")
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, current_app.config.get("POSTS_PER_PAGE", 10), False)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )