from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Department(Base):
    """Description: (incomplete)"""

    __tablename__ = "departments"
    departmentName: Mapped[str] = mapped_column('name', String(50), nullable=False, primary_key=True)
    abbreviation: Mapped[str] = mapped_column('abbreviation', String(6), nullable=False)
    chairName: Mapped[str] = mapped_column('chair_name', String(80), nullable=False)
    building: Mapped[str] = mapped_column('building', String(10), nullable=False)
    officeNum: Mapped[int] = mapped_column('office', Integer, nullable=False)
    description: Mapped[str] = mapped_column('description', String(80), nullable=False)

    __table_args__ = (UniqueConstraint("abbreviation", name = "departments_uk_01"),UniqueConstraint("chair_name", name = "departments_uk_02"
UniqueConstraint("building","office", name = "departmants_uk_03"), UniqueConstraint("description", name = "departments_uk_04"))

    def __init__(self, department_name: str, abbr: str, chair_name: str, building: str, office: int, description: str):
        self.departmentName = department_name
        self.abbreviation = abbr
        self.chairName = chair_name
        self.building = building
        self.officeNum = office
        self.description = description

    def __str__(self):
        return ""

