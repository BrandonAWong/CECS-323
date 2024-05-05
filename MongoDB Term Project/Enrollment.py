from mongoengine import Document, EmbeddedDocumentField, ReferenceField, StringField
from Subsets import StudentSubset


class Enrollment(Document):
    """An account of participation of a student to a section. Said instances are issued by the university and pertain to a specific course."""
    student = EmbeddedDocumentField(StudentSubset, db_field='student')  
    section = ReferenceField('Section', required=True)
    enrollment_identifier = StringField(unique=True)  # Unique identifier for enrollment

    
    meta = {'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_pk'}
            ],
           }

    
    def save(self, *args, **kwargs):
        self.enrollment_identifier = (f"{self.section.semester}-{self.section.sectionYear}-" 
                                      f"{self.section.course.department.abbreviation}-"
                                      f"{self.section.course.courseNumber}-"
                                      f"{self.student.firstName}-{self.student.lastName}")
        super().save(*args, **kwargs)
  

    def __init__(self, section, student: StudentSubset, *args, **values):
        super().__init__(*args, **values)
        self.section = section
        self.student = student

  
    def __str__(self):
      return f"{self.student.firstName} {self.student.lastName} is enrolled in {self.section}"
