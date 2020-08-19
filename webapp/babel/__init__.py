from flask_babel import Babel
from flask import has_request_context, session

babel = Babel()


@babel.localeselector
def get_locale():
    if has_request_context():
        locale = session.get("locale")
        if locale:
            return locale
        session["locale"] = "en"
        return session["locale"]


def create_module(app):
    babel.init_app(app)
    from .routes import babel_blueprint
    app.register_blueprint(babel_blueprint)
