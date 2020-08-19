from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_required, current_user
from webapp.auth import has_role
from .forms import CKTextArea


class StatisticView(BaseView):
    @expose("/")
    @login_required
    @has_role('administrator')
    def index(self):
        return self.render("admin/admin_index.html")


class DBView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("administrator")


class FileView(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("administrator")


class PostView(DBView):
    form_overrides = dict(text=CKTextArea)
    column_searchable_list = ('text', 'title')
    column_filters = ('publish_date',)

    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'
