from mongoengine import EmbeddedDocument, DateField, StringField
from ConstraintUtilities import validate_past_or_present
from datetime import date


class StudentMajor(EmbeddedDocument):
    """The association class between Student and Major."""
    major = StringField(db_field='major', required=True)
    declarationDate = DateField(db_field='declaration_date', required=True, default = date.today, validation=validate_past_or_present)

    
    def __init__(self, major: str, declarationDate: date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.major = major
        self.declarationDate = declarationDate
        

    def __str__(self):
        return self.major
