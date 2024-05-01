from mongoengine import *
#from Department import Department need this to embed but not sure how we are doing that


class Course(Document):
    """A catalog entry.  Each course proposes to offer students who enroll in
        a section of the course an organized sequence of lessons and assignments
        aimed at teaching them specified skills."""
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=699, required=True)
    courseName = StringField(db_field='course_name', max_length=80, required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)
    department = EmbeddedDocumentField(Department, db_field='department')
    #maybe use reference field for department?

    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department_abbreviation', 'course_number'], 'name': 'courses_pk'},
                {'unique': True, 'fields' : ['department_abbreviation', 'course_name'], 'name': 'coursess_uk_01'}
            ]}


    def __init__(self, courseNumber: int, courseName: str, description: str, units: int, *args, **values):
        super().__init__(*args, **values)
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units


    def set_department(self, department: Department):
        pass
        #self.department = department

    def __str__(self):
        return f"Department abbrev: {self.department.abbreviation} number: {self.courseNumber} name: {self.name} units: {self.units}"
        #i think we can use self.department.abbreviation
