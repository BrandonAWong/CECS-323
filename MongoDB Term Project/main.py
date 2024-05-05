from mongoengine import NotUniqueError, ValidationError
from pymongo import monitoring
from datetime import time, date
from Utilities import Utilities
from ConstraintUtilities import select_general, unique_general, print_dup_key_error, get_retry
from CommandLogger import CommandLogger
from Menu import Menu
from Option import Option
from menu_definitions import menu_main
from Department import Department
from Major import Major
from Course import Course
from Section import Section
from Student import Student
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from LetterGrade import LetterGrade
from PassFail import PassFail
from Subsets import DepartmentSubset, CourseSubset, MajorSubset, StudentSubset


# ============================== Departments ============================== #


def select_department() -> Department:
    return select_general(Department)


def add_department():
    while True:
        try:
            department = Department(
                input("Department Name --> "),
                input("Department Abbreviation --> "),
                input("Department Chair Name --> "),
                input("Department building --> ").upper(),
                int(input("Department Office Number --> ")),
                input("Department Description --> ")
            )
        except ValueError:
            print("Invalid input.")
            if get_retry():
                continue
            break
        
        violations = unique_general(department)
        if violations:
            [print(f"Your input values violated constraint: {violation}") for violation in violations]
            if get_retry():
                continue
            break
        try:
            department.save()
            break
        except ValidationError as e:
            print(e)
            if not get_retry():
                break
            

def list_departments():
    print("Listing all Departments:")
    [print(f'{i+1}. {department}') for i, department in enumerate(Department.objects())]


def delete_department():
    department = select_department()
    if department.get_courses() or department.get_majors():
        print(f'Department still has {len(department.get_courses())} courses and '
              f'{len(department.get_majors())} majors.  Delete them first.')
    else:
        department.delete()


# ============================== Majors ============================== #


def select_major() -> Major:
    return select_general(Major)


def add_major():
  while True:
    department = select_department()
    major = Major(
        department,
        input("Major Name --> "),
        input("Major Description --> ")
    )
    violations = unique_general(major)
    if violations:
        [print(f'Your input values violated constraint: {violation}') for violation in violations]
        if get_retry():
            continue
        break
    try:
        major.save()
        department.add_major(MajorSubset(major.name))
        department.save()
        break
    except ValidationError as e:
        print(e)
        if not get_retry():
            break


def list_majors():
    department = select_department()
    print(f'Majors offered by {department.name} ({department.abbreviation})')
    [print(f'\t{i+1}. {major}\n') for i, major in enumerate(department.get_majors())]


def delete_major():
    department = select_department()
    major_menu = [Option(str(major), major) for major in department.get_majors()]
    major = Menu('Course Menu', 'Choose which course to remove', major_menu).menu_prompt()
    major_count = Student.objects(studentMajors__major=major.name).count()
    if major_count:
        print(f'{major_count} student(s) are still in {major.name}.  Delete their majors first.')
    else:
        Major.objects(name=major.name).get().delete()
        department.remove_major(major)
        department.save()


# ============================== Courses ============================== #


def select_course() -> Course:
    return select_general(Course)


def add_course():
  while True:
      try:
          department = select_department()
          course = Course(
              DepartmentSubset(department.name, department.abbreviation),
              int(input("Course Number --> ")),
              input("Course Name --> "),
              input("Course Description --> "),
              int(input("Course Units --> "))
          )
      except ValueError:
          print("Invalid input.")
          if get_retry():
              continue
          break

      try:
          course.save()
          department.add_course(CourseSubset(course.courseNumber, course.courseName))
          department.save()
          break
      except (ValidationError, NotUniqueError) as e:
            if isinstance(e, NotUniqueError):
                print_dup_key_error(e)
            else:
                print(e)
            if not get_retry():
                break


def list_courses():
  department = select_department()
  print(f'Courses offered by {department.name} ({department.abbreviation})')
  [print(f'\t{i+1}. {course}\n') for i, course in enumerate(department.get_courses())]


def delete_course():
    department = select_department()
    course_menu = [Option(str(course), course) for course in department.get_courses()]
    course = Menu('Course Menu', 'Choose which course to remove', course_menu).menu_prompt()
    course_main = Course.objects(department__abbreviation=department.abbreviation, courseNumber=course.courseNumber).get()
    section_count = Section.objects(course=course_main.pk).count()
    if section_count:
        print(f'There are {section_count} sections under {course.courseName} ({course.courseNumber}).  Delete them first.')
    else:
        course_main.delete()
        department.remove_course(course)
        department.save()


# ============================== Sections ============================== #


def select_section() -> Section:
    return select_general(Section)


def add_section():
  while True:
    try:
      section = Section(
          select_course(),
          int(input("Section Number --> ")),
          input("Section Semester --> "),
          int(input("Section Year --> ")),
          input("Section Building --> ").upper(),
          int(input("Section Room --> ")),
          input("Section Schedule --> "),
          str(time(*[int(e) for e in input("Section time (24-hour) [HH:MM] --> ").split(":")])),
          input("Section Instructor --> ")
      )
    except (ValueError, TypeError, Warning) as e:
        print("Invalid input.  Try again.")
        if get_retry():
            continue
        break
        
    violations = unique_general(section)
    if violations:
        [print(f'Your input values violated constraint: {violation}') for violation in violations]
        if get_retry():
            continue
        break
    try:
        section.save()
        break
    except (ValidationError, Warning) as e:
        print(e)
        if not get_retry():
            break


