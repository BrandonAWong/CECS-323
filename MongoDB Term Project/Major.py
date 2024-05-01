from mongoengine import *
#from Department import Department
#I think we might need to bring in a reference to the department (look at orderitems)

class Major(Document):
    """A distinct field of study.  Each major has a degree program that a student
    can pursue towards a college diploma.  Many universities offer specializations
    within a major to accommodate students who have a more focused set of
    objectives for their education.  Several Departments have multiple majors.
    For instance the CECS department has both a Computer Engineering as well as
    a Computer Science major."""
    
    #Include this line if we change it to reference the department
    #department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    name = StringField(db_field='name', max_length=80, min_length=1, required=True)
    description = StringField(db_field='description', max_length=80, min_length=1, required=True)

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'majors_pk'}
            ]}

    def __init__(self, name: str, description: str, *args, **values): #department: Department (maybe)
        super().__init__(*args, **values)
        #self.department = department
        self.name = name
        self.description = description


    def __str__(self):
        return f"Major: Department - {self.department.name} Major Name: {self.name}" #this would need the reference to department

    #I think we need these methods but not sure how to implement yet
    def add_student(self, student):
       pass

    def remove_student(self, student):
        pass
