from flask_login import LoginManager, AnonymousUserMixin
from flask_bcrypt import Bcrypt

# Create LoginManager object
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

# Create Bcrypt object for hashing user's passwords
bcrypt = Bcrypt()


# Reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


# Init objects and register blueprint
def create_module(app, **kwargs):
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
