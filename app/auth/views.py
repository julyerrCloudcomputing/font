from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Teacher,Student


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(student)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login_student'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login_student', methods=['GET', 'POST'])
def login_student():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        student = Student.query.filter_by(name=form.name.data).first()
        if student is not None and student.verifypassword(
                form.password.data):
            # log employee in
            login_user(student)

            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))


        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        teacher = Teacher.query.filter_by(name=form.name.data).first()
        if teacher is not None and teacher.verifypassword(
                form.password.data):
            # log employee in
            login_user(teacher)

            # redirect to the dashboard page after login
            return redirect(url_for('home.teacher_dashboard'))


        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('home.homepage'))


