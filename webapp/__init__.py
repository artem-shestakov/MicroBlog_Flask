from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from flask_youtube.youtube import YouTube

db = SQLAlchemy()
migrate = Migrate()
celery = Celery()
debugtoolbar = DebugToolbarExtension()
cache = Cache()
yt = YouTube()


def create_app(config_object):
    from .main import create_module as main_create_module
    from .posts import create_module as posts_create_module
    from .auth import create_module as auth_create_module
    from .api import create_module as api_create_module
    from .admin import create_module as admin_create_module
    from .babel import create_module as babel_create_module

    app = Flask(__name__)
    app.config.from_object(config_object)

    # Errors handlers
    @app.errorhandler(403)
    def page_not_found(error):
        """ Return error 403 """
        return render_template('403.html'), 403

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        """ Return error 404 """
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(error):
        """ Return error 500 """
        return render_template('500.html'), 500

    db.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)

    debugtoolbar.init_app(app)
    cache.init_app(app)
    yt.init_app(app)

    main_create_module(app)
    posts_create_module(app)
    auth_create_module(app)
    api_create_module(app)
    admin_create_module(app)
    babel_create_module(app)

    return app
