from flask import Blueprint, redirect, render_template, url_for, flash, request, jsonify, abort, current_app
import sqlalchemy
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from .forms import RegistrationForm, LoginForm, OpenIDForm, ForgotPass, ResetPassword
from . import authenticate, check_confirmed
from .models import User
from .tasks import send_confirm_email, send_pass_reset_email
from .utils import confirm_token, verify_reset_pass_token
from webapp import db
from flask_babel import gettext
from datetime import datetime
from flask_babel import gettext as _


def find_user(**kwargs):
    """Find user by arguments"""
    try:
        user = User.query.filter_by(**kwargs).first_or_404()
        return user
    except sqlalchemy.exc.OperationalError as err:
        flash(gettext("Something went wrong, try later"), category="danger")
        if err.orig.args[0] == 1045:
            current_app.logger.error(err)
        elif err.orig.args[0] == 2003:
            current_app.logger.error(err)
        raise abort(500)


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


# Base 500 handler
@auth_blueprint.app_errorhandler(500)
def app_error(error):
    """ Return error 500 """
    return render_template('500.html'), 500


# Route to login form
@auth_blueprint.route("/login", methods=('GET', "POST"))
def login():
    """Login user function"""
    form = LoginForm()
    # If get POST request from form
    if form.validate_on_submit():
        user = find_user(email=form.email.data)
        login_user(user, remember=form.remember_me.data)
        flash("You have been logged successfully", category="success")
        return redirect(url_for("main.home", page=1))
    return render_template("login.html", form=form)


# Logout user and redirect to index page
@auth_blueprint.route("/logout", methods=("GET", "POST"))
@login_required
def logout():
    """Logout user function"""
    logout_user()
    flash("You have been logged out", category="success")
    return redirect(url_for("main.home", page=1))


# Registration page
@auth_blueprint.route("/registration", methods=("GET", "POST"))
def registration():
    """Render registration form and user registration"""
    form = RegistrationForm()
    # If POST request from form
    if form.validate_on_submit():
        new_user = User(email=form.email.data, f_name=form.f_name.data)
        new_user.set_password(form.password.data)
        new_user.l_name = form.l_name.data
        try:
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.OperationalError as err:
            flash(gettext("Something went wrong, try later"), category="danger")
            if err.orig.args[0] == 1045:
                current_app.logger.error(err)
            elif err.orig.args[0] == 2003:
                current_app.logger.error(err)
            raise abort(500)
        except Exception as err:
            print(">>>>>", err)
            raise abort(500)
        return redirect(url_for(".login"))
    return render_template("registration.html", form=form)


# URL for email confirmation
@auth_blueprint.route("/email-confirm/<token>")
def email_confirm(token):
    """Confirmation user's email by token"""
    try:
        email = confirm_token(token)
        if email is False:
            flash("The confirm link invalid", category="danger")
            return redirect(url_for("main.home", page=1))
    except:
        flash("The confirm link invalid", category="danger")
    user = find_user(email=email)
    if user.email_confirm:
        flash("Account already confirmed!", category="success")
    else:
        user.email_confirm = True
        user.email_confirm_on = datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
            flash("You have confirmed your account!", category="success")
        except sqlalchemy.exc.OperationalError as err:
            flash(gettext("Something went wrong, try later"), category="danger")
            if err.orig.args[0] == 1045:
                current_app.logger.error(err)
            elif err.orig.args[0] == 2003:
                current_app.logger.error(err)
            raise abort(500)
    return redirect(url_for("main.home", page=1))


@auth_blueprint.route("/unconfirmed")
@login_required
def unconfirmed():
    """If user confirm redirect to index oage, else render unconfirmed page"""
    if current_user.email_confirm:
        return redirect(url_for("main.home", page=1))
    flash(_("Please confirm your email"), category="danger")
    return render_template("unconfirmed.html")


@auth_blueprint.route("/resend_email", methods=["POST"])
@login_required
def resend_email():
    """Re-send email confirmation to user"""
    email = current_user.email
    send_confirm_email(email)
    flash(_("Confirmation email has been send"), category="info")
    return redirect(url_for("main.home", page=1))


@auth_blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot_pass():
    """Form for users who forgot password"""
    form = ForgotPass()
    if form.validate_on_submit():
        email = form.email.data
        send_pass_reset_email(email)
        flash(_("We send you email to reset your password"), category="info")
        redirect("main.home")
        return redirect(url_for(".login"))
    return render_template("forgot_pass.html", form=form)


@auth_blueprint.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Reset password by user's token"""
    try:
        email = verify_reset_pass_token(token)["email"]
        if email is False:
            flash("The confirm link invalid", category="danger")
            return redirect(url_for("main.home", page=1))
    except:
        flash("The confirm link invalid", category="danger")
        return redirect(url_for("main.home", page=1))
    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            new_password = form.password.data
            user.set_password(new_password)
            try:
                db.session.add(user)
                db.session.commit()
            except sqlalchemy.exc.OperationalError as err:
                flash(gettext("Something went wrong, try later"), category="danger")
                if err.orig.args[0] == 1045:
                    current_app.logger.error(err)
                elif err.orig.args[0] == 2003:
                    current_app.logger.error(err)
                raise abort(500)
        return redirect(url_for(".login"))
    return render_template("reset_pass.html", token=token, form=form)


@auth_blueprint.route("/profile")
@login_required
@check_confirmed
def user_profile():
    """User's profile page"""
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
