from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.schema import Sequence

from app import db, login_manager


class Teacher(UserMixin,db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course', backref='teachers',
                                lazy='dynamic')
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Teacher: {}>'.format(self.username) 

registrations = db.Table('registrations',  
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),  
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))  
)  
  

class Student(UserMixin,db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer,Sequence('models_student_seq', start=10000, increment=1), primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course',secondary=registrations,  
                                    backref=db.backref('students', lazy='dynamic'),  
                                    lazy='dynamic')
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student: {}>'.format(self.name) 

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    if user_id > 10000 :
        return Student.query.get(int(user_id))
    else:
        return Teacher.query.get(int(user_id))


class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    courseNums = db.Column(db.String(60), unique=True)
    # students = db.relationship('Student', backref='courses',
    #                             lazy='dynamic')
    experiments = db.relationship('Experiment', backref='courses',
                                lazy='dynamic')
    def __repr__(self):
        return '{}'.format(self.name)

class Experiment(db.Model):

    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    content = db.Colume(db.LargeBinary)
    courseName = db.Column(db.String(60), db.ForeignKey('courses.name'))
    containerName = db.Column(db.String(60))
    # students = db.relationship('Student', backref='courses',
    #                             lazy='dynamic')
    def __repr__(self):
        return '{}'.format(self.name)

class Container(db.model):
    __tablename__ = 'containers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

