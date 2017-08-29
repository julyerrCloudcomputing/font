# coding=utf-8
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from ..models import Student, Teacher, Experiment, Course
from . import home
from .. import db


# from ..models import Employee


@home.route('/')
def homepage():
    # form = LoginForm()
    return redirect(url_for('auth.login'))  # render_template('auth/login.html', form=form)


# @home.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     return render_template('home/dashboard.html', title='Dashboard')


@home.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    print(current_user.isTeacher)
    if not current_user.isTeacher:
        abort(403)
    return render_template('home/teacher_dashboard.html', title='Teacher Dashboard')


@home.route('/list_courses', methods=['GET', 'POST'])
@login_required
def list_courses():
    courses = Student.query.filter_by(name=current_user.name).first().courses
    experimentSet = []
    for i in courses:
        experiments = Experiment.query.filter_by(courseName=i.name).all()
        experimentSet.append(experiments)
    # return render_template('home/list_courses.html', title='Student Classes', courses=courses, experimentSet=experimentSet)
    return render_template('home/list_courses.html', courses=courses, experimentSet=experimentSet, name=current_user.realname)

@home.route('/selectCourseForm', methods=['GET', 'POST'])
@login_required
def selectCourseForm():
    return render_template('home/select_course.html', name=current_user.realname)


@home.route('/selectCourse', methods=['GET', 'POST'])
@login_required
def selectCourse():  # 查询表单提交处理函数
    nums = request.form['nums']
    course = Course.query.filter_by(courseNums=nums).first()
    if course:
        current_user.courses.append(course)
        db.session.commit()
    else:
        flash("no course set the id ")
    return redirect(url_for('home.selectCourseForm'))


@home.route('/experiment/<string:name>', methods=['GET', 'POST'])
@login_required
def experiment(name):
    experiment = Experiment.query.filter_by(name=name).first()
    return render_template('pwd/index.html', experiment=experiment, title='terminal online')
