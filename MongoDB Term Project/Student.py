from mongoengine import Document, StringField, EmbeddedDocumentListField, ListField, ReferenceField, NotUniqueError
from StudentMajor import StudentMajor


class Student(Document):
    """An individual who may or may not be enrolled at the university, who
    enrolls in courses toward some educational objective.  That objective
    could be a formal degree program, or it could be a specialized certificate."""
    firstName = StringField(db_field='first_name', required=True)
    lastName = StringField(db_field='last_name', required=True)
    email = StringField(db_field='email', required=True)
    studentMajors = EmbeddedDocumentListField(StudentMajor, db_field='student_majors')
    enrollments = ListField(ReferenceField('Enrollment', db_field='enrollments'))


    meta = {'collection': 'students',
            'indexes': [
              {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_01'}, 
              {'unique': True, 'fields': ['email'], 'name': 'students_uk_02' }
            ]}


    def __init__(self, firstName: str, lastName: str, email: str, *args, **values):
        super().__init__(*args, **values)
        if self.studentMajors is None:
            self.studentMajors = []
        if self.enrollments is None:
            self.enrollments = []
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


    def add_major(self, major):
        if major.major in [m.major for m in self.studentMajors]:
            raise NotUniqueError(f'Operation failed.  Student already a part of {major.major}.')
        elif major not in self.studentMajors:
            self.studentMajors.append(major)


    def remove_major(self, major=None, majorName=None):
        if major and major in self.studentMajors:
            self.studentMajors.remove(major)
        elif majorName:
            [self.studentMajors.remove(m) for m in self.studentMajors if majorName == m.major]
            

    def get_majors(self):
        return self.studentMajors

    
    def add_enrollment(self, enrollment):
        if enrollment not in self.enrollments:
            self.enrollments.append(enrollment)


    def remove_enrollment(self, enrollment):
        if enrollment in self.enrollments:
            self.enrollments.remove(enrollment)

 
    def get_enrollments(self):
        return self.enrollments


    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.pk}) @ {self.email}"