def list_sections():
    course = select_course()
    print(f'Sections of {course.department.abbreviation} {course.courseNumber} ({course.courseName}')
    [print(f'\t{i+1}. {section}\n') for i, section in enumerate(Section.objects(course=course))]


def delete_section():
    section = select_section()
    if section.get_enrollments():
        print(f'Section still has {len(section.get_enrollments())} enrollments.  Delete them first')
    else:
        section.delete()


# ============================== Students ============================== #


def select_student() -> Student:
    return select_general(Student)


def add_student():
  while True:
    student = Student(
      input("Student First Name --> "),
      input("Student Last Name --> "),
      input("Student Email --> ")
    )
      
    violations = unique_general(student)
    if violations:
        [print(f'Your input values violated constraint: {violation}') for violation in violations]
        if get_retry():
            continue
        break
    try:
        student.save()
        break
    except ValidationError as e:
        print(e)
        if not get_retry():
            break


def list_students():
    print("Listing all Students:")
    [print(f'\t{i+1}. {student}\n') for i, student in enumerate(Student.objects())]


def delete_student():
    student = select_student()
    if student.get_majors() or student.get_enrollments():
        print(f'Student still has {len(student.get_majors())} majors and '
              f'{len(student.get_enrollments())} enrollments.  Delete them first.')
    else:
        student.delete()


# ============================== StudentMajors ============================== #


def add_student_major():
    while True:
        student = select_student()
        try:
            student_major = StudentMajor(
                select_major().name,
                date(*[int(e) for e in input("Declaration Date[YYYY/MM/DD] --> ").split("/")])
            )
        except (ValueError, TypeError):
            print("Invalid input.")
            if get_retry():
                continue
            break
            
        try:
            student.add_major(student_major)
            student.save()
            break
        except (ValidationError, NotUniqueError) as e:
            print(e)
            if not get_retry():
                break


def list_student_majors():
    student = select_student()
    print(f"Listing all Majors of {student}:")
    [print(f'\t{i+1}. {major}\n') for i, major in enumerate(student.get_majors())]


def delete_student_major():
    student = select_student()
    major_menu = [Option(str(major), major) for major in student.get_majors()]
    student.remove_major(Menu('Major Menu', 'Choose which major to remove', major_menu).menu_prompt())
    student.save()


# ============================== Enrollments ============================== #


def select_enrollment() -> Enrollment:
    return select_general(Enrollment)


def select_enrollment_type() -> LetterGrade | PassFail:
    return Menu('Enrollment Type Menu', 'Choose enrollment type', 
                [Option('Letter Grade', LetterGrade),
                Option('Pass/Fail', PassFail)]).menu_prompt()


def add_enrollment():
    while True:
        student = select_student()
        section = select_section()
        enrollment = Enrollment(section, StudentSubset(student.firstName, student.lastName))
        violations = unique_general(enrollment)
        if violations:
            [print(f'Your input values violated constraint: {violation}') for violation in violations]
            if get_retry():
                continue
            break
        enrollment_type = select_enrollment_type()
        try:
            data = (input('Minimum Satisfactory Grade --> ').upper() if enrollment_type is LetterGrade 
                    else date(*[int(e) for e in input('Application Date[YYYY/MM/DD] --> ').split("/")]))
            if isinstance(data, str) and data not in ('A', 'B', 'C'):
                raise ValidationError('Minimum Grade must be one (A, B, C).')
            enrollment.save()
            enrollment_type(enrollment.pk, data).save()
            student.add_enrollment(enrollment)
            section.add_enrollment(enrollment)
            student.save()
            section.save()
            break
        except (ValueError, ValidationError, NotUniqueError) as e:
            if isinstance(e, NotUniqueError):
                print_dup_key_error(e)
            else:
                print(e)
            if not get_retry():
                break


def list_student_enrollments():
    student = select_general(Student)
    print(f"Listing all Enrollments of {student}")
    for i, enrollment in enumerate(student.get_enrollments()):
        enrollment_type = LetterGrade if LetterGrade.objects(enrollmentID=enrollment.pk).count() else PassFail
        print(f'\t{i+1}. {enrollment}\n\t{enrollment_type.objects(enrollmentID=enrollment.pk).get()}\n')


def delete_student_enrollment():
    student = select_student()
    enrollment_menu = [Option(str(enrollment), enrollment) for enrollment in student.get_enrollments()]
    enrollment = Menu('Enrollment Menu', 'Choose which enrollment to remove', enrollment_menu).menu_prompt()
    enrollment_type = LetterGrade if LetterGrade.objects(enrollmentID=enrollment.pk).count() else PassFail
    enrollment_type.objects(enrollmentID=enrollment.pk).get().delete()
    enrollment.section.remove_enrollment(enrollment)
    student.remove_enrollment(enrollment)
    student.save()
    enrollment.section.save()
    enrollment.delete()


# ============================== main ============================== #


if __name__ == '__main__':
    print("Starting in main.")
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    menu: Menu = menu_main.menu_prompt()
    action: str = ""
    while action != "pass" and isinstance(menu, Menu):
        action = menu.menu_prompt()
        if action == "back":
            menu = menu_main.menu_prompt()
            continue
        print(f"next action: {action}")
        exec(action)
    print("All done for now.")
