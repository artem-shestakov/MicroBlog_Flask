from flask_admin import Admin
from .routes import StatisticView, DBView, PostView
from webapp.auth.models import User, db
from webapp.posts.models import Post

admin = Admin()


def create_module(app, **kwargs):
    admin.init_app(app)
    admin.add_view(StatisticView(name="Statistic"))

    models = [User]

    for model in models:
        admin.add_view(DBView(model, db.session, category="Models"))
    admin.add_view(PostView(Post, db.session, category='Models'))
