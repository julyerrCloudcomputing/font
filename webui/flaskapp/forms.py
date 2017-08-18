# -*- coding=utf-8 -*-
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class Login_Form(FlaskForm):
    name = StringField(u'用户名', validators=[DataRequired()])
    pwd = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登录')


class Register_Form(FlaskForm):
    name = StringField(u'用户名', validators=[DataRequired()])
    pwd = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')


class Update_Form(FlaskForm):
    name = StringField(u'要修改的用户名', validators=[DataRequired()])
    pwd = PasswordField(u'该用户的新密码', validators=[DataRequired()])
    submit = SubmitField(u'确认修改')


class Delete_Form(FlaskForm):
    name = StringField(u'要删除的用户名', validators=[DataRequired()])
    submit = SubmitField(u'确认删除')


class student_update_pwd_Form(FlaskForm):
    new_pwd = PasswordField(u'新密码', validators=[DataRequired()])
    submit = SubmitField(u'确认更新密码')