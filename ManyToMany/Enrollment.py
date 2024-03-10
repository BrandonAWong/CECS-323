from orm_base import Base
from sqlalchemy import Integer, String, ForeignKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from IntrospectionFactory import IntrospectionFactory
from constants import START_OVER, REUSE_NO_INTROSPECTION

introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    class Enrollment(Base):
        __tablename__ = "enrollments"
        section: Mapped["Section"] = relationship(back_populates="students")
        departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation',
                                                  String(10), nullable=False, primary_key=True)
        courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                  nullable=False, primary_key=True)
        sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                                  nullable=False, primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), 
                                                  nullable=False, primary_key=True)
        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                  primary_key=True) 
        student: Mapped["Student"] = relationship(back_populates="majors")
        studentId: Mapped[int] = mapped_column('student_id', ForeignKey("students.student_id"), primary_key=True)

        __table_args__ = (ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionNumber],
                                               ["Section.departmentAbbreviation", "Section.courseNumber", "Section.sectionNumber"],
                                              name="enrollments_sections_fk_01"),
                          UniqueConstraint("department_abbreviation", "course_number", "section_year", "semester", "student_id", name="enrollments_uk_01"))

        def __init__(self, section, student):
            self.section = section
            self.departmentAbbreviation = section.departmentAbbreviation
            self.courseNumber = section.courseNumber
            self.sectionNumber = section.sectionNumber
            self.semester = section.semester
            self.sectionYear = section.sectionYear
            self.student = student
            self.studentId = student.studentID


        def __str__(self):
            return f"Enrollment: {self.student} ({self.studentId}) is enrolled in {self.section}"

