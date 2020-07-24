import os
from wedapp import db, migrate, create_app
from wedapp.posts.model import User, Post, Comment, Tag, tags

# Get config Class for app and create app
env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app(f"config.{env.capitalize()}Config")


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, migrate=migrate, User=User, Post=Post, Comment=Comment, Tag=Tag,
                tags=tags)
