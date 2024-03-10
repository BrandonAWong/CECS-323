import logging
from constants import *
from menu_definitions import select_menu, debug_select, section_select, department_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Section import Section
from Enrollment import Enrollment
from Option import Option
from Menu import Menu
from SQLAlchemyUtilities import check_unique
from datetime import time
from pprint import pprint



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


def add_course(session: Session):
    """
    This demonstrates how to use the utilities in SQLAlchemy Utilities for checking
    all the uniqueness constraints of a table in one method call.  The user
    experience is tougher to customize using this technique, but the benefit is that
    new uniqueness constraints will be automatically added to the list to be checked,
    without any change to the add_course code.

    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    violation = True  # Flag that we still have to prompt for fresh values
    while violation:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        course = Course(department, number, name, description, units)
        violated_constraints = check_unique(Session, course)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(course)


def add_section(sess: Session) -> None:
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

        if (sess.query(Section).filter(Section.course == course, Section.sectionNumber == number,
                                       Section.sectionYear == year, Section.semester == semester).count()):
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


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this major?")
    department: Department = select_department(sess)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.departmentAbbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    while not unique_email or not unique_name:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == last_name,
                                                        Student.firstName == first_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.email == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that email address.  Try again.")
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def add_student_major(sess):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That student already has that major.  Try again.")
        student = select_student(sess)
        major = select_major(sess)
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(student)                           # add the StudentMajor to the session
    sess.flush()


def add_major_student(sess):
    while True:
        major: Major = select_major(sess)
        student: Student = select_student(sess)
        if not sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                StudentMajor.majorName == major.name).count():
            break
        print("That major already has that student.  Try again.")
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(major)                           # add the StudentMajor to the session
    sess.flush()


def add_student_section(sess: Session) -> None:
    while True:
        student: Student = select_student(sess)
        section: Section = select_section(sess)
        if not sess.query(Enrollment).filter(Enrollment.studentId == student.studentID, 
                Enrollment.departmentAbbreviation == section.departmentAbbreviation,
                Enrollment.courseNumber == section.courseNumber,
                Enrollment.sectionNumber == section.sectionNumber,
                Enrollment.semester == section.semester,
                Enrollment.sectionYear == section.sectionYear).count():
            break
        print("That student is already in the section")
    student.add_section(section)
    sess.add(student)
    sess.flush()
    

def add_section_student(sess: Session) -> None:
    while True:
        section: Section = select_section(sess)
        student: Student = select_student(sess)
        if not sess.query(Enrollment).filter(Enrollment.studentId == student.studentID, 
                Enrollment.departmentAbbreviation == section.departmentAbbreviation,
                Enrollment.courseNumber == section.courseNumber,
                Enrollment.sectionNumber == section.sectionNumber,
                Enrollment.semester == section.semester,
                Enrollment.sectionYear == section.sectionYear).count():
            break
        print("That section already hast this student")
    section.add_student(student)
    sess.add(section)
    sess.flush()

def select_department(sess: Session) -> Department:
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

def select_course(sess: Session) -> Course:
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

def select_section(sess) -> Section:
    """
    Select a Section through different uniqueness constraints. 
    :param sess:    The connection to the database.
    :return:        The selected section.
    """
    command: str = section_select.menu_prompt()
    while True:
        try:
            year: int = int(input("Section year--> "))
            semester: str = get_valid_input("Section semester--> ",
                                            ("Fall", "Spring", "Winter", "Summer I", "Summer II"))
            schedule: str = get_valid_input("Section schedule--> ",
                                            ("MW", "TuTh", "MWF", "F", "S")) 
            start_time: time = time(*[int(e) for e in input("Section time[HH:MM]--> ").split(":")]) 
            match(command):
                case("course/section_num"):
                    course: Course = select_course(sess)
                    section_number: int = int(input("Section number--> "))
                    section: Section = sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                            Section.schedule == schedule, Section.startTime == start_time,
                                            Section.courseNumber == course.courseNumber, 
                                            Section.departmentAbbreviation == course.departmentAbbreviation,
                                            Section.sectionNumber == section_number).first()
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

        except ValueError:
            print("Invalid Input.  Try again.")

        if section:
            print(section)
            return section
        print("Section not found.  Try again.")

def select_student(sess) -> Student:
    """
    Select a student by the combination of the last and first.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == last_name,
                                                     Student.firstName == first_name).count()
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    student: Student = sess.query(Student).filter(Student.lastName == last_name,
                                                  Student.firstName == first_name).first()
    return student


def select_major(sess) -> Major:
    """
    Select a major by its name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = sess.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major: Major = sess.query(Major).filter(Major.name == name).first()
    return major


def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    student: Student = select_student(session)
    """This is a bit ghetto.  The relationship from Student to StudentMajor has 
    cascade delete, so this delete will work even if a student has declared one
    or more majors.  I could write a method on Student that would return some
    indication of whether it has any children, and use that to let the user know
    that they cannot delete this particular student.  But I'm too lazy at this
    point.
    """
    session.delete(student)


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_student_major(sess):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_major_student(sess: Session):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def delete_student_section(sess: Session):
    print("Prompting you for the student and the section they are no longer a part of.")
    select_student(sess).remove_enrollment(select_section(sess))


def delete_section_student(sess: Session):
    print("Prompting you for the section and the student who is no longer a part of that section.")
    select_section(sess).remove_enrollment(select_student(sess))

def delete_student(sess: Session) -> None:
    print("deleting a student")
    student: Student = select_student(sess)
    if student.sections:
        print(f"Student is in {len(student.sections)}.  Remove those first before removing student")
    else:
        sess.delete(student)


def delete_section(sess: Session) -> None:
    print("deleting a section")
    section: Section = select_section(sess)
    if section.students:
        print(f"Section contains {len(section.students)} students.  Delete them first then try again.")
    else:
        sess.delete(section)


def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: list[Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(sess.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_section(sess:Session) -> None:
    [print(section) for section in list(sess.query(Section).order_by(Section.sectionNumber))]


def list_student(sess: Session):
    """
    List all Students currently in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(sess: Session):
    """
    List all majors in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(sess.query(Major).order_by(Major.departmentAbbreviation))
    for major in majors:
        print(major)


def list_student_major(sess: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param sess:    The connection to the database
    :return:        None
    """
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_major_student(sess: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param sess:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_student_section(sess: Session) -> None:
    [print(section) for section in select_student(sess).sections]


def list_section_student(sess: Session) -> None:
    [print(student) for student in select_section(sess).students]


def move_course_to_new_department(sess: Session):
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
    new_department = select_department(sess)
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
    students: list[Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: list[Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: list[Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(sess):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess:    The session that's open.
    :return:        None
    """
    department: Department = Department("Computer Science", "CECS", "Joe biden", "ECS", 1, "hello!")
    course = Course(department, 323, "Data", "yolo", 3)
    section = Section(course, 3, "Spring", 2024, "ECS", 2, "MW", time(12,30), "donald")
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    sess.add(department)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)
    sess.add(course)
    sess.add(section)
    sess.flush()                                # Force SQLAlchemy to update the database, although not commit


def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess:    The connection to the database.
    :return:        None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())


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
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    menu: Menu = select_menu.menu_prompt()
    with Session() as sess:
        action: str = ''
        while action != menu.last_action():
            action = menu.menu_prompt()
            if action == "back":
                menu = select_menu.menu_prompt()
                continue
            print('next action: ', action)
            exec(action)
        sess.commit()
    print('Ending normally')
