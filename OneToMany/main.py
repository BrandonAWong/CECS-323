import logging
# from os import SEEK_HOLE
# My option lists for
from menu_definitions import debug_select, menu_select, section_select, department_select, student_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Student import Student
from Section import Section
from Option import Option
from Menu import Menu
# Poor man's enumeration of the two available modes for creating the tables
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
import IPython  # So that I can exit out to the console without leaving the application.
from sqlalchemy import inspect # map from column name to attribute name
from pprint import pprint
from datetime import time

#________________________________________________________________
#Student Methods

def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    # Note that there is no physical way for us to duplicate the student_id since we are
    # using the Identity "type" for studentId and allowing PostgreSQL to handle that.
    # See more at: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == lastName,
                                                        Student.firstName == firstName).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.eMail == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    newStudent = Student(lastName, firstName, email)
    session.add(newStudent)


def select_student_id(sess: Session) -> Student:
    """
    Prompt the user for a specific student by the student ID.  Generally
    this is not a terribly useful approach, but I have it here for
    an example.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    ID: int = -1
    while not found:
        ID = int(input("Enter the student ID--> "))
        id_count: int = sess.query(Student).filter(Student.studentId == ID).count()
        found = id_count == 1
        if not found:
            print("No student with that ID.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.studentId == ID).first()
    return return_student


def select_student_first_and_last_name(sess: Session) -> Student:
    """
    Select a student by the combination of the first and last name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student last name to delete--> ")
        firstName = input("Student first name to delete--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == lastName,
                                                     Student.firstName == firstName).count()
        found = name_count == 1
        if not found:
            print("No student by that name.  Try again.")
    oldStudent = sess.query(Student).filter(Student.lastName == lastName,
                                            Student.firstName == firstName).first()
    return oldStudent


def select_student_email(sess: Session) -> Student:
    """
    Select a student by the e-mail address.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    email: str = ''
    while not found:
        email = input("Enter the student email address --> ")
        id_count: int = sess.query(Student).filter(Student.eMail == email).count()
        found = id_count == 1
        if not found:
            print("No student with that email address.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.eMail == email).first()
    return return_student


def find_student(sess: Session) -> Student:
    """
    Prompt the user for attribute values to select a single student.
    :param sess:    The connection to the database.
    :return:        The instance of Student that the user selected.
                    Note: there is no provision for the user to simply "give up".
    """
    find_student_command = student_select.menu_prompt()
    match find_student_command:
        case "ID":
            old_student = select_student_id(sess)
        case "first/last name":
            old_student = select_student_first_and_last_name(sess)
        case "email":
            old_student = select_student_email(sess)
        case _:
            old_student = None
    return old_student


def delete_student(session: Session):
    """
    Prompt the user for a student by the last name and first name and delete that
    student.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a student")
    oldStudent = find_student(session)
    session.delete(oldStudent)


def list_students(session: Session):
    """
    List all of the students, sorted by the last name first, then the first name.
    :param session:
    :return:
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    options: [Option] = []                      # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Student).filter(Student.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)

#__________________________________________________________________
# Department Methods
    
def add_department(session: Session) -> None:
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    while True: 
        name: str = input("Department name--> ")
        abbreviation: str = input("Department abbreviation--> ")
        chair_name: str = input("Department Chair--> ")
        building: str = input("Department Building--> ")
        office: int = int(input("Department Office in Building --> "))
        description: str = input("Department description --> ")

        if session.query(Department).filter(Department.abbreviation == abbreviation).count():
            print("We already have an abbreviation of that department.  Try again.")
            continue
        elif session.query(Department).filter(Department.chairName == chair_name).count():
            print("We already have that professor as chair of another department.  Try again.")
            continue
        elif session.query(Department).filter(Department.building == building, Department.office == office).count(): 
            print("That building and room already is taken by another department.  Try again.")
            continue
        elif session.query(Department).filter(Department.description == description).count():
            print("Another department already has that description.  Try again.")
            continue
        break

    session.add(Department(name, abbreviation, chair_name, building, office, description))


def delete_department(session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = find_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)

def find_department(sess: Session) -> Department:
        """
        Prompt the user for attribute values to select a single department.
        :param sess:    The connection to the database.
        :return:        The instance of Department that the user selected.
                        Note: there is no provision for the user to simply "give up".
        """
        find_department_command = department_select.menu_prompt()
        match find_department_command:
            case "abbreviation":
                old_department = select_department_abbreviation(sess)
            case "chair":
                old_department = select_department_chair(sess)
            case "building/office":
                old_department = select_department_building_office(sess)
            case "description":
                old_department = select_department_description(sess)
            case _:
                old_department = None
        print(str(old_department))
        return old_department

#Helper methods for find_department
def select_department_abbreviation(sess: Session) -> Department:
    """
    Select a department by the abbreviation.
    :param sess:	The connection to the databse.
    :return:		The selected department.
    """
    while True:
        abbreviation: str = input("Enter the department abbreviation --> ")
        if sess.query(Department).filter(Department.abbreviation == abbreviation).first():
            return sess.query(Department).filter(Department.abbreviation == abbreviation).first()
        print("No department with that abbreviation.  Try again.")

def select_department_chair(sess: Session) -> Department:
    """
    Select a department by the abbreviation.
    :param sess:	The connection to the database.
    :return: 		The selected department.
    """
    while True:
        chair: str = input("Enter the departnment chair --> ")
        if sess.query(Department).filter(Department.chairName == chair).first():
            return sess.query(Department).filter(Department.chairName == chair).first()
        print("No department with that chair.  Try again.")

def select_department_building_office(sess: Session) -> Department:
    """
    Select a department by the abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    while True:
        building: str = input("Enter the department building --> ")
        office: int = int(input("Enter the department office number --> "))
        if sess.query(Department).filter(Department.building == building, Department.office == office).first():
            return sess.query(Department).filter(Department.building == building, Department.office == office).first()
        print("No department is in that room.  Try again.")

