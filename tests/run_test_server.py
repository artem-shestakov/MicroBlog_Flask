from webapp import create_app, db
from webapp.auth.models import User, Role

app = create_app('config.TestConfig')

db.app = app
db.create_all()

with app.app_context():
    user_role = Role("user")
    author_role = Role("author")
    db.session.add(user_role)
    db.session.add(author_role)
    db.session.commit()

    test_user = User(email="test@test.com", f_name="test")
    test_user.set_password("test")
    test_user.roles.append(author_role)
    db.session.add(test_user)
    db.session.commit()

app.run()
