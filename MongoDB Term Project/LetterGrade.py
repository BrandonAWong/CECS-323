from mongoengine import Document, StringField, ObjectIdField


class LetterGrade(Document):
    """Specifies if an enrollment is a for a class which uses letter grades rather than pass fail."""
    enrollmentID = ObjectIdField(db_field='id', primary_key=True)
    minSatisfactory = StringField(db_field='min_satisfactory', choices=("A", "B", "C"), required=True)

    
    def __init__(self, enrollmentID, minSatisfactory: str, *args, **values):
        super().__init__(*args, **values)
        self.enrollmentID = enrollmentID
        self.minSatisfactory = minSatisfactory

    
    def __str__(self):
        return f"The miniumum letter grade for this enrollment is {self.minSatisfactory}"
