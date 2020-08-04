from flask_login import LoginManager, AnonymousUserMixin, login_user
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized
from flask_openid import OpenIDResponse
from flask import session, g, flash, redirect, url_for
from wedapp import db


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

    github_blueprint = make_github_blueprint(
        client_id=app.config.get("GITHUB_CLIENT_ID"),
        client_secret=app.config.get("GITHUB_CLIENT_SECRET")
    )
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(twitter_blueprint, url_prefix="/auth/login")
    app.register_blueprint(facebook_blueprint, url_prefix="/auth/login")
    app.register_blueprint(github_blueprint, url_prefix="/auth/login")


@openid.after_login
def create_or_login(resp: OpenIDResponse):
    from .models import User
    session['openid'] = resp.identity_url
    username = resp.nickname or resp.email or resp.fullname
    # Check data from OpenID provider
    if not username:
        flash("Invalid login. Please try again.", category="danger")
        redirect(url_for(".login"))
    user = User.query.filter_by(username=username).first()
    # If user does not exist
    if user is None:
        user = User(username=username)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            print(err)
    login_user(user)
    g.user = user
    flash("You have been logged in.", category="success")
    return redirect(openid.get_next_url())


@oauth_authorized.connect
def logged_in(blueprint, token):
    from .models import User
    if blueprint.name == "twitter":
        username = session.get("twitter_oauth_token").get("screen_name")
    elif blueprint.name == "facebook":
        resp = facebook.get("/me")
        username = resp.json()["name"]
    elif blueprint.name == "github":
        resp = github.get("/user")
        print(">>>>>>>>>>>", resp.json())
        username = resp.json()["login"]
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            print(err)
    login_user(user)
    g.user = user
    flash("You have been logged in.", category="success")
