from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(40), nullable=False, unique=True)
    name = Column(String(80), nullable=False)
    is_system = Column(Boolean, nullable=False, default=False)

    employee_roles = relationship("EmployeeRole", back_populates="role")