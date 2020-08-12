from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app, abort
from pymysql import OperationalError
from .fields import HTMLField
from .parser import post_get_parser, post_post_parser, post_put_parser
from wedapp.posts.models import Post, Tag, Comment
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

comment_field = {
    "id": fields.Integer(),
    "name": fields.String(),
    "text": fields.String(),
    "date": fields.DateTime(dt_format="iso8601")
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


# API request handler function for posts
class PostApi(Resource):
    @marshal_with(post_fields)
    @jwt_required
    # GET information from post
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            return post
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
    # Create post
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

    @jwt_required
    # Update post
    def put(self, post_id=None):
        if not post_id:
            abort(400)
        try:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            args = post_put_parser.parse_args()
            if  get_jwt_identity() != post.user_id:
                abort(403)
            if args["title"]:
                post.title = args["title"]
            if args["text"]:
                post.text = args["text"]
            if args["tags"]:
                add_tags_to_post(post, args["tags"])
            db.session.merge(post)
            db.session.commit()
            return {"id": post_id}, 201
        except OperationalError as err:
            current_app.logger.info(f"Database error {err}")
        except Exception as err:
            current_app.logger.info(f"Database error {err}")

    @jwt_required
    # Delete post
    def delete(self, post_id=None):
        if not post_id:
            abort(400)
        try:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            if get_jwt_identity() != post.user_id:
                abort(403)
            db.session.delete(post)
            db.session.commit()
            return "", 204
        except OperationalError as err:
            current_app.logger.info(f"Database error {err}")
        except Exception as err:
            current_app.logger.info(f"Database error {err}")


# API request handler function for comments in posts
class CommentPostApi(Resource):
    @marshal_with(comment_field)
    @jwt_required
    # Get all comments by post ID
    def get(self, post_id=None):
        if not post_id:
            abort(400)
        try:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            comments = post.comments.all()
            return comments
        except OperationalError as err:
            current_app.logger.info(f"Database error {err}")
        except Exception as err:
            current_app.logger.info(f"Database error {err}")


# Comments API
class CommentsApi(Resource):
    @jwt_required
    # Delete comment by ID
    def delete(self, comment_id=None):
        if not comment_id:
            abort(400)
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                abort(404)
            user = User.query.filter_by(username="admin").one()
            if get_jwt_identity() != user.id:
                abort(403)
            db.session.delete(comment)
            db.session.commit()
            return "", 204
        except OperationalError as err:
            current_app.logger.info(f"Database error {err}")
        except Exception as err:
            current_app.logger.info(f"Database error {err}")
