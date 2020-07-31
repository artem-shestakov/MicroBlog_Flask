from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import User


class OpenIDForm(FlaskForm):
    """
    OpenID form.
    """
    openid = StringField("OpenID", validators=[DataRequired(), URL()])


class LoginForm(FlaskForm):
    """
    Form for login user
    """
    username = StringField("Username", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")

    # Override standart method of FlaskForm class
    def validate(self):
        # Getting result from standart method of FlaskForm class
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        # Additional check user login and password
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("Invalid username or password")
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append("Invalid username or password")
            return False

        return True


class RegistrationForm(FlaskForm):
    """
    Form for registration
    """
    username = StringField("Username", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    recaptcha = RecaptchaField()

    # Override standart method of FlaskForm class
    def validate(self):
        # Getting result from standart method of FlaskForm class
        check_validate = super(RegistrationForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        # Additional check if user login in database
        if user:
            self.username.errors.append("User with this name already exists")
            return False

        return True
