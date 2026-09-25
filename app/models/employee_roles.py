from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class EmployeeRole(Base):
    __tablename__ = "employee_roles"
    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    branch_id = Column(Integer, ForeignKey("branches.id"))

    role = relationship("Role", back_populates="employee_roles")
    employee = relationship("Employees", back_populates="employee_roles")


