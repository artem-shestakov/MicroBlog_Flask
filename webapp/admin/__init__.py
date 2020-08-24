from flask_admin import Admin
from .routes import StatisticView, DBView, PostView, FileAdmin
from webapp.auth.models import User, db
from webapp.posts.models import Post


def create_module(app, **kwargs):
    admin = Admin(app)
    admin.add_view(StatisticView(name="Statistic"))
    admin.add_view(FileAdmin(app.static_folder, "/static", name="Static Files"))

    models = [User]

    for model in models:
        admin.add_view(DBView(model, db.session, category="Models"))
    admin.add_view(PostView(Post, db.session, category='Models'))
