from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
from flask import current_app


def generate_confirm_token(email):
    """
    Generate token from email and salt
    """
    serializer = URLSafeTimedSerializer(secret_key=current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SALT_SECRET"])


def confirm_token(token):
    """
    Getting email by encoding token.
    """
    serializer = URLSafeTimedSerializer(secret_key=current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config["SALT_SECRET"],
            max_age=3600
        )
    except Exception as err:
        print(err)
        return False
    return email


def generate_reset_pass_token(email):
    """Generate token for password reset URL by email"""

    serializer = TimedJSONWebSignatureSerializer(secret_key=current_app.config["SECRET_KEY"],
                                                 expires_in=1800)
    return serializer.dumps({"email": email}).decode("utf-8")


def verify_reset_pass_token(token):
    """Getting email by encoding token to reset password"""
    serializer = TimedJSONWebSignatureSerializer(secret_key=current_app.config["SECRET_KEY"],
                                                 expires_in=1800)
    try:
        email = serializer.loads(token)
    except Exception as err:
        print(err)
        return False
    return email
