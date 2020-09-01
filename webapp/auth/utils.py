from itsdangerous import URLSafeTimedSerializer
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
