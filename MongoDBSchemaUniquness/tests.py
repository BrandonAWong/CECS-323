from pprint import pprint
from pymongo.errors import DuplicateKeyError, WriteError
from ExceptionPrint import print_exception


def test_insert(db, obj):
    collection = db["departments"]
    try:
        collection.insert_one(obj)
    except (DuplicateKeyError, WriteError) as e:
        print_exception(e)


def add_test(db):
    print("Adding base department\n"
          "---------------------------")
    department = {
            "name": "Computer Science",
            "abbreviation": "CECS",
            "chair_name": "Joe Biden's Rat",
            "building": "EN2",
            "office": 100,
            "description": "Learn how to Code."
    }
    pprint(department)
    input("Press Enter to try to insert...")
    test_insert(db, department)


def test_name(db):
    print("Testing min length of name\n"
          "---------------------------")
    department_name_minLength = {
        "name": "a",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5,
        "description": "Filler Description"
    }
    pprint(department_name_minLength)
    input("Press Enter to try to insert...")
    test_insert(db, department_name_minLength)
    input("Press Enter to continue to next case...")

    print("Testing max length of name\n"
          "---------------------------")
    department_name_maxLength = {
        "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5,
        "description": "Filler Description"
    }
    pprint(department_name_maxLength)
    input("Press Enter to try to insert...")
    test_insert(db, department_name_maxLength)
    input("Press Enter to continue to next case...")

    print("Testing uniquness of name\n"
          "---------------------------")
    department_name_unique = {
    "name": "Computer Science",
    "abbreviation": "RAND",
    "chair_name": "Ian Weiss",
    "building": "ECS",
    "office": 5,
    "description": "Filler Description"
    }
    pprint(department_name_unique)
    input("Press Enter to try to insert...")
    test_insert(db, department_name_unique) 


def test_abbreviation(db):
    print("Testing min length of abbreviation\n"
          "---------------------------")
    department_abbrv_maxLength = {
        "name": "Random Department",
        "abbreviation": "MORETHANSIX",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5,
        "description": "Filler Description"
    }   
    pprint(department_abbrv_maxLength)
    input("Press Enter to try to insert...")
    test_insert(db, department_abbrv_maxLength)
    input("Press Enter to continue to next case...")

    print("Testing uniquness of abbreviation\n"
          "---------------------------")
    department_abbrv_unique = {
        "name": "Random Department",
        "abbreviation": "CECS",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5,
        "description": "Filler Description"
    }
    pprint(department_abbrv_unique)
    input("Press Enter to try to insert...")
    test_insert(db, department_abbrv_unique)


def test_chair(db):
    print("Testing max length chair name\n"
          "---------------------------")
    department_chair_maxLength = {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "building": "ECS",
        "office": 5,
        "description": "Filler Description"
    }
    pprint(department_chair_maxLength)
    input("Press Enter to try to insert...")
    test_insert(db, department_chair_maxLength)
    input("Press Enter to continue to next case...")

    print("Testing uniquness of chair name\n"
          "---------------------------")
    department_chair_unique = {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "Joe Biden's Rat",
        "building": "ECS",
        "office": 5,
        "description": "Filler Description"
    }
    input("Press Enter to try to insert...")
    pprint(department_chair_unique)
    test_insert(db, department_chair_unique)


def test_building(db):
    print("Testing building constraint\n"
          "---------------------------")
    department_building_enum = {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "WRONG BUILDING",
        "office": 5,
        "description": "Filler Description"
    }
    pprint(department_building_enum)
    input("Press Enter to try to insert...")
    test_insert(db, department_building_enum)


def test_room(db):
    print("Testing building/room uniqueness\n"
          "---------------------------")
    department_room_unique = {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "EN2",
        "office": 100,
        "description": "Filler Description"
    }
    pprint(department_room_unique)
    input("Press Enter to try to insert...")
    test_insert(db, department_room_unique)   


def test_description(db):
    print("Testing description min length\n"
          "---------------------------")
    department_desc_minLength = {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5,
        "description": "Short"
    }
    pprint(department_desc_minLength)
    input("Press Enter to try to insert...")
    test_insert(db, department_desc_minLength)   
    input("Press Enter to continue to next case...")
    
    print("Testing description max length\n"
          "---------------------------")
    department_desc_maxLength = {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5,
        "description": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    }
    pprint(department_desc_maxLength)
    input("Press Enter to try to insert...")
    test_insert(db, department_desc_maxLength) 


def test_missing(db):
    print("Testing missing description field\n"
          "---------------------------")
    department_missing_field= {
        "name": "Random Department",
        "abbreviation": "RAND",
        "chair_name": "Ian Weiss",
        "building": "ECS",
        "office": 5
    }
    pprint(department_missing_field)
    input("Press Enter to try to insert...")
    test_insert(db, department_missing_field)

