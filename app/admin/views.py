# coding=utf-8
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from . import admin
from forms import CourseForm, ExperimentForm
from .. import db
from ..models import Student,Teacher,Experiment,Course
from ..auth.forms import UpdateForm
from werkzeug.security import generate_password_hash
import string, random


@admin.route('/courses', methods=['GET', 'POST'])
@login_required
def list_courses():
    if not current_user.isTeacher:
        abort(403)    
    courses = Course.query.filter_by(teacherName=current_user.name).all()
    return render_template('admin/courses/courses.html',
                           courses=courses, title="courses")

@admin.route('/courses/edit/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_course(name):
    """
    Edit a course
    """

#############################################################
    if not current_user.isTeacher:
        abort(403)    
    add_course = False
#############################################################

    course = Course.query.filter_by(name=name).first()
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        if Course.query.filter_by(form.courseNums.data).first().name is not name:
            flash(u'选课口令已存在，请更改')
            return redirect(url_for('admin.edit_course', name=name))
        course.name = form.name.data
        course.description = form.description.data
        course.courseNums = form.courseNums.data
        db.session.commit()
        flash(u'课程信息修改成功')

        # redirect to the courses page
        return redirect(url_for('admin.list_courses'))

    form.description.data = course.description
    form.name.data = course.name
    course.courseNums = form.courseNums.data
    return render_template('admin/courses/course.html', action="Edit",
                           add_course=add_course, form=form,
                           course=course, title="Edit Course", code=course.courseNums)

@admin.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.isTeacher:
        abort(403)    
    add_course = True
    courseNums = ''.join(random.sample(string.ascii_letters+string.digits, 8))
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data,
                                description=form.description.data,teacherName=current_user.name,
                                courseNums=form.courseNums.data)
        try:
            # add course to the database
            db.session.add(course)
            db.session.commit()
            flash(u'成功创建一门课程')
        except:
            # in case course name already exists
            flash(u'创建课程失败，可能是选课口令与已存在的课程相同')

        # redirect to courses page
        return redirect(url_for('admin.list_courses'))

    # load course template
    return render_template('admin/courses/course.html',
                           add_course=add_course, form=form,
                           title="Add Course", code=courseNums)

@admin.route('/courses/delete/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_course(name):
    if not current_user.isTeacher:
        abort(403)
    """
    Delete a course from the database
    """

    course = Course.query.filter_by(name=name).first()
    db.session.delete(course)
    db.session.commit()
    flash(u'成功删除该课程')

    # redirect to the courses page
    return redirect(url_for('admin.list_courses'))

@admin.route('/experiments')
@login_required
def list_experiments():
    if not current_user.isTeacher:
        abort(403)    
    """
    List all experiments
    """
    experiments = []
    for i in Course.query.filter_by(teacherName=current_user.name):
        for j in Experiment.query.filter_by(courseName=i.name).all():
            experiments.append(j)
    return render_template('admin/experiments/experiments.html',
                           experiments=experiments, title='experiments')


@admin.route('/experiments/delete/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_experiment(name):
    if not current_user.isTeacher:
        abort(403)
    """
    Assign a department and a role to an experiment
    """

    experiment = Experiment.query.filter_by(name=name).first()

    db.session.delete(experiment)
    db.session.commit()
    flash(u'成功删除实验')

    return redirect(url_for('admin.list_experiments'))

@admin.route('/experiments/edit/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_experiment(name):
    if not current_user.isTeacher:
        abort(403)
    """
    Edit a experiment
    """

    add_experiment = False

    experiment = Experiment.query.filter_by(name=name).first()
    form = ExperimentForm(obj=experiment)
    if form.validate_on_submit():
        experiment.name = form.name.data
        experiment.description = form.description.data
        experiment.content = form.content.data
        experiment.courseName = form.courseName.data
        experiment.containerName = form.containerName.data# .name
        db.session.commit()
        flash(u'实验修改成功')

        # redirect to the experiments page
        return redirect(url_for('admin.list_experiments'))

    experiment.name = form.name.data
    experiment.description = form.description.data
    experiment.content = form.content.data
    experiment.courseName = form.courseName.data
    experiment.containerName = form.containerName.data
    return render_template('admin/experiments/experiment.html', add_experiment=add_experiment,
                           form=form, title="Edit experiment")

@admin.route('/experiments/add', methods=['GET', 'POST'])
@login_required
def add_experiment():
    if not current_user.isTeacher:
        abort(403)
    """
    Add a experiment
    """

    add_experiment = True

    form = ExperimentForm()
    if form.validate_on_submit():
        experiment = Experiment(name=form.name.data,description=form.description.data,
            content=form.content.data,courseName=form.courseName.data,containerName=form.containerName.data)  # .name)
        try:
            db.session.add(experiment)
            db.session.commit()
            flash(u'实验创建完成')
        except:
            flash(u'实验创建失败')
            return redirect(url_for('admin.add_experiment'))
            

        # redirect to the experiments page
        return redirect(url_for('admin.list_experiments'))

    return render_template('admin/experiments/experiment.html', add_experiment=add_experiment,
                           form=form, title="Add experiment")

@admin.route('/experiments/ckupload/', methods=['POST', 'OPTIONS'])
@login_required
def ckupload():
    form = ExperimentForm()
    response = form.upload(endpoint=admin)
    return response


@admin.route('/update_infos', methods=['GET', 'POST'])
@login_required
def update_infos():
    if not current_user.isTeacher:
        abort(403)
    form = UpdateForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(name=current_user.name).first()
        teacher.realname = form.realname.data
        teacher.password_hash = form.password.data  # generate_password_hash(form.password.data)
        db.session.commit()
        db.session.close()
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('home/update_infos.html', form=form)


@admin.route('/edit_account/delete/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_account(name):
    if not current_user.isTeacher:
        abort(403)
    """
    Assign a department and a role to an experiment
    """

    student = Student.query.filter_by(name=name).first()

    db.session.delete(student)
    db.session.commit()
    flash(u'成功删除学生账户')

    return redirect(url_for('home.teacher_dashboard'))

@admin.route('/edit_account/edit/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_account(name):
    if not current_user.isTeacher:
        abort(403)
    """
    Edit a experiment
    """
    student = Student.query.filter_by(name=name).first()
    realname = student.realname
    form = UpdateForm()
    if form.validate_on_submit():
        student.realname = form.realname.data
        student.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        db.session.close()
        flash(u'修改成功')
        return redirect(url_for('home.teacher_dashboard'))
    return render_template('home/update_infos.html', name=realname, form=form)
