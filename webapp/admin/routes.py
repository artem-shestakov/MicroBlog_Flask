from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from webapp.auth import has_role
from .forms import CKTextArea


class StatisticView(BaseView):
    @expose("/")
    @login_required
    @has_role('administrator')
    def index(self):
        return self.render("admin/admin_index.html")


class DBView(ModelView):
    pass


class PostView(DBView):
    form_overrides = dict(text=CKTextArea)
    column_searchable_list = ('text', 'title')
    column_filters = ('publish_date',)

    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'
