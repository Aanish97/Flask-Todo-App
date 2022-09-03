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
    password_hashed = db.Column(db.String(200), nullable=False)
    todo_list = db.relationship('Todo', backref='user', lazy=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=True)
