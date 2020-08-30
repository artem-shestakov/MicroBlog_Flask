from webapp import db, cache
from flask_login import AnonymousUserMixin
from . import bcrypt


class BlogAnonymus(AnonymousUserMixin):
    def __init__(self):
        self.email = "Guest"


roles = db.Table(
    "role_user",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("user_roles.id"))
)


# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    f_name = db.Column(db.String(255), nullable=False)
    l_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    about = db.Column(db.Text())
    account_type = db.Column(db.String(25), nullable=False, default="local")
    email_confirm = db.Column(db.Boolean(), nullable=False, default=False)
    email_confirm_on = db.Column(db.DateTime())
    posts = db.relationship("Post", backref="users", lazy="dynamic")
    roles = db.relationship("Role", secondary=roles, backref=db.backref("users", lazy="dynamic"))

    def __init__(self, email, f_name):
        default_role = Role.query.filter_by(name="user").one()
        self.roles.append(default_role)
        self.email = email
        self.f_name = f_name

    # Check user's role
    @cache.memoize(timeout=60)
    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False

    # Block standard methods of Flask Login module
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
        return f"<User '{self.email}'>"


# Class for user's role
class Role(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Role '{self.name}'>"
