from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from ..models import Student,Teacher


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             EqualTo('confirm_password'), DataRequired()])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if Student.query.filter_by(name=field.data).first() or Teacher.filter_by(name=field.name).first:
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
