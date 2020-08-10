from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app, abort
from pymysql import OperationalError
from .fields import HTMLField
from .parser import post_get_parser, post_post_parser
from wedapp.posts.models import Post, Tag
from wedapp.auth.models import User
from wedapp import db

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


# Add tags to post by through API request
def add_tags_to_post(post, tags):
    for item in tags:
        try:
            tag = Tag.query.filter_by(title=item).first()
            if tag:
                post.tags.append(tag)
            else:
                tag = Tag(title=item)
                post.tags.append(tag)
        except OperationalError as err:
            current_app.logger.error(f"Database error {err}")
        except Exception as err:
            current_app.logger.error(f"Database error {err}")


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
                posts = user.posts.order_by(Post.publish_date.desc()).\
                    paginate(page, current_app.config.get("POSTS_PER_PAGE", 10))
            # Else get all post
            else:
                posts = Post.query.order_by(Post.publish_date.desc()).\
                    paginate(page, current_app.config.get("POSTS_PER_PAGE", 10))
            return posts.items

    @jwt_required
    def post(self, post_id=None):
        args = post_post_parser.parse_args(strict=True)
        new_post = Post(title=args["title"])
        new_post.user_id = get_jwt_identity()
        new_post.text = args["text"]
        if args["tags"]:
            add_tags_to_post(new_post, args["tags"])
        try:
            db.session.add(new_post)
            db.session.commit()
            return {'id': new_post.id}, 201
        except OperationalError as err:
            current_app.logger.info(f"Database error {err}")
        except Exception as err:
            current_app.logger.info(f"Database error {err}")
