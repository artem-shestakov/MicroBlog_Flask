from flask import flash, current_app, abort
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import User
import sqlalchemy
from flask_babel import lazy_gettext as _l
from flask_babel import gettext as _


class OpenIDForm(FlaskForm):
    """
    OpenID form.
    """
    openid = StringField(_l("OpenID"), validators=[DataRequired(), URL()])


class LoginForm(FlaskForm):
    """
    Form for login user
    """
    email = StringField(_l("E-mail"), validators=[DataRequired(), Length(max=255)])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember me"))

    # Override standard method of FlaskForm class
    def validate(self):
        # Getting result from standart method of FlaskForm class
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        # Additional check user login and password
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append(_("Invalid email or password"))
            return False

        if not user.check_password(self.password.data):
            self.email.errors.append(_("Invalid email or password"))
            return False

        return True


class RegistrationForm(FlaskForm):
    """
    Form for registration
    """
    email = EmailField(_l("E-Mail"), validators=[DataRequired(), Length(max=255)])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(_l("Confirm password"), validators=[DataRequired(), EqualTo("password")])
    f_name = StringField(_l("First name"), validators=[DataRequired(), Length(max=255)])
    l_name = StringField(_l("Last name"), validators=[Length(max=255)])
    # recaptcha = RecaptchaField()

    # Override standart method of FlaskForm class
    def validate(self):
        # Getting result from standard method of FlaskForm class
        check_validate = super(RegistrationForm, self).validate()
        if not check_validate:
            return False
        try:
            user = User.query.filter_by(email=self.email.data).first()
        except sqlalchemy.exc.OperationalError as err:
            flash(_l("Something went wrong, try later"), category="danger")
            if err.orig.args[0] == 1045:
                current_app.logger.error(err)
            elif err.orig.args[0] == 2003:
                current_app.logger.error(err)
            raise abort(500)

        # Additional check if user login in database
        if user:
            self.email.errors.append(_("User with this email already exists"))
            return False
        return True


class ProfileForm(FlaskForm):
    """Form of user's profile"""
    email = EmailField(_l("E-Mail"), validators=[DataRequired(), Length(max=255)])
    f_name = StringField(_l("First name"), validators=[DataRequired(), Length(max=255)])
    l_name = StringField(_l("Last name"), validators=[Length(max=255)])
    about = TextAreaField(_l("About"), validators=[Length(max=1000)])


class ForgotPass(FlaskForm):
    """
    Form for sending token to reset password
    """
    email = EmailField(_l("E-Mail"), validators=[DataRequired(), Length(max=255)])
    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(ForgotPass, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append(_("User with this email is not registered"))
            return False
        return True


class ResetPassword(FlaskForm):
    """
    Reset password form
    """
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(_l("Confirm password"), validators=[DataRequired(), EqualTo("password")])
    # recaptcha = RecaptchaField()