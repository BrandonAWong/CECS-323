from Menu import Menu
from Option import Option


menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])


add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "add_department()"),
    Option("Major", "add_major()"),
    Option("Course", "add_course()"),
    Option("Section", "add_section()"),
    Option("Student", "add_student()"),
    Option("Major to a Student", "add_student_major()"),
    Option("Enroll Student to a Section", "add_enrollment()"),
    Option("Back", "back"),
    Option("Exit", "pass")
])


list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Departments", "list_departments()"),
    Option("Majors of a Department", "list_majors()"),
    Option("Courses of a Department", "list_courses()"),
    Option("Sections of a Course", "list_sections()"),
    Option("Students", "list_students()"),
    Option("Majors from a Student", "list_student_majors()"),
    Option("Enrollments from a Student", "list_student_enrollments()"),
    Option("Back", "back"),
    Option("Exit", "pass")
])


delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "delete_department()"),
    Option("Major", "delete_major()"),
    Option("Course", "delete_course()"),
    Option("Section", "delete_section()"),
    Option("Student", "delete_student()"),
    Option("Major from a Student", "delete_student_major()"),
    Option("Enrollment from a Student", "delete_student_enrollment()"),
    Option("Back", "back"),
    Option("Exit", "pass")
])


menu_main = Menu('main', 'Please select one of the following options:', [
Option("Add", add_menu),
Option("List", list_menu),
Option("Delete", delete_menu),
Option("Exit this application", "pass")
])
