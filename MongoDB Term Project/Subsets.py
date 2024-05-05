from mongoengine import EmbeddedDocument, StringField, IntField


class DepartmentSubset(EmbeddedDocument):
    name = StringField(db_field='name', max_length=80, min_length=1, required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6, min_length=1, required=True)


    def __init__(self, name: str, abbreviation: str, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.abbreviation = abbreviation


class MajorSubset(EmbeddedDocument):
    name = StringField(db_field='name', max_length=80, min_length=1, required=True)


    def __init__(self, name: str, *args, **values):
        super().__init__(*args, **values)
        self.name = name


    def __str__(self):
        return self.name
        

class CourseSubset(EmbeddedDocument):
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=699, required=True)
    courseName = StringField(db_field='course_name', max_length=80, required=True)

    
    def __init__(self, courseNumber: int, courseName: str, *args, **values):
        super().__init__(*args, **values)
        self.courseNumber = courseNumber
        self.courseName = courseName


    def __str__(self):
        return f"{self.courseName} ({self.courseNumber})"


class StudentSubset(EmbeddedDocument):
    firstName = StringField(db_field='first_name', required=True)
    lastName = StringField(db_field='last_name', required=True)

    
    def __init__(self, firstName: str, lastName: str, *args, **values):
        super().__init__(*args, **values)
        self.firstName = firstName
        self.lastName = lastName