def select_department_description(sess: Session) -> Department:
    """
    Select a department by the abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    while True:
        description: str = input("Enter the department description --> ")
        if sess.query(Department).filter(Department.description == description).count():
            return sess.query(Department).filter(Department.description == description).first()
        print("No department with that description.  Try again.")

def list_departments(session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)

def list_department_courses(sess):
    department = find_department(sess)
    dept_courses: list[Section] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)

#_______________________________________________________________________
#Course Methods
    
def add_course(session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = find_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)

def select_course(sess) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course

def delete_course(sess):
    print("deleting a course")
    course: Course = select_course(sess)
    n_sections: int = sess.query(Section).filter(Section.courseNumber == course.courseNumber).count()
    if n_sections:
        print(f"Sorry, there are {n_sections} sections of this course. Delete them first, "
              "then come back here to delete the course.")
    else:
        sess.delete(course)


def list_courses(sess):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = sess.query(Course).order_by(Course.courseNumber)
    for course in courses:
        print(course)


def move_course_to_new_department(sess):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = find_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)

def list_course_sections(sess) -> None:
    """
    List all sections currently in a course.
    :param sess:    The connection to the database.
    :return:        None
    """
    course: Course = select_course(sess)
    print(f"Sections for course: {course}")
    [print(f"{section}\n") for section in course.get_sections()]


#_____________________________________________________
# Section Methods

def add_section(sess) -> None:
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    course: Course = select_course(sess)
    while True:
        number: int = int(input("Section number--> "))
        year: int = int(input("Section year--> "))
        semester: str = get_valid_input("Section semester--> ",
                                        ("Fall", "Spring", "Winter", "Summer I", "Summer II"))

        if (sess.query(Section).filter(Section.course == course, Section.number == number,
                                       Section.year == year, Section.semester == semester).count()):
            print("We already have a section with that number.  Try again")
            continue

        schedule: str = get_valid_input("Section schedule--> ",
                                        ("MW", "TuTh", "MWF", "F", "S")) 
        start_time: time = time(*[int(e) for e in input("Section time[HH:MM]--> ").split(":")]) 
        building: str = get_valid_input("Section building--> ", 
                                        ("VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"))
        room: int = int(input("Section room--> "))

        if (sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                       Section.schedule == schedule, Section.startTime == start_time, 
                                       Section.building == building, Section.room == room).count()):
            print("We already have a section in this room.  Try again.")
            continue

        instructor: str = input("Section instructor--> ")
        if (sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                       Section.schedule == schedule, Section.startTime == start_time, 
                                       Section.instructor == instructor).count()): 
            print("We already have that instructor in a section at the same time.  Try again.")
            continue
        break
    
    sess.add(Section(course, number, semester, year, building, room, schedule, start_time, instructor))


def select_section(sess) -> Section:
    """
    Select a Section through different uniqueness constraints. 
    :param sess:    The connection to the database.
    :return:        The selected section.
    """
    command: str = section_select.menu_prompt()
    while True:
        year: int = int(input("Section year--> "))
        semester: str = get_valid_input("Section semester--> ",
                                        ("Fall", "Spring", "Winter", "Summer I", "Summer II"))
        schedule: str = get_valid_input("Section schedule--> ",
                                        ("MW", "TuTh", "MWF", "F", "S")) 
        start_time: time = time(*[int(e) for e in input("Section time[HH:MM]--> ").split(":")]) 
        match(command):
            case("building/room"):
                building: str = get_valid_input("Section building--> ", 
                                        ("VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"))
                room: int = int(input("Section room--> "))
                section: Section = sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                       Section.schedule == schedule, Section.startTime == start_time, 
                                       Section.building == building, Section.room == room).first()
            case("instructor"):
                instructor: str = input("Section instructor--> ")
                section: Section = sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                       Section.schedule == schedule, Section.startTime == start_time, 
                                       Section.instructor == instructor).first() 

        if section:
            print(section)
            return section 
        print("Section not found.  Try again.")

def delete_section(sess) -> None:
    print("deleting a section")
    sess.delete(select_section(sess))


#__________________________________________________________________
#Helper Methods

def get_valid_input(prompt: str, valid_entries: tuple | list | set) -> str:
    while True:
        usr_input = input(prompt)
        if usr_input in valid_entries:
            return usr_input
        print(f"Invalid input. Input must only be {valid_entries}.  Try again.")

if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == INTROSPECT_TABLES:
        print("reusing tables")
        # The reflection is done in the imported files that declare the entity classes, so there is no
        # reflection needed at this point, those classes are loaded and ready to go.
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")
    
    menu: Menu = menu_select.menu_prompt()
    with Session() as sess:
        action: str = ''
        while action != menu.last_action():
            action = menu.menu_prompt()
            if action == "back":
                menu = menu_select.menu_prompt()
                continue
            print('next action: ', action)
            exec(action)
        sess.commit()
    print('Ending normally')
