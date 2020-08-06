from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object):
    from .main import create_module as main_create_module
    from .posts import create_module as posts_create_module
    from .auth import create_module as auth_create_module
    from .api import create_module as api_create_module

    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    main_create_module(app)
    posts_create_module(app)
    auth_create_module(app)
    api_create_module(app)

    return app
