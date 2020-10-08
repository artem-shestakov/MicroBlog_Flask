from flask_restful import fields

users_fields = {
    'id': fields.Integer(),
    'email': fields.String(),
    'f_name': fields.String(),
    'l_name': fields.String(),
    'avatar': fields.String()
}