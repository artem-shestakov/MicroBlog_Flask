from flask import session, flash, redirect, url_for, g
from flask_openid import OpenIDResponse
from flask_login import login_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib import facebook, github
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


@oauth_authorized.connect
def logged_in(blueprint, token):
    if blueprint.name == "twitter":
        username = session.get("twitter_oauth_token").get("screen_name")
    elif blueprint.name == "facebook":
        resp = facebook.get("/me")
        username = resp.json()["name"]
    elif blueprint.name == "github":
        resp = github.get("/user")
        print(">>>>>>>>>>>", resp)
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