# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, EqualTo

from ..models import Student,Teacher


class RegistrationForm(FlaskForm):
    name = StringField(u'学号', validators=[DataRequired()])
    realname = StringField(u'姓名', validators=[DataRequired()])
    # password = PasswordField(u'密码', validators=[
    #                         EqualTo('confirm_password'), DataRequired()])
    # confirm_password = PasswordField('Confirm Password')
    ####confirm_password not used
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if Student.query.filter_by(name=field.data).first() or Teacher.filter_by(name=field.name).first:
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    name = StringField(u'学号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    is_teacher = BooleanField()
    submit = SubmitField(u'登录')


class UpdateForm(FlaskForm):
    realname = StringField(u'姓名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'确认修改')