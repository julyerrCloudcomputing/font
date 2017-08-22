from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Student,Teacher,Experiment,Course,Container
from flask_login import current_user
import uuid

class CourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    courseNums = StringField('CourseNums',default=uuid.uuid1() )
    submit = SubmitField('Submit')


class ExperimentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    content = TextAreaField('Content',default = 'please edit the content')
    courseName = QuerySelectField(query_factory=lambda: Course.query.filter_by(teacherName=current_user.name).all(),
                                  get_label="name")
    containerName = QuerySelectField(query_factory=lambda: Container.query.filter(Container.name.like('%'+courseName+'%')).all(),
                            get_label="name")
    submit = SubmitField('Submit')
