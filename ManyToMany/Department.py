from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from typing import List  # Use this for the list of courses offered by the department
from constants import START_OVER, REUSE_NO_INTROSPECTION
from sqlalchemy import UniqueConstraint
from sqlalchemy import String, Integer


# Find out whether we're introspecting or recreating.
introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:            # Define the entity from scratch

    class Department(Base):
        """An organization within a particular college within a university.  Each
        department offers one or more major fields of study to its students, and
        within each major, some number of courses.  Each course is offered on
        a regular basis as a scheduled section of a given course.

        Note, this is just a shell of the Department class.  There are additional
        columns needed, but this is enough to demonstrate one-to-many relationships."""
        __tablename__ = "departments"  # Give SQLAlchemy th name of the table.
        name: Mapped[str] = mapped_column("name", String(50), nullable=False, primary_key=True)
        abbreviation: Mapped[str] = mapped_column("abbreviation", String(10), nullable=False)
        chairName: Mapped[str] = mapped_column("chair_name", String(80), nullable=False)
        building: Mapped[str] = mapped_column("building", String(10), nullable=False)
        office: Mapped[int] = mapped_column("office", Integer, nullable=False)
        description: Mapped[str] = mapped_column("description", String(80), nullable=False)
        courses: Mapped[List["Course"]] = relationship(back_populates="department")
        majors: Mapped[List["Major"]] = relationship(back_populates="department")
        __table_args__ = (UniqueConstraint("abbreviation", name="departments_uk_01"),
                            UniqueConstraint("chair_name", name="departments_uk_02"),
                            UniqueConstraint("building", "office", name="departments_uk_03"),
                            UniqueConstraint("description", name="departments_uk_04"))


        def __init__(self, name: str, abbreviation: str, chair: str, building: str, office: int, description: str):
            self.name = name
            self.abbreviation = abbreviation
            self.chairName = chair
            self.building = building
            self.office = office
            self.description = description

        def add_course(self, course):
            if course not in self.courses:
                self.courses.add(course)  # I believe this will update the course as well.


        def remove_course(self, course):
            if course in self.courses:
                self.courses.remove(course)


        def get_courses(self):
            return self.courses


        def add_major(self, major):
            if major not in self.majors:
                self.majors.add(major)


        def remove_major(self, major):
            if major in self.majors:
                self.majors.remove(major)


        def get_majors(self):
            return self.majors

    def __str__(self):
        return (f"Department: {self.name} / {self.abbreviation}\n{self.description}\n"
                f"The chair, {self.chairName} is located at {self.building} {self.office} number course offered: {len(self.courses)}")

