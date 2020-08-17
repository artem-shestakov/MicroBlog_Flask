from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from flask_assets import Bundle, Environment

db = SQLAlchemy()
migrate = Migrate()
celery = Celery()
debugtoolbar = DebugToolbarExtension()
cache = Cache()
assets_app = Environment()

css_bundle = Bundle(
    "css/bootstrap.css",
    filters="cssmin",
    output="css/common.css"
)

js_bundle = Bundle(
    "js/ckeditor/ckeditor.js",
    filters="jsmin",
    output="js/common.js"
)


def create_app(config_object):
    from .main import create_module as main_create_module
    from .posts import create_module as posts_create_module
    from .auth import create_module as auth_create_module
    from .api import create_module as api_create_module
    from .admin import create_module as admin_create_module

    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)

    debugtoolbar.init_app(app)
    cache.init_app(app)
    assets_app.init_app(app)
    assets_app.register("css_app", css_bundle)
    assets_app.register("js_app", js_bundle)

    main_create_module(app)
    posts_create_module(app)
    auth_create_module(app)
    api_create_module(app)
    admin_create_module(app)

    return app
