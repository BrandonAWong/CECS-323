from sqlalchemy import UniqueConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List  # Use this for the list of courses offered by the department

"""This is the guts of the department class that needs to be defined
regardless whether we introspect or not."""
__tablename__ = "departments"  # Give SQLAlchemy th name of the table.
name: Mapped[str] = mapped_column("name", String(50), nullable=False, primary_key=True)
abbreviation: Mapped[str] = mapped_column("abbreviation", String(10), nullable=False)
chairName: Mapped[str] = mapped_column("chair_name", String(80), nullable=False)
building: Mapped[str] = mapped_column("building", String(10), nullable=False)
office: Mapped[int] = mapped_column("office", Integer, nullable=False)
description: Mapped[str] = mapped_column("description", String(80), nullable=False)
courses: Mapped[List["Course"]] = relationship(back_populates="department")
# __table_args__ can best be viewed as directives that we ask SQLAlchemy to
# send to the database.  In this case, that we want two separate uniqueness
# constraints (candidate keys).
__table_args__ = (UniqueConstraint("abbreviation", name="departments_uk_01"),
                    UniqueConstraint("chair_name", name="departments_uk_02"),
                    UniqueConstraint("building", "office", name="departments_uk_03"),
                    UniqueConstraint("description", name="departments_uk_04"))


def add_course(self, course):
    if course not in self.courses:
        self.courses.add(course)  # I believe this will update the course as well.


def remove_course(self, course):
    if course in self.courses:
        self.courses.remove(course)


def get_courses(self):
    return self.courses


def __str__(self):
    return (f"Department: {self.name} / {self.abbreviation}\n{self.description}\n"
            f"The chair, {self.chairName} is located at {self.building} {self.office}number course offered: {len(self.courses)}")
