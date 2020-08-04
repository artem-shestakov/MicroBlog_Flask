from flask import session, flash, redirect, url_for, g
from flask_openid import OpenIDResponse
from flask_login import login_user
from wedapp import db
from .models import User
from . import openid


@openid.after_login
def create_or_login(resp: OpenIDResponse):
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


