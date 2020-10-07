from flask_restful import reqparse
import werkzeug

avatar_post_parser = reqparse.RequestParser()
avatar_post_parser.add_argument('image',
                                type=werkzeug.datastructures.FileStorage,
                                required=True,
                                location='files',
                                help='Use this parameter to upload avatar image')
