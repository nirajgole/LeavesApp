from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class HolidayBase(BaseModel):
    hrholidayId: int
    holidayName: str
    holidayDate: date
    holidayType: str
    isActive: bool

class HolidayResponse(BaseModel):
    data: List[HolidayBase]
    succeeded: bool