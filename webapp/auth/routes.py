from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from .forms import RegistrationForm, LoginForm, OpenIDForm
from . import openid, authenticate
from .models import User
from webapp import db
from flask_babel import gettext

# Init Blueprint
auth_blueprint = Blueprint(
    "auth",
    __name__,
    template_folder="../templates/auth",
    url_prefix="/auth"
)


# Base 404 handler
@auth_blueprint.app_errorhandler(404)
def page_not_found(error):
    """ Return error 404 """
    return render_template('404.html'), 404


# Route to login form
@auth_blueprint.route("/login", methods=('GET', "POST"))
@openid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIDForm()
    # Validate data from OpenID
    if openid_form.validate_on_submit():
        return openid.try_login(openid_form.openid.data,
                                ask_for=["nickname", "email"],
                                ask_for_optional=["fullname"])

    # If get POST request from form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user, remember=form.remember_me.data)
        flash("You have been logged successfully", category="success")
        return redirect(url_for("main.home", page=1))

    # Check OpenID errors
    openid_errors = openid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")
    return render_template("login.html", form=form, openid_form=openid_form)


# Logout user and redirect to index page
@auth_blueprint.route("/logout", methods=("GET", "POST"))
@login_required
def logout():
    logout_user()
    flash("You have been logged out", category="success")
    return redirect(url_for("main.home", page=1))


# Registration page
@auth_blueprint.route("/registration", methods=("GET", "POST"))
@openid.loginhandler
def registration():
    form = RegistrationForm()
    openid_form = OpenIDForm()
    # Validate data from OpenID
    if openid_form.validate_on_submit():
        return openid.try_login(openid_form.openid.data,
                                ask_for=["username", "email"],
                                ask_for_optional=["fullname"])

    # If POST request from form
    if form.validate_on_submit():
        new_user = User(email=form.email.data, f_name=form.f_name.data)
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as err:
            flash(gettext("Something went wrong, try later"), category="danger")
            redirect(url_for("main.home", page=1))
        return redirect(url_for(".login"))
    openid_errors = openid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")
    return render_template("registration.html", form=form)


# JWT token route
@auth_blueprint.route("/api", methods=["POST"])
def api():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"msg": "Missing <username> parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing <password> parameter"})
    user = authenticate(username=username, password=password)
    if not user:
        return jsonify({"msg": "Bad password or username"})
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
