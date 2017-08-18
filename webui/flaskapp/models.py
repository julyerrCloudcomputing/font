# -*- coding: utf-8 -*-

from flask_login import UserMixin
from flaskapp import db

class Users(UserMixin, db.Model):
    __tablename__ = 'users'  # 对应数据库的表
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128), unique=False)
    is_admin = db.Column(db.Boolean, default=0)

    def __init__(self, name, pwd):
        self.username = name
        self.password_hash = pwd

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
