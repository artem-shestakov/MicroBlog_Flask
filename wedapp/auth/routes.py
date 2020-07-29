from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm
from .models import User
from wedapp import db

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
def login():
    form = LoginForm()
    # If get POST request from form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember_me.data)
        flash("You have been logged successfully", category="success")
        return redirect(url_for("main.home", page=1))
    return render_template("login.html", form=form)


# Logout user and redirect to index page
@auth_blueprint.route("/logout", methods=("GET", "POST"))
@login_required
def logout():
    logout_user()
    flash("You have been logged out", category="success")
    return redirect(url_for("main.home", page=1))


# Registration page
@auth_blueprint.route("/registration", methods=("GET", "POST"))
def registration():
    form = RegistrationForm()
    # If POST request from form
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as err:
            flash("Something went wrong, try later")
            redirect(url_for("main.home", page=1))
        return redirect(url_for(".login"))
    return render_template("registration.html", form=form)
