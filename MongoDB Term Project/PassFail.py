from mongoengine import Document, DateField, ObjectIdField
from ConstraintUtilities import validate_past_or_present
from datetime import date

      
class PassFail(Document):
    """Specifies if an enrollment is a for a class which uses a pass Fail system."""
    enrollmentID = ObjectIdField(db_field='id', primary_key=True)
    applicationDate = DateField(db_field='application_date', required=True, default=date.today, validation=validate_past_or_present)

    
    def __init__(self, enrollmentID, applicationDate: date, *args, **values):
        super().__init__(*args, **values)
        self.enrollmentID = enrollmentID
        self.applicationDate = applicationDate

    
    def __str__(self):
        return f"The application date for this enrollment is {self.applicationDate}"
