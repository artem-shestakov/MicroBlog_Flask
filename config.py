import os
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()
mysql_pass = os.getenv("MYSQL_ROOT_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
recaptch_public_key = os.getenv("RECAPTCHA_PUBLIC_KEY")
recaptcha_private_key = os.getenv("RECAPTCHA_PRIVATE_KEY")
tw_api_key = os.getenv("TWITTER_API_KEY")
tw_api_secret = os.getenv("TWITTER_API_SECRET")
fb_client_id = os.getenv("FACEBOOK_CLIENT_ID")
fb_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")
github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
gitlab_client_id = os.getenv("GITLAB_CLIENT_ID")
gitlab_client_secret = os.getenv("GITLAB_CLIENT_SECRET")
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_user_password = os.getenv("RABBITMQ_DEFAULT_PASS")
smtp_from = os.getenv("SMTP_FROM")
smtp_server = os.getenv("SMTP_SERVER")
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


class Config(object):
    POSTS_PER_PAGE = 10


class ProdConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    ASSETS_DEBUG = False
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_DB = "0"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{mysql_pass}@db:3306/{mysql_database}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = f"amqp://{rabbitmq_user}:{rabbitmq_user_password}@rabbitmq//"
    CELERY_RESULT_BACKEND = f"amqp://{rabbitmq_user}:{rabbitmq_user_password}@rabbitmq//"
    CELERY_IMPORTS = ["webapp.posts.tasks"]
    CELERY_ALWAYS_EAGER = False
    SERVER_NAME = "artem-shestakov.site"
    PREFERRED_URL_SCHEME = "https"
    SECRET_KEY = b'\xe5LpK!\xa4\x99\x92G\xd1T\x82\xdfR\x0c\xb6\x95\xbd\x1c\xab\x19\x94\xc87'
    SMTP_FROM = smtp_from
    SMTP_SERVER = smtp_server
    SMTP_USER = smtp_user
    SMTP_PASS = smtp_pass
    RECAPTCHA_PUBLIC_KEY = f"{recaptch_public_key}"
    RECAPTCHA_PRIVATE_KEY = f"{recaptcha_private_key}"
    PROPAGATE_EXCEPTIONS = True
    OAUTHLIB_RELAX_TOKEN_SCOPE = 1
    TWITTER_API_KEY = f"{tw_api_key}"
    TWITTER_API_SECRET = f"{tw_api_secret}"
    FACEBOOK_CLIENT_ID = f"{fb_client_id}"
    FACEBOOK_CLIENT_SECRET = f"{fb_client_secret}"
    GITHUB_CLIENT_ID = f"{github_client_id}"
    GITHUB_CLIENT_SECRET = f"{github_client_secret}"
    GITLAB_CLIENT_ID = f"{gitlab_client_id}"
    GITLAB_CLIENT_SECRET = f"{gitlab_client_secret}"


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    ASSETS_DEBUG = True
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_DB = "0"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{mysql_pass}@127.0.0.1:3306/{mysql_database}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = f"amqp://{rabbitmq_user}:{rabbitmq_user_password}@127.0.0.1//"
    CELERY_RESULT_BACKEND = f"amqp://{rabbitmq_user}:{rabbitmq_user_password}@127.0.0.1//"
    CELERY_IMPORTS = ["webapp.posts.tasks"]
    CELERY_ALWAYS_EAGER = False
    # CELERYBEAT_SCHEDULE = {
    #     'weekly-digest': {
    #         'task': 'webapp.posts.tasks.remind',
    #         'schedule': crontab(minute="*/1")
    #     },
    # }
    SERVER_NAME = "0.0.0.0"
    PREFERRED_URL_SCHEME = "https"
    SECRET_KEY = b'\xe5LpK!\xa4\x99\x92G\xd1T\x82\xdfR\x0c\xb6\x95\xbd\x1c\xab\x19\x94\xc87'
    SMTP_FROM = smtp_from
    SMTP_SERVER = smtp_server
    SMTP_USER = smtp_user
    SMTP_PASS = smtp_pass
    RECAPTCHA_PUBLIC_KEY = f"{recaptch_public_key}"
    RECAPTCHA_PRIVATE_KEY = f"{recaptcha_private_key}"
    PROPAGATE_EXCEPTIONS = True
    OAUTHLIB_RELAX_TOKEN_SCOPE = 1
    TWITTER_API_KEY = f"{tw_api_key}"
    TWITTER_API_SECRET = f"{tw_api_secret}"
    FACEBOOK_CLIENT_ID = f"{fb_client_id}"
    FACEBOOK_CLIENT_SECRET = f"{fb_client_secret}"
    GITHUB_CLIENT_ID = f"{github_client_id}"
    GITHUB_CLIENT_SECRET = f"{github_client_secret}"
    GITLAB_CLIENT_ID = f"{gitlab_client_id}"
    GITLAB_CLIENT_SECRET = f"{gitlab_client_secret}"


class TestConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = b'\xe5LpK!\xa4\x99\x92G\xd1T\x82\xdfR\x0c\xb6\x95\xbd\x1c\xab\x19\x94\xc87'

    CELERY_BROKER_URL = f"amqp://{rabbitmq_user}:{rabbitmq_user_password}@127.0.0.1//"
    CELERY_RESULT_BACKEND = f"amqp://{rabbitmq_user}:{rabbitmq_user_password}@127.0.0.1//"

    SMTP_FROM = smtp_from
    SMTP_SERVER = smtp_server
    SMTP_USER = smtp_user
    SMTP_PASS = smtp_pass


