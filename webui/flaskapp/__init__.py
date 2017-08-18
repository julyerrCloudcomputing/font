#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

#解决flash的一个bug
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


app = Flask(__name__)

#各项插件的配置
app.config['SECRET_KEY']='the quick brown fox jumps over a lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:123456@localhost/web'  # 配置数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap(app)
moment=Moment(app)
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import Users
    return Users.query.get(user_id)
    # return Users.query.get(int(user_id))

from flaskapp import views, models