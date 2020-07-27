from flask import Blueprint, redirect, render_template, url_for
from .forms import RegistrationForm
from .models import User
from wedapp import db

auth_blueprint = Blueprint(
    "auth",
    __name__,
    template_folder="../templates/auth",
    url_prefix="/auth"
)


@auth_blueprint.route("/login")
def login():
    return "Login"


@auth_blueprint.route("/registration", methods=("GET", "POST"))
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for(".login"))
    return render_template("registration.html", form=form)
