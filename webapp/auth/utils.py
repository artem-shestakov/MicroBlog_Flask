from itsdangerous import URLSafeSerializer
from flask import current_app


def generate_confirm_token(email):
    """
    Generate token from email and salt
    """
    serializer = URLSafeSerializer(secret_key=current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SALT_SECRET"])


def confirm_token(token):
    """
    Getting email by encoding token.
    """
    serializer = URLSafeSerializer(secret_key=current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config["SALT_SECRET"]
        )
    except Exception as err:
        print(err)
        return False
    return email
