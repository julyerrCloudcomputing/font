# coding:utf-8
from flask import flash, redirect, render_template, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Teacher, Student


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(name=form.name.data).first()
        if student:
            flash(u'帐号'+form.name.data+u'已存在，无法再次创建')
            return redirect(url_for('auth.login'))
        student = Student(name=form.name.data, realname=form.realname.data,
                          password=form.password.data, isTeacher=0)
        # add employee to the database
        db.session.add(student)
        db.session.commit()
        flash(u'注册成功')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session.keys():
        if current_user.isTeacher:
            return redirect(url_for('admin.list_courses'))
        else:
            return redirect(url_for('home.list_courses'))
    # if current_user:
    #     return redirect(url_for('home.list_courses'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.is_teacher.data:
            teacher = Teacher.query.filter_by(name=form.name.data).first()
            if teacher is not None and teacher.verifypassword(
                    form.password.data):
                login_user(teacher)
                return redirect(url_for('home.teacher_dashboard'))
            else:
                flash(u'密码不正确')

        else:
            student = Student.query.filter_by(name=form.name.data).first()
            if student is not None and student.verifypassword(
                    form.password.data):
                login_user(student)
                return redirect(url_for('home.list_courses'))
            else:
                flash(u'密码不正确')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    # flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
