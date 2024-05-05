from mongoengine import Document, IntField, StringField, EmbeddedDocumentField
from Subsets import DepartmentSubset


class Course(Document):
    """A catalog entry.  Each course proposes to offer students who enroll in
    a section of the course an organized sequence of lessons and assignments
    aimed at teaching them specified skills."""
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=699, required=True)
    courseName = StringField(db_field='course_name', max_length=80, required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)
    department = EmbeddedDocumentField(DepartmentSubset, db_field='department')


    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department.abbreviation', 'courseNumber'], 'name': 'courses_pk'},
                {'unique': True, 'fields' : ['department.abbreviation', 'courseName'], 'name': 'coursess_uk_01'}
            ]}


    def __init__(self, department: DepartmentSubset, courseNumber: int, courseName: str, description: str, units: int, *args, **values):
        super().__init__(*args, **values)
        self.department = department
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units
        

    def set_department(self, department: DepartmentSubset):
        self.department = department

    
    def __str__(self):
        return f"Department abbrev: {self.department.abbreviation} number: {self.courseNumber} name: {self.courseName} units: {self.units}"
