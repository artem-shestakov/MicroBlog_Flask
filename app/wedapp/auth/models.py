from app.wedapp import db
from flask_login import AnonymousUserMixin
from . import bcrypt


class BlogAnonymus(AnonymousUserMixin):
    def __init__(self):
        self.username = "Guest"


# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    # email = db.Column(db.String(255), nullable=False, unique=True)
    posts = db.relationship("Post", backref="users", lazy="dynamic")

    # def __init__(self, username):
    #     self.username = username

    # Block standart methods of Flask Login module
    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)

    # Encrypt user password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    # Check hash from db and from login form
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User '{self.username}'>"
