from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

followers = db.Table("followers", db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
                     db.Column("followed_id", db.Integer, db.ForeignKey("user.id")))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140), default="")
    gender = db.Column(db.String(20), default="Prefer not to say")
    avatar = db.Column(db.String(200), default="/static/images/defaultAvatar.png")
    projects = db.relationship("Project", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(64))
    description = db.Column(db.String(600), default="")
    rating = db.Column(db.Float)
    category = db.Column(db.String(40))
    download_file = db.Column(db.String(200), default="")
    screenshots = db.relationship("Screenshot", backref="project", lazy="dynamic")
    comments = db.relationship("Comment", backref="project", lazy="dynamic")

class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))