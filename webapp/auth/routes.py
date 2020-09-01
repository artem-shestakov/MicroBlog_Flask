from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from .forms import RegistrationForm, LoginForm, OpenIDForm, ForgotPass, ResetPassword
from . import openid, authenticate, check_confirmed
from .models import User
from .tasks import send_confirm_email, send_pass_reset_email
from .utils import confirm_token, confirm_reset_pass_token
from webapp import db
from flask_babel import gettext
from datetime import datetime
from flask_babel import gettext as _

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
#@openid.loginhandler
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


# URL for email confirmation
@auth_blueprint.route("/email-confirm/<token>")
def email_confirm(token):
    try:
        email = confirm_token(token)
        if email is False:
            flash("The confirm link invalid", category="danger")
            return redirect(url_for("main.home", page=1))
    except:
        flash("The confirm link invalid", category="danger")
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirm:
        flash("Account already confirmed!", category="success")
    else:
        user.email_confirm = True
        user.email_confirm_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account!", category="success")
    return redirect(url_for("main.home", page=1))


@auth_blueprint.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.email_confirm:
        return redirect(url_for("main.home", page=1))
    flash(_("Please confirm your email"), category="danger")
    return render_template("unconfirmed.html")


@auth_blueprint.route("/resend_email", methods=["POST"])
@login_required
def resend_email():
    email = current_user.email
    send_confirm_email(email)
    flash(_("Confirmation email has been send"), category="info")
    return redirect(url_for("main.home", page=1))


@auth_blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot_pass():
    form = ForgotPass()
    if form.validate_on_submit():
        email = form.email.data
        send_pass_reset_email(email)
        flash(_("We send you email to reset your password"), category="info")
        redirect(".login")
        return redirect(url_for(".login"))
    return render_template("forgot_pass.html", form=form)


@auth_blueprint.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = confirm_reset_pass_token(token)
        if email is False:
            flash("The confirm link invalid", category="danger")
            return redirect(url_for("main.home", page=1))
    except:
        flash("The confirm link invalid", category="danger")
    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email["email"]).first()
        if user:
            new_password = form.password.data
            user.set_password(new_password)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for(".login"))
    return render_template("reset_pass.html", token=token, form=form)


@auth_blueprint.route("/profile")
@login_required
@check_confirmed
def user_profile():
    return render_template("profile.html", user=current_user, title=_("User profile"))


# JWT token route
@auth_blueprint.route("/api", methods=["POST"])
def api():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email:
        return jsonify({"msg": "Missing <email> parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing <password> parameter"}), 400
    user = authenticate(email=email, password=password)
    if not user:
        return jsonify({"msg": "Bad password or username"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
