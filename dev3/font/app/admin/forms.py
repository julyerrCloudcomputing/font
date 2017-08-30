# coding=utf-8
import os, random, datetime

from flask import make_response, current_app, request, url_for
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
    courseNums = StringField('CourseNums')
    submit = SubmitField('Submit')


class CKEditor(object):
    def __init__(self):
        pass

    def gen_rnd_filename(self):
        """generate a random filename"""
        filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))

    def upload(self, endpoint=current_app):
        """img or file upload methods"""
        error = ''
        url = ''
        callback = request.args.get("CKEditorFuncNum")

        if request.method == 'POST' and 'upload' in request.files:
            # /static/upload
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            rnd_name = '%s%s' % (self.gen_rnd_filename(), fext)
            filepath = os.path.join(endpoint.static_folder, 'upload', rnd_name)

            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                    error = 'ERROR_DIR_NOT_WRITEABLE'
            if not error:
                fileobj.save(filepath)
                url = url_for('admin.static', filename='%s/%s' % ('upload', rnd_name))
        else:
            error = 'post error'

        res = """
                <script type="text/javascript">
                window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
                </script>
             """ % (callback, url, error)

        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response

class ExperimentForm(FlaskForm, CKEditor):
    name = StringField(u'实验名称', validators=[DataRequired()])
    description = StringField(u'实验简介', validators=[DataRequired()])
    content = TextAreaField(u'实验指导')
    courseName = QuerySelectField(u'所属课程', query_factory=lambda: Course.query.filter_by(teacherName=current_user.name).all(),
                                  get_label="name")
    containerName = QuerySelectField(u'所需镜像', query_factory=lambda: Container.query.filter(Container.name.like('%'+'centos'+'%')).all(),
                            get_label="name")
    submit = SubmitField(u'提交')
