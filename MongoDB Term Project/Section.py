from mongoengine import Document, IntField, ListField, StringField, ReferenceField, DENY
from Course import Course 
from Enrollment import Enrollment

def validate_start_time(value):
    start_hour, start_minute, _ = [int(e) for e in value.split(":")]
    if start_hour < 8 or start_hour >= 19 or (start_hour == 19 and start_minute > 30):
        raise Warning("Start time should be between 8:00 and 19:30.")


class Section(Document):
    """An individual instance of a course within a university in which students 
    can enroll. Said instances are commonly differentiated by an integer with two 
    digits. Examples may include: Section 03 of the course CECS 323.""" 
    sectionNumber = IntField(db_field='section_number', min_value=1, max_value=20, required=True)
    semester = StringField(db_field='semester', choices = ('Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'), required=True)
    sectionYear = IntField(db_field='section_year', min_value=1, required=True) 
    building = StringField(db_field='building', choices = ('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 
                                                           'EN5', 'ET', 'HSCI', 'NUR', 'VEC'), required=True)
    room = IntField(db_field='room', min_value=1, max_value=999, required=True)
    schedule = StringField(db_field='schedule', choices=('MW', 'TuTh', 'MWF', 'F', 'S'), required=True) 
    startTime = StringField(db_field='start_time', max_length=20, required=True, validation=validate_start_time)
    instructor = StringField(db_field='instructor', max_length=40, required=True)
    course = ReferenceField(Course, required=True, reverse_delete_rule=DENY)
    enrollments = ListField(ReferenceField(Enrollment, db_field='enrollments'))

    
    meta = {'collection': 'sections',
            'indexes': [
                    {'unique': True, 'fields': ['course', 'sectionNumber','semester', 'sectionYear'], 'name': 'sections_pk'},
                    {'unique': True, 'fields' : ['semester', 'sectionYear','building', 'room', 'schedule', 'startTime'], 'name': 'sections_uk_01'},
                    {'unique': True, 'fields' : ['semester', 'sectionYear','schedule', 'startTime', 'instructor'], 'name': 'sections_uk_02'}
            ]}

    
    def __init__(self,  course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str, 
                room: int, schedule: str, startTime, instructor: str, *args, **values):
        super().__init__(*args, **values)
        if self.enrollments is None:
              self.enrollments = []
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor
        self.course = course

    
    def add_enrollment(self, enrollment):
        if enrollment not in self.enrollments:
            self.enrollments.append(enrollment)


    def remove_enrollment(self, enrollment):
        if enrollment in self.enrollments:
            self.enrollments.remove(enrollment)


    def get_enrollments(self):
        return self.enrollments

    
    def __str__(self):
        return (f"Course number: {self.course.courseNumber} Course name: {self.course.courseName}\n\t"
                f"Section number: {self.sectionNumber} Semester: {self.semester} Section year: {self.sectionYear}\n\t"
                f"Instructor: {self.instructor} Schedule: {self.schedule} Start time: {self.startTime}\n\t"
                f"Building: {self.building} Room: {self.room}")
