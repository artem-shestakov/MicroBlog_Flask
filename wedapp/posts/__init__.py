def create_module(app, **kwargs):
    from .routes import posts_blueprint
    app.register_blueprint(posts_blueprint)