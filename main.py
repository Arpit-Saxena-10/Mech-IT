from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True,nullable = True)
    email = db.Column(db.String(120), unique = True,nullable = True)
    password = db.Column(db.String(60),nullable = True)

    def __repr__(self):
        return self.username

class SubField(enum.Enum):
    TFE = 'TFE'
    Manufacturing = 'Manufacturing'
    Design = 'Design'

class Student_Program(enum.Enum):
    BTech = 'Btech'
    MTech = 'MTech'
    Phd = 'Phd'

course_faculty = db.Table('course_faculty',
                          db.Column('faculty_id',db.Integer,db.ForeignKey('faculty.id')),
                          db.Column('course_id',db.Integer,db.ForeignKey('course.id')),
)


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60),nullable = True)
    field = db.Column(db.Enum(SubField), default = SubField.TFE,nullable = False)
    # courses = db.relationship('Course',backref = 'Prof')
    courses = db.relationship('Course',secondary=course_faculty,backref='instructors')

    def __repr__(self):
        return self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=True)
    field = db.Column(db.Enum(SubField), default=SubField.TFE, nullable=False)
    # instructor = db.Column(db.Integer,db.ForeignKey(Faculty.id))

    def __repr__(self):
        return self.name

course_TA = db.Table('course_TA',
                          db.Column('student_id',db.Integer,db.ForeignKey('student.id')),
                          db.Column('course_id',db.Integer,db.ForeignKey('course.id')),
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60),nullable = True)
    program = db.Column(db.Enum(Student_Program), default=SubField.TFE, nullable=False)
    field = db.Column(db.Enum(SubField), default=SubField.TFE, nullable=False)
    TA_courses = db.relationship('Course', secondary=course_TA, backref='TA')

    # field =

@app.route("/")
def home():
    return "<h1> Home Page2</h1>"


if __name__ == '__main__':
    app.run(debug=True)