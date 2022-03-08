from flask import Flask, render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
import enum
import json

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
    BTech = 'BTech'
    MTech = 'MTech'
    Phd = 'Phd'

class Section(enum.Enum):
    no_section = 'No Section'
    S1 = 'S1'
    S2 = 'S2'
    S3 = 'S3'

# course_faculty = db.Table('course_faculty',
#                           db.Column('faculty_id',db.Integer,db.ForeignKey('faculty.id')),
#                           db.Column('course_id',db.Integer,db.ForeignKey('course.id')),
# )
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=True)
    field = db.Column(db.Enum(SubField), default=SubField.TFE, nullable=False)
    # instructor = db.Column(db.Integer,db.ForeignKey(Faculty.id))
    instructors = association_proxy('course_faculty', 'faculty')
    tas = association_proxy('course_ta', 'ta')

    def __repr__(self):
        return self.name

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60),nullable = True)
    field = db.Column(db.Enum(SubField), default = SubField.TFE,nullable = False)
    # courses = db.relationship('Course',backref = 'Prof')
    # courses = db.relationship('Course',secondary=course_faculty,backref='instructors')
    courses = association_proxy('course_faculty','course')

    def __repr__(self):
        return self.name


class Course_Faculty(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    section = db.Column(db.Enum(Section), default = Section.no_section,nullable = False)

    course = db.relationship(Course, backref=backref("course_faculty"))
    faculty = db.relationship(Faculty, backref=backref("course_faculty"))
    # course = db.relationship("Course")

    def __repr__(self):
        return "course: "+str(self.course_id)+"  Faculty: "+ str(self.faculty_id)

# Course.instructors = association_proxy("instructors", "faculty")
# Faculty.courses = association_proxy("courses", "course")

# course_TA = db.Table('course_TA',
#                           db.Column('student_id',db.Integer,db.ForeignKey('student.id')),
#                           db.Column('course_id',db.Integer,db.ForeignKey('course.id')),
# )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60),nullable = True)
    program = db.Column(db.Enum(Student_Program), default=SubField.TFE, nullable=False)
    field = db.Column(db.Enum(SubField), default=SubField.TFE, nullable=False)
    #TA_courses = db.relationship('Course', secondary=course_TA, backref='TA')
    courses = association_proxy('course_ta', 'course')

class Course_Ta(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    section = db.Column(db.Enum(Section), default = Section.no_section,nullable = False)

    course = db.relationship(Course, backref=backref("course_ta"))
    ta = db.relationship(Student, backref=backref("course_ta"))

    def __repr__(self):
        return "course: "+str(self.course_id)+"  TA: "+ str(self.student_id)
#
# Course.TAs = association_proxy("TAs", "student")
# Student.courses = association_proxy("courses", "course")

@app.route("/")
def home():
    fields = [field.value for field in SubField]

    # c = Course.query.filter(Course.field.in_(['TFE']))
    # for i in c:
    #     print('newi',i.name)
    #print('c', c)
    # c = Course.query.filter(Course.field.in_(fields))
    # print('c',c)
    courses = Course.query.all()
    # print(courses)
    return render_template('home.html',courses = courses,fields=fields)

@app.route("/course", methods = ["GET","POST"])
def get_course():
    subfield = request.form.get('subfield')
    print(subfield)
    courses_query = Course.query.filter(Course.field.in_([subfield]))
    courses = [{'id':course.id,'name':course.name} for course in courses_query]
    # for course in courses_query:
    #     print('asdfa',i.name)
    print(courses)
    return jsonify(courses)

@app.route("/alloted_sections", methods = ["GET","POST"])
def get_alloted_sections():
    course_id = request.form.get('course_id')
    query = Course_Faculty.query.filter_by(course_id=course_id)
    course_sections = [{'section':q.section.value,'prof':q.faculty.name} for q in query]
    return jsonify(course_sections)

@app.route("/add_section", methods = ["GET","POST"])
def get_alloted_course():
    course_id = request.form.get('course_id')
    query = Course_Faculty.query.filter_by(course_id=course_id)
    course_sections = [{'section':q.section.value,'prof':q.faculty.name} for q in query]
    return jsonify(course_sections)

@app.route("/get_fac", methods = ["GET","POST"])
def get_fac():
    subfield,course_id,num_sections = request.form.get('subfield'),request.form.get('course_id'),int(request.form.get('num_sections'))
    query = Course_Faculty.query.filter_by(course_id=course_id)
    course_sections = [q.section.value for q in query]
    course_sections.append(Section.no_section.value)  # Adding this in course sections so that No_section is not added as a section later
    # get new sections that are to be alloted
    new_sections = [section.value for section in Section if section.value not in course_sections]
    faculty = [{'name':fac.name,'id':fac.id} for fac in Faculty.query.filter(Faculty.field.in_([subfield]))]
    response = {'sections':new_sections[:num_sections],'profs':faculty}
    # Get next sections

    # query = Course_Faculty.query.filter_by(course_id=course_id)
    # course_sections = [{'section':q.section.value,'prof':q.faculty.name} for q in query]

    return jsonify(response)

@app.route("/allot_section_fac", methods = ["GET","POST"])
def allot_section_fac():
    section_faculty_list = json.loads(request.form.get('section_faculty_list'))
    course_id = request.form.get('course_id')
    for i in section_faculty_list:
        section,faculty_id = i['section'],i['faculty_id']
        q = Course_Faculty.query.filter_by(faculty_id=faculty_id,course_id=course_id)
        if q.count()==0:
            new_entry = Course_Faculty(faculty_id=faculty_id,course_id=course_id,section=section)
            db.session.add(new_entry)
    db.session.commit()
    return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)