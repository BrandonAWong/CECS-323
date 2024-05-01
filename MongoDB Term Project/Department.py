import mongoengine
from mongoengine import *

class Department(Document):
    """An organization within a particular college within a university.  Each
        department offers one or more major fields of study to its students, and
        within each major, some number of courses.  Each course is offered on
        a regular basis as a scheduled section of a given course."""
    
    name = StringField(db_field='name', max_length=80, min_length=1, required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6, min_length=1, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, min_length=5, required=True)
    building = StringField(db_field='building', max_length=10, min_length=1, required=True) #need to do enum or check on list here
    office = IntField(db_field='office', min_value=0, required=True)
    description = StringField(db_field='description', max_length=80, min_length=1, required=True)
    courses = ListField(ReferenceField('Course')) #I think this brings in the ID, not sure how to bring in the string like our design (maybe change it)
    majors = ListField(ReferenceField('Major'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_pk'},
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['chair_name'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_03'}
            ]}

    def __init__(self, name: str, abbreviation: str, chairName: str, building: str, office: int, description: str, *args, **values):
        super().__init__(*args, **values)
        if self.courses is None:
            self.courses = []  # initialize to no courses in the department
        if self.majors is None:
            self.majors = []  # initialize to no majors in the department
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
        return (f"Department: {self.name} / {self.abbreviation}\n{self.description}\n"
                f"The chair, {self.chairName} is located at {self.building} {self.office} number course offered: {len(self.courses)}")

    