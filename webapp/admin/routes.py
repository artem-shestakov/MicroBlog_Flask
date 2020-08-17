from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from webapp.auth import has_role


class StatisticView(BaseView):
    @expose("/")
    @login_required
    @has_role('administrator')
    def index(self):
        return self.render("admin/admin_index.html")


class DBView(ModelView):
    pass
