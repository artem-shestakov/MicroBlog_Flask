from flask_login import LoginManager, AnonymousUserMixin
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook


# Create LoginManager object
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

# Create Bcrypt object for hashing user's passwords
bcrypt = Bcrypt()

# Create OpenID object
openid = OpenID()


# Reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


# Init objects and register blueprint
def create_module(app, **kwargs):
    login_manager.init_app(app)
    bcrypt.init_app(app)
    openid.init_app(app)

    twitter_blueprint = make_twitter_blueprint(
        api_key=app.config.get("TWITTER_API_KEY"),
        api_secret=app.config.get("TWITTER_API_SECRET")
    )

    facebook_blueprint = make_facebook_blueprint(
        client_id=app.config.get("FACEBOOK_CLIENT_ID"),
        client_secret=app.config.get("FACEBOOK_CLIENT_SECRET")
    )
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(twitter_blueprint, url_prefix="/auth/login")
    app.register_blueprint(facebook_blueprint, url_prefix="/auth/login")

