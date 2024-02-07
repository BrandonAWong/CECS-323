from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Department(Base):
    """A section of a the university which deals with the study of 
	a particular subject. Several different programs and degrees are offered
	regarding the subject. An examlpe would be the Department of Finance from
	the College of Business (COB) from California State University Long Beach."""
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column("name", String(50), nullable=False, primary_key=True)
    abbreviation: Mapped[str] = mapped_column("abbreviation", String(6), nullable=False)
    chairName: Mapped[str] = mapped_column("chair_name", String(80), nullable=False)
    building: Mapped[str] = mapped_column("building", String(10), nullable=False)
    office: Mapped[int] = mapped_column("office", Integer, nullable=False)
    description: Mapped[str] = mapped_column("description", String(80), nullable=False)

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

    def __str__(self):
        return f"Department: {self.name} / {self.abbreviation}\n{self.description}\n"
               f"The chair, {self.chairName} is located at {self.building} {self.office}"

