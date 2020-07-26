from wedapp import db

# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship("Post", backref="users", lazy="dynamic")

    # def __init__(self, username):
    #     self.username = username

    def __repr__(self):
        return f"<User '{self.username}'>"