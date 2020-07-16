from main import app, db, migrate, User, Post, Comment, Tag, tags


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, migrate=migrate, User=User, Post=Post, Comment=Comment, Tag=Tag,
                tags=tags)
