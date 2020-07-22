import os
from dotenv import load_dotenv

load_dotenv()
mysql_pass = os.getenv("MYSQL_ROOT_PASSWORD")


class Config(object):
    POSTS_PER_PAGE = 10


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{mysql_pass}@127.0.0.1:3306/web_blog"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'\xe5LpK!\xa4\x99\x92G\xd1T\x82\xdfR\x0c\xb6\x95\xbd\x1c\xab\x19\x94\xc87'
