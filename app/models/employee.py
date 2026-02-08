from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Employee(Base):
    __tablename__ = "employees"

    employeeId = Column(Integer, primary_key=True, index=True)
    employeeCode = Column(String(50), unique=True, index=True)

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    firstName = Column(String(100))
    lastName = Column(String(100))
    mobileNo = Column(String(20))

    centerId = Column(Integer)
    department = Column(String(100))
    designation = Column(String(100))
    onBoardingStatus = Column(String(50), default="Pending")

    # roles must exist in the DB to store ["Admin"] or ["Employee"]
    roles = Column(JSON, default=["Employee"])

    reportingOfficerId = Column(
        Integer, ForeignKey("employees.employeeId"), nullable=True
    )

    leaves = relationship(
        "LeaveRequest",
        back_populates="employee",
        foreign_keys="[LeaveRequest.employeeId]" # <--- CRITICAL FIX
    )