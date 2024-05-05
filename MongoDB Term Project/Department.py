from mongoengine import Document, EmbeddedDocument,IntField, StringField, EmbeddedDocumentListField
from Subsets import CourseSubset, MajorSubset

class Department(Document):
    """An organization within a particular college within a university.  Each
    department offers one or more major fields of study to its students, and
    within each major, some number of courses.  Each course is offered on
    a regular basis as a scheduled section of a given course."""
    name = StringField(db_field='name', max_length=80, min_length=1, required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6, min_length=1, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, min_length=5, required=True)
    building = StringField(db_field='building', choices = ('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 
                                                           'EN5', 'ET', 'HSCI', 'NUR', 'VEC'), required=True)
    office = IntField(db_field='office', min_value=0, required=True)
    description = StringField(db_field='description', max_length=80, min_length=1, required=True)
    courses = EmbeddedDocumentListField(CourseSubset, db_field='courses')
    majors = EmbeddedDocumentListField(MajorSubset, db_field='majors')

    
    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_pk'},
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['chairName'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_03'}
            ]}

    
    def __init__(self, name: str, abbreviation: str, chairName: str, building: str, office: int, description: str, *args, **values):
        super().__init__(*args, **values)
        if self.courses is None:
            self.courses = []
        if self.majors is None:
            self.majors = []
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description

    
    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    
    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    
    def get_courses(self):
        return self.courses

    
    def add_major(self, major):
        if major not in self.majors:
            self.majors.append(major)

    
    def remove_major(self, major):
        if major in self.majors:
            self.majors.remove(major)

    
    def get_majors(self):
        return self.majors

    
    def __str__(self):
        return (f"{self.name} ({self.abbreviation})\n\t{self.description}\n\t"
                f"The chair, {self.chairName} is located at {self.building} {self.office}\n\tNumber of course offered: {len(self.courses)}")
        