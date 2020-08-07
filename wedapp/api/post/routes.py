from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required
from flask import current_app, abort
from .fields import HTMLField
from .parser import post_get_parser
from wedapp.posts.models import Post
from wedapp.auth.models import User

# JSON format for tag
tag_fields = {
    "id": fields.Integer(),
    "title": fields.String()
}


def get_author(post):
    user = User.query.filter_by(id=post.user_id)
    return user

# JSON format of post object
post_fields = {
    "id": fields.Integer(),
    "title": fields.String(),
    "text": HTMLField(),
    "publish_date": fields.DateTime(dt_format="iso8601"),
    "author": fields.String(attribute=lambda x: x.users.username),
    "tags": fields.List(fields.Nested(tag_fields))
}
# API request handler function
class PostApi(Resource):
    @marshal_with(post_fields)
    @jwt_required
    # GET request
    def get(self, post_id=None):
        if post_id:
            pass
        else:
            # Getting arguments from request
            args = post_get_parser.parse_args()
            page = args["page"] or 1
            # If user argument in request getting posts by this user
            if args["user"]:
                user = User.query.filter_by(username=args["user"]).first()
                if not user:
                    abort(404)
                posts = user.posts.order_by(Post.publish_date.desc()).paginate(page, current_app.config.get("POSTS_PER_PAGE", 10))
            # Else get all post
            else:
                posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, current_app.config.get("POSTS_PER_PAGE", 10))
            return posts.items
