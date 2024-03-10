from Menu import Menu
from Option import Option
from constants import *
"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "add_department(sess)"),
    Option("Course", "add_course(sess)"),
    Option("Section", "add_section(sess)"),
    Option("Major", "add_major(sess)"),
    Option("Student", "add_student(sess)"),
    Option("Student to Major", "add_student_major(sess)"),
    Option("Major to Student", "add_major_student(sess)"),
    Option("Student to Section", "add_student_section(sess)"),
    Option("Section to Student", "add_section_student(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "delete_department(sess)"),
    Option("Course", "delete_course(sess)"),
    Option("Section", "delete_section(sess)"),
    Option("Major", "delete_major(sess)"),
    Option("Student", "delete_student(sess)"),
    Option("Student to Major", "delete_student_major(sess)"),
    Option("Major to Student", "delete_major_student(sess)"),
    Option("Student to Section", "delete_student_section(sess)"),
    Option("Section to Student", "delete_section_student(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Department", "list_department(sess)"),
    Option("Course", "list_course(sess)"),
    Option("Major", "list_major(sess)"),
    Option("Student", "list_student(sess)"),
    Option("Student to Major", "list_student_major(sess)"),
    Option("Major to Student", "list_major_student(sess)"),
    Option("Student to Section", "list_student_section(sess)"),
    Option("Section to Student", "list_section_student(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])

# A menu to prompt for whether to create new tables or reuse the old ones.
introspection_select = Menu("introspection select", 'To introspect or not:', [
    Option('Start all over', START_OVER),
    Option("Reuse without introspection", REUSE_NO_INTROSPECTION)
])

enrollment_menu = Menu("enrollment menu", "Please indicate what you want to do:", [
    Option("Enroll (Student to Section)", "add_student_section(sess)"),
    Option("Enroll (Section to Student)", "add_section_student(sess)"),
    Option("Unenroll (Student to Section)", "delete_student_section(sess)"),
    Option("Unenroll (Section to Student)", "delete_section_student(sess)"),
    Option("List Enrollment (Student to Section)", "list_student_section(sess)"),
    Option("List Enrollment (Section to Student)", "list_section_student(sess)"),
    Option("Delete a Section", "delete_section(sess)"),
    Option("Delete a Student", "delete_student(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Back", "back"),
    Option("Exit this application", "pass")
])

department_select = Menu('department select', "Please select how you want to select a department:", [
    Option("Abbreviation", "abbreviation"),
    Option("Chair Name", "chair"),
    Option("Building and Office", "building/office"),
    Option("Description", "description")
])

section_select = Menu('section select', 'Please select how you want to select a section:', [
    Option("Building and Room", "building/room"),
    Option("Instructor", "instructor")
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Boilerplate Data", "boilerplate(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Rollback", "session_rollback(sess)"),
    Option("Back", "back"),
    Option("Exit this application", "pass")
])

select_menu = Menu('select', 'Please select what you wana do:', [
    Option("Add", add_menu),
    Option("List", list_menu),
    Option("Delete", delete_menu),
    Option("Enrollment (simplified)", enrollment_menu),
    Option("Boilerplate + Rollback", menu_main)
])
