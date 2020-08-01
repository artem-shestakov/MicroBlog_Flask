import os
from app.wedapp import db, migrate, create_app
from app.wedapp.posts import Post, Comment, Tag, tags
from app.wedapp.auth import User

# Get config Class for app and create app object
env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app(f"config.{env.capitalize()}Config")


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, migrate=migrate, User=User, Post=Post, Comment=Comment, Tag=Tag,
                tags=tags)
