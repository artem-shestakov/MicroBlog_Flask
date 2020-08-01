import os
from dotenv import load_dotenv

load_dotenv()
mysql_pass = os.getenv("MYSQL_ROOT_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
recaptch_public_key = os.getenv("RECAPTCHA_PUBLIC_KEY")
recaptcha_private_key = os.getenv("RECAPTCHA_PRIVATE_KEY")
tw_api_key = os.getenv("TWITTER_API_KEY")
tw_api_secret = os.getenv("TWITTER_API_SECRET")


class Config(object):
    POSTS_PER_PAGE = 10


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{mysql_pass}@127.0.0.1:3306/{mysql_database}"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'\xe5LpK!\xa4\x99\x92G\xd1T\x82\xdfR\x0c\xb6\x95\xbd\x1c\xab\x19\x94\xc87'
    RECAPTCHA_PUBLIC_KEY = f"{recaptch_public_key}"
    RECAPTCHA_PRIVATE_KEY = f"{recaptcha_private_key}"
    POSTS_PER_PAGE = 10
    TWITTER_API_KEY = f"{tw_api_key}"
    TWITTER_API_SECRET = f"{tw_api_secret}"
