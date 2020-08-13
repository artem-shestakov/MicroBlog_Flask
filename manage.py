import os
from webapp import db, migrate, create_app
from webapp.posts.models import Post, Comment, Tag, tags
from webapp.auth.models import User

# Get config Class for app and create app object
env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app(f"config.{env.capitalize()}Config")


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, migrate=migrate, User=User, Post=Post, Comment=Comment, Tag=Tag,
                tags=tags)
