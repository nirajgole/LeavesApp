from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from app.db.base import Base

class LeaveRequest(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employeeId = Column(UNIQUEIDENTIFIER, ForeignKey("employees.employeeId"))

    leaveTypeId = Column(Integer)
    fromDate = Column(Date, nullable=False)
    toDate = Column(Date, nullable=True)
    leaveSession = Column(String(20), nullable=True)
    reason = Column(Text)
    status = Column(String(20), default="Pending")
    financialYearId = Column(Integer)

    # Secondary link to Employee table
    approvedBy = Column(UNIQUEIDENTIFIER, ForeignKey("employees.employeeId"), nullable=True)
    approvalComments = Column(String(255), nullable=True)

    # RELATIONSHIPS
    # We must explicitly tell SQLAlchemy which foreign_key belongs to which relationship
    employee = relationship(
        "Employee",
        back_populates="leaves",
        foreign_keys=[employeeId]
    )

    approver = relationship(
        "Employee",
        foreign_keys=[approvedBy]
    )