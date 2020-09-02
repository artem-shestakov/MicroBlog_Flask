from flask_login import LoginManager, AnonymousUserMixin, login_user, current_user
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.gitlab import make_gitlab_blueprint, gitlab
from flask_dance.consumer import oauth_authorized
from flask_openid import OpenIDResponse
from flask import session, g, flash, redirect, url_for, abort, current_app
from webapp import db
from flask_jwt_extended import JWTManager
from functools import update_wrapper, wraps
from pymysql import OperationalError
from flask_babel import gettext as _
from sqlalchemy import event
from .tasks import greeting_sender


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

# Create JSON web token object
jwt = JWTManager()


# Reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(user_id)


# Init objects and register blueprint
def create_module(app, **kwargs):
    from .models import User
    login_manager.init_app(app)
    bcrypt.init_app(app)
    openid.init_app(app)
    jwt.init_app(app)

    facebook_blueprint = make_facebook_blueprint(
        client_id=app.config.get("FACEBOOK_CLIENT_ID"),
        client_secret=app.config.get("FACEBOOK_CLIENT_SECRET"),
        scope=["email"]
    )

    github_blueprint = make_github_blueprint(
        client_id=app.config.get("GITHUB_CLIENT_ID"),
        client_secret=app.config.get("GITHUB_CLIENT_SECRET"),
        scope=["user:email"]
    )

    gitlab_blueprint = make_gitlab_blueprint(
        client_id=app.config.get("GITLAB_CLIENT_ID"),
        client_secret=app.config.get("GITLAB_CLIENT_SECRET"),
        scope=["read_user email"]
    )
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(facebook_blueprint, url_prefix="/auth/login")
    app.register_blueprint(github_blueprint, url_prefix="/auth/login")
    app.register_blueprint(gitlab_blueprint, url_prefix="/auth/login")

    event.listen(User, "after_insert", greeting_sender)


def has_role(roles):
    """Decorator function for checkin user's role"""
    def decorator_func(f):
        def wrapper_func(*args, **kwargs):
            for role in roles:
                if current_user.has_role(role):
                    return f(*args, **kwargs)
            abort(403)
        return update_wrapper(wrapper_func, f)
    return decorator_func


def check_confirmed(f):
    """Decorator for checking user's email confirmation"""
    @wraps(f)
    def wrapper_func(*args, **kwargs):
        if current_user.email_confirm is False:
            return redirect(url_for("auth.unconfirmed"))
        return f(*args, **kwargs)
    return wrapper_func


def authenticate(email, password):
    """Check user and password before return JWT"""
    from .models import User
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user
    except OperationalError as err:
        current_app.logger.error(f"Database error {err}")
    except Exception as err:
        current_app.logger.error(f"Database error {err}")


# Handler run after response from OpenID provider
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


# Handler run after response from OAuth provider
@oauth_authorized.connect
def logged_in(blueprint, token):
    from .models import User
    if blueprint.name == "facebook":
        resp = facebook.get("/me?fields=name,first_name,email")
        email = resp.json()["email"]
        f_name = resp.json()["first_name"]
        account_type = "facebook"
    elif blueprint.name == "github":
        user_info = github.get("/user")
        user_email = github.get("/user/emails")
        email = user_email.json()[0]["email"]
        f_name = user_info.json()["name"]
        account_type = "github"
    elif blueprint.name == "gitlab":
        resp = gitlab.get("user")
        email = resp.json()["email"]
        f_name = resp.json()["name"].split()[0]
        account_type = "gitlab"
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, f_name=f_name, account_type=account_type)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
    login_user(user)
    g.user = user
    flash(_("You have been logged in."), category="success")
