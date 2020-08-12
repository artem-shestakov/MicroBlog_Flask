from flask_restful import Api
from .post.routes import PostApi, CommentPostApi, CommentsApi

rest_api = Api()


# Register API module
def create_module(app, **kwargs):
    rest_api.add_resource(
        PostApi,
        "/api/post",
        "/api/post/<int:post_id>"
    )

    rest_api.add_resource(
        CommentPostApi,
        "/api/post/<int:post_id>/comments"
    )

    rest_api.add_resource(
        CommentsApi,
        "/api/comments/<int:comment_id>"
    )

    rest_api.init_app(app)
