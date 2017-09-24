# coding=utf-8
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from . import admin
from forms import CourseForm, ExperimentForm
from .. import db
from ..models import Student,Teacher,Experiment,Course, registrations
from ..auth.forms import UpdateForm
from werkzeug.security import generate_password_hash
import string, random


@admin.route('/courses', methods=['GET', 'POST'])
@login_required
def list_courses():
    courses = Course.query.filter_by(teacherName=current_user.name).all()
    return render_template('admin/courses/courses.html',
                           courses=courses, title="courses")

@admin.route('/courses/edit/<string:name>', methods=['GET', 'POST'])
@login_required
def edit_course(name):
    """
    Edit a course
    """
    if not current_user.isTeacher:
        abort(403)
    add_course = False
    course = Course.query.filter_by(courseNums=name).first()
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.name = form.name.data
        course.description = form.description.data
        db.session.commit()
        flash(u'课程信息修改成功')
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
    """
    Delete a course from the database
    """

    course = Course.query.filter_by(courseNums=name).first()
    db.session.delete(course)
    db.session.commit()
    flash(u'成功删除该课程')

    # redirect to the courses page
    return redirect(url_for('admin.list_courses'))

@admin.route('/experiments')
@login_required
def list_experiments():
    """
    List all experiments
    """
    experiments = []
    # for course in Course.query.filter_by(teacherName=current_user.name):
    #     for experiment in Experiment.query.filter_by(courseNums=course.courseNums).all():
    #         experiments.append(experiment)
    for experiment in Experiment.query.filter_by(teacherName=current_user.name):
        experiments.append(experiment)
    return render_template('admin/experiments/experiments.html',
                           experiments=experiments, title='experiments')


@admin.route('/experiments/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_experiment(id):
    """
    Assign a department and a role to an experiment
    """

    experiment = Experiment.query.filter_by(id=id).first()

    db.session.delete(experiment)
    db.session.commit()
    flash(u'成功删除实验')

    return redirect(url_for('admin.list_experiments'))

@admin.route('/experiments/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_experiment(id):
    """
    Edit a experiment
    """

    add_experiment = False

    experiment = Experiment.query.filter_by(id=id).first()
    form = ExperimentForm(obj=experiment)
    if form.validate_on_submit():
        experiment.name = form.name.data
        experiment.description = form.description.data
        experiment.content = form.content.data
        experiment.courseNums = form.courseNums.data.courseNums
        # type(form.courseNums.data) is app.models.course
        experiment.containerName = form.containerName.data# .name
        # type(form.containerName.data) is unicode
        db.session.commit()
        flash(u'实验修改成功')

        # redirect to the experiments page
        return redirect(url_for('admin.list_experiments'))

    experiment.name = form.name.data
    experiment.description = form.description.data
    experiment.content = form.content.data
    experiment.courseNums = form.courseNums.data# .courseNums
    experiment.containerName = form.containerName.data
    return render_template('admin/experiments/experiment.html', add_experiment=add_experiment,
                           form=form, title="Edit experiment")

@admin.route('/experiments/add', methods=['GET', 'POST'])
@login_required
def add_experiment():
    """
    Add a experiment
    """

    add_experiment = True

    form = ExperimentForm()
    if form.validate_on_submit():
        experiment = Experiment(name=form.name.data,description=form.description.data,
                    content=form.content.data,courseNums=form.courseNums.data.courseNums,
                    containerName=form.containerName.data, teacherName=current_user.name)  # .name)
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
    form = UpdateForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(name=current_user.name).first()
        teacher.realname = form.realname.data
        teacher.password_hash = form.password.data  # generate_password_hash(form.password.data)
        db.session.commit()
        db.session.close()
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('home/update_infos.html', form=form, name=current_user.realname)


@admin.route('/edit_account/delete/<string:name>', methods=['GET', 'POST'])
@login_required
def delete_account(name):
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


@admin.route('/related_students')
def related_students():
    """
    list all related students.
    """
    courses = Teacher.query.filter_by(name=current_user.name).first().courses
    studentsList = []
    for course in courses:
        students = db.session.query(registrations).filter_by(courseNums=course.courseNums).all()
        studentsList.append(students)
    print studentsList, '\n\n\n'
    return render_template('admin/related_students.html',
                           courses=courses, studentsList=studentsList)

@admin.route('/experiment_before', methods=['GET', 'POST'])
@login_required
def experiment_before():
    # experiment = Experiment.query.filter_by(name=name).first()
    return render_template('pwd/index.html',isTeacher=1, title='terminal online')

@admin.before_request
def teacher_required():
    if not current_user.isTeacher:
        abort(403)
