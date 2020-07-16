from main import app, db, migrate, manager, User, Post


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, migrate=migrate, manager=manager,User=User, Post=Post)


if __name__ == '__main__':
    manager.run()