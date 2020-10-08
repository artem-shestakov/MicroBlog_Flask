from flask import current_app, abort, send_from_directory
from flask_restful import Resource, marshal_with
from werkzeug.utils import secure_filename
from webapp.utils.response import response_with
import webapp.utils.response_code as response_code
from webapp import db
import os
from .parser import avatar_post_parser
from .fields import users_fields
from webapp.auth.models import User


class AvatarApi(Resource):
    def get(self, user_id):
        """
        Get user's avatar

        :param user_id: user ID
        """
        user = User.query.get(user_id)
        if user.avatar:
            return send_from_directory(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}",
                                       user.avatar)
        else:
            abort(response_with(response_code.NOT_FOUND_404,
                                message='Image not found'))

    @marshal_with(users_fields)
    def post(self, user_id):
        """
        Upload image for user's avatar

        :param user_id: user ID
        """
        args = avatar_post_parser.parse_args()
        file = args['image']
        user = User.query.get(user_id)
        if file:
            filename = secure_filename(file.filename)
            filename = str(user.id) + os.path.splitext(filename)[1]
            user.avatar = filename
            print(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}{filename}")
            file.save(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}{filename}")
            db.session.add(user)
            db.session.commit()
            return user
        else:
            abort(response_with(response_code.INVALID_INPUT_422,
                                message='Image param empty or file has not supported format'))
