from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin
from forms import CourseForm, ExperimentForm
from .. import db
from ..models import Student,Teacher,Experiment,Course



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
        course.name = form.name.data
        course.description = form.description.data
        course.courseNums = form.courseNums.data
        db.session.commit()
        flash('You have successfully edited the course.')

        # redirect to the courses page
        return redirect(url_for('admin.list_courses'))

    form.description.data = course.description
    form.name.data = course.name
    course.courseNums = form.courseNums.data
    return render_template('admin/courses/course.html', action="Edit",
                           add_course=add_course, form=form,
                           course=course, title="Edit Course")

@admin.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.isTeacher:
        abort(403)    
    add_course = True
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data,
                                description=form.description.data,teacherName=current_user.name,
                                courseNums=form.courseNums.data)
        try:
            # add course to the database
            db.session.add(course)
            db.session.commit()
            flash('You have successfully added a new course.')
        except:
            # in case course name already exists
            flash('Error: course name already exists or uuid should different .')

        # redirect to courses page
        return redirect(url_for('admin.list_courses'))

    # load course template
    return render_template('admin/courses/course.html',
                           add_course=add_course, form=form,
                           title="Add Course")    

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
    flash('You have successfully deleted the course.')

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
    flash('You have successfully deleted the account.')

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
        experiment.containerName = form.containerName.data.name
        db.session.commit()
        flash('You have successfully edited the experiment.')

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
            content=form.content.data,courseName=form.courseName.data,containerName=form.containerName.data.name)
        try:
            db.session.add(experiment)
            db.session.commit()
            flash('You have successfully added the experiment.')
        except:
            flash('The experiment has already exists.')
            

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
