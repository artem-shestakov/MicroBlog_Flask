from .tasks import reminder_save
from .models import Reminder
from sqlalchemy import event


def create_module(app, **kwargs):
    event.listen(Reminder, "after_insert", reminder_save)
    from .routes import posts_blueprint
    app.register_blueprint(posts_blueprint)
