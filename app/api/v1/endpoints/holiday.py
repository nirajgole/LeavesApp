from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.holiday import Holiday
from app.models.employee import Employee

router = APIRouter()

# 3.8.1 Get All Holidays [cite: 389]
@router.get("/hrholiday/GetAll", response_model=dict)
def get_all_holidays(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user) #
):
    """Get list of all holidays in the system[cite: 394]."""
    holidays = db.query(Holiday).filter(Holiday.isActive == True).all()
    return {
        "data": holidays,
        "succeeded": True
    }

# 3.8.2 Get Upcoming Holidays by Employee [cite: 397]
@router.get("/Employee/GetUpComingHoliday/{id}", response_model=dict)
def get_upcoming_holidays(
    id: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Returns upcoming holidays applicable to the employee based on center/state[cite: 402, 403]."""
    # Fetch holidays occurring today or in the future
    today = datetime.now().date()

    # Logic to filter holidays by the employee's centerId or National holidays
    upcoming = db.query(Holiday).filter(
        Holiday.holidayDate >= today,
        Holiday.isActive == True,
        (Holiday.centerId == current_user.centerId) | (Holiday.holidayType == "National")
    ).order_by(Holiday.holidayDate).all()

    return {
        "data": upcoming,
        "succeeded": True
    }