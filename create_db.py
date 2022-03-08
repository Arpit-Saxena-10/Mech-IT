from main2 import db,Student,Faculty,Course,Course_Faculty,Course_Ta

db.create_all()

s1 = Student(name='abc',program = 'MTech',field='TFE')
c1 = Course(name = 'Fluid',field='TFE')
c2 = Course(name = 'Manpro',field='Manufacturing')
c3 = Course(name = 'Thermo',field='TFE')
f1 = Faculty(name = 'f1',field='TFE')

db.session.add_all([c1,c2,c3,f1,s1])
db.session.commit()
print(f1.courses)
# f1.courses.append(c1)
cf=Course_Faculty(course_id =c1.id,faculty_id=f1.id,section='S1')
db.session.add_all([cf])
db.session.commit()

print(f1.courses)
print(c1.instructors)
print(Course_Faculty.query.all())
print(f1.courses[0])
print(c1.instructors[0])
# db.session.add_all([f1])
# print(Faculty.query.all()[0].courses)
# print(Course.query.all()[0].instructors)
#db.session.commit()

cs = Course_Ta(course_id = c1.id,student_id=s1.id)
db.session.add_all([cs])
db.session.commit()
print()
print(c1.tas)
print(s1.courses)
print(Course_Ta.query.filter_by(course=c1,ta=s1).first().section.value)
#c.instructors