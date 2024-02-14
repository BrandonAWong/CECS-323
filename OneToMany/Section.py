from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from Department import Department
from Course import Course 
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES

introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    class Section(Base):
        """DEFINTION"""
        __tablename__ = "sections"

        course: Mapped["Course"] = relationship(back_populates="sections")

        departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation',
                                                  String(10), primary_key=True)
        courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                  nullable=False, primary_key=True)
        sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                                  primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), nullable=False,
                                                  primary_key=True)
        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                  primary_key=True)
        building: Mapped[str] = mapped_column('building', String(6), nullable=False)
        room: Mapped[int] = mapped_column('room', Integer, nullable=False)
        schedule: Mapped[str] = mapped_column('schedule', String(6))
        startTime: Mapped[Time] = mapped_column('start_time', Time)
        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        __table_args__ = (UniqueConstraint("year", "semester", "schedule", "start_time", 
                                           "building", "room", name="sections_uk_01"),
                          UniqueConstraint("year", "semester", "schedule", "start_time", 
                                           "instructor", name="sections_uk_02"),
                          ForeignKeyConstraint([departmentAbbreviation],
                                               [Department.abbreviation]),
                          ForeignKeyConstraint([courseNumber], [Course.courseNumber]))

elif introspection_type == INTROSPECT_TABLES:
    class Section(Base):
        __table__ = Table("sections", Base.metadata, autoload_with=engine)
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        courseNumber: Mapped[int] = column_property(__table__.c.course_number)
        course: Mapped["Course"] = relationship(back_populates="sections")

def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int,
             building: str, room: int, schedule: str, startTime: Time, instructor: str):
    self.departmentAbbreviation = course.departmentAbbreviation
    self.course = course
    self.courseNumber = course.courseNumber
    self.sectionNumber = sectionNumber
    self.semester =  semester
    self.sectionYear = sectionYear
    self.building = building
    self.room = room
    self.schedule = schedule
    self.startTime = startTime
    self.instructor = instructor


def __str__(self):
    return (f"Course number: {self.courseNumber} Course name: {self.name} units: {self.units}\n"
            f"Section number: {self.sectionNumber} Semester: {self.semester} Section year: {self.sectionYear}\n"
            f"Instructor: {self.instructor} Schedule: {self.schedule} Start time: {self.startTime}\n"
            f"Building: {self.building} Room: {self.room}")

setattr(Section, '__init__', __init__)
setattr(Section, '__str__', __str__)
