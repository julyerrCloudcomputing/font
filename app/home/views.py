# coding=utf-8
from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import login_required, current_user, logout_user
from ..models import Student, Teacher, Experiment, Course
from . import home
from .. import db
from ..auth.forms import UpdateForm
from werkzeug.security import generate_password_hash
import json

from ..models import Container


# @home.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     return render_template('home/dashboard.html', title='Dashboard')


@home.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if not current_user.isTeacher:
        abort(403)
    students = Student.query.all()
    return render_template('home/teacher_dashboard.html', students=students)


@home.route('/list_courses', methods=['GET', 'POST'])
@login_required
def list_courses():
    courses = Student.query.filter_by(name=current_user.name).first().courses
    experimentSet = []
    for i in courses:
        experiments = Experiment.query.filter_by(courseNums=i.courseNums).all()
        experimentSet.append(experiments)
    # return render_template('home/list_courses.html', title='Student Classes', courses=courses,
    # experimentSet=experimentSet)
    return render_template('home/list_courses.html', courses=courses, experimentSet=experimentSet,
                           name=current_user.realname)


@home.route('/selectCourseForm', methods=['GET', 'POST'])
@login_required
def selectCourseForm():
    return render_template('home/select_course.html')


@home.route('/selectCourse', methods=['GET', 'POST'])
@login_required
def selectCourse():  # 查询表单提交处理函数
    nums = request.form['nums']
    course = Course.query.filter_by(courseNums=nums).first()
    if course:
        try:
            current_user.courses.append(course)
            db.session.commit()
            flash(u'选课成功')
            return redirect(url_for('home.list_courses'))
        except:
            flash(u'选课失败，可能是您已经拥有该门课程')
            return redirect(url_for('home.list_courses'))
    else:
        flash(u'选课码无效')
        return redirect(url_for('home.selectCourseForm'))


@home.route('/experiment/<string:id>', methods=['GET', 'POST'])
@login_required
def experiment(id):
    experiment = Experiment.query.filter_by(id=id).first()
    return render_template('pwd/index.html', content=experiment.content,
                           containerName=experiment.containerName,
                           isTeacher=0, title='terminal online')


@home.route('/update_infos', methods=['GET', 'POST'])
@login_required
def update_infos():
    form = UpdateForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(name=current_user.name).first()
        student.realname = form.realname.data
        student.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        db.session.close()
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('home/update_infos.html', name=current_user.realname, form=form)


@home.route('/images/search', methods=['GET', 'POST'])
def images_search():
    imageName = json.loads(request.get_data())
    imageNames = []
    for i in Container.query.filter(Container.name.like('%' + imageName['term'] + '%')).all():
        imageNames.append(i.name)
    return jsonify(imageNames)
