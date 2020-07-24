from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def page_404(error):
    render_template("404.html"), 404


def create_app(config_object):
    from .posts.routes import posts_blueprint
    from .main.routes import main_blueprint

    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(posts_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_error_handler(404, page_404)

    return app
