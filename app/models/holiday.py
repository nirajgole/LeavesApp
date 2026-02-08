from sqlalchemy import Column, Integer, String, Date, Boolean
from app.db.base import Base


class Holiday(Base):
    __tablename__ = "holidays"

    hrholidayId = Column(Integer, primary_key=True, index=True)  #
    holidayName = Column(String(100), nullable=False)  #
    holidayDate = Column(Date, nullable=False)  #
    holidayType = Column(String(50))  # e.g., National, State, Center-Specific
    isActive = Column(Boolean, default=True)  #
    # Fields to handle center-specific holidays
    centerId = Column(Integer, nullable=True)  # [cite: 9]
    stateId = Column(Integer, nullable=True)  # [cite: 54]
