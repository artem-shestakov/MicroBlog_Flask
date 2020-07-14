import os
from dotenv import load_dotenv

load_dotenv()
mysql_pass = os.getenv("MYSQL_ROOT_PASSWORD")


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{mysql_pass}@127.0.0.1:3306/web_blog"
    SQLALCHEMY_ECHO = True
