import hashlib
from datetime import datetime

from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

__all__ = ('User', 'Todo')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password_hashed = db.Column(db.String(200), nullable=True)
    todo_list = db.relationship('Todo', backref='user', lazy=True)

    def create_user(username, email, password):

        if username and email and password:
            hash_password = self.password(password)

            user = User(username=username,
                        email=email,
                        password=hash_password)
            db.session.add(user)
            db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hashed = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hashed, password)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=True)
