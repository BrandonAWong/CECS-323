import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from pymongo.errors import WriteError, DuplicateKeyError
from Menu import Menu
from menu_definitions import menu_main 
from ExceptionPrint import print_exception
from tests import *


def setup_students_collection(students):
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        print("e-mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')


def setup_departments_collection(departments):
        departments_indexes = departments.index_information()
        if'departments_name' in departments_indexes.keys():
            print("name index present")
        else:
            departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='departments_name')
            
        if'departments_abbreviation' in departments_indexes.keys():
            print("abbreviation index present")
        else:
            departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')

        if'departments_chair_name' in departments_indexes.keys():
            print("chair_name index present")
        else:
            departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_name')

        if'deapartments_building_and_office' in departments_indexes.keys():
            print("building and office index present")
        else:
            departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)], 
                                    unique=True, name='deapartments_building_and_office')
        
        if'deapartments_description' in departments_indexes.keys():
            print("description index present")
        else:
            departments.create_index([('description', pymongo.ASCENDING)], unique=True, name='departments_description')


def add_departments_validator(db):
    departments_validator = {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "A division of a university where faculty are devoted to a particular academic discipline",
                    'required': ["name", "abbreviation", "chair_name", "building", "office", "description"],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'name': {
                            'bsonType': "string",
                            'minLength': 10,
                            'maxLength': 50,
                            'description': "Name of the department"
                        },
                        'abbreviation': {
                            'bsonType': "string",
                            'maxLength': 6,
                            'description': "Shorthand abbreviation of department name"
                        },
                        'chair_name': {
                            'bsonType': "string",
                            'maxLength': 80,
                            'description': "Name of the head of the department"
                        },
                        'building': {
                            'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "ET", "HSCI", "NUR", "VEC"],
                            'description': "The building that contains the department chair's office"
                        },
                        'office': {
                            'bsonType': "number",
                            'description': "Room number of the department chair's office"
                        },
                        'description': {
                            'bsonType': "string",
                            'minLength': 10,
                            'maxLength': 80,
                            'description': "Description of the department"
                        }
                    }
                }
            }
        }

    db.command("collMod", "departments", **departments_validator)


def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = collection.count_documents({"e_mail": email})
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    # Build a new students document preparatory to storing it
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    results = collection.insert_one(student)
    

def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from 
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def delete_student(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    student = select_student(db)
    # Create a "pointer" to the students collection within the db database.
    students = db["students"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = students.delete_one({"_id": student["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} students.")


def list_student(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)


def add_department(db):
    """
    Add a new Department
    :param collection:  The pointer to the departments collection.
    :return:            None
    """
    collection = db["departments"]
    while True:
        name = input("Department name-> ")
        abbrv = input("Department abbreviation--> ")
        chair = input("Department chair name--> ")
        building = input("Department building--> ")
        try:
            office = int(input("Department office number--> "))
        except ValueError:
            print("Wrong value type entered.  Try again.")
            continue
        desc = input("Department description--> ")
        try:
            collection.insert_one(
                {
                "name": name,
                "abbreviation": abbrv,
                "chair_name": chair,
                "building": building,
                "office": office,
                "description": desc
                }
            )
            return 
        except (WriteError, DuplicateKeyError) as e:
            print_exception(e)

def select_department(db):
    """
    Select a department by department name.
    :param db:      The connection to the database.
    :return:        The selected department as a dict.  
    """
    # Create a connection to the students collection from this database
    collection = db["departments"]

    while True:
        name = input("Department Name--> ")
        if not collection.count_documents({"name": name}):
            print("No Department found by that name.  Try again.")
            continue
        break
    return collection.find_one({"name": name})


def delete_department(db):
    """
    Delete a department from the database.
    :param db:  The current database connection.
    :return:    None
    """
    department = select_department(db)
    departments = db["departments"]
    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments.")


def list_department(db):
    """
    List all of the departments, sorted by name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    for department in departments:
        pprint(department)
        print()


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [CECS-323-Spring-2023-user] -->') or \
                    "CECS-323-Spring-2023-user"
    project: str = input('Mongo project name [cecs-323-spring-2023] -->') or \
                   "CECS-323-Spring-2023"
    hash_name: str = input('7-character database hash [puxnikb] -->') or "puxnikb"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    cluster = "mongodb+srv://brandonwong2004:joe@school-management-syste.zkhdl1x.mongodb.net/?retryWrites=true&w=majority&appName=school-management-system"    
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    #___________________Set up the students collection___________________
    setup_students_collection(students)
    pprint(students.index_information())


        #___________________Set up the departments collection___________________
    setup_departments_collection(departments)
    pprint(departments.index_information())

    menu: Menu = menu_main.menu_prompt()
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        if action == "back":
            menu = menu_main.menu_prompt()
            continue
        print('next action: ', action)
        exec(action)

