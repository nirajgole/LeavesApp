from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.api.v1.endpoints.deps import get_current_user
from app.models.employee import Employee
from app.models.leave import LeaveRequest

# Note: In a full system, you would also import WFH, TravelClaim, and Candidate models
# from app.models.attendance import WebAttendance
from datetime import datetime

router = APIRouter()


# 3.9.1 Get HR Dashboard Overall Status [cite: 406]
@router.get("/overallstatus", response_model=dict)
def get_overall_status(
    db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)
):
    """Get high-level HR metrics for dashboard display."""
    # Access Control: HR Admins and Managers only

    today = datetime.now().date()

    # 1. Employee Stats
    total_employees = db.query(Employee).count()
    active_employees = (
        db.query(Employee).filter(Employee.onBordingStatus == "Completed").count()
    )

    # 2. Leave Stats
    on_leave_today = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.status == "Approved",
            LeaveRequest.fromDate <= today,
            LeaveRequest.toDate >= today,
        )
        .count()
    )

    pending_leaves = (
        db.query(LeaveRequest).filter(LeaveRequest.status == "Pending").count()
    )

    # 3. Attendance Logic (Simplified)
    # For a real implementation, you would query WFH, Travel, and Recruitment tables here

    return {
        "data": {
            "totalEmployees": total_employees,  #
            "activeEmployees": active_employees,  #
            "onLeaveToday": on_leave_today,  #
            "pendingLeaveRequests": pending_leaves,  #
            "pendingWFHRequests": 10,  # Placeholder for WFH module logic
            "pendingTravelClaims": 8,  # Placeholder for Travel module logic
            "newApplications": 5,  # Placeholder for Recruitment module logic
            "pendingOnboarding": 3,  # Placeholder
        },
        "succeeded": True,
    }


# 3.9.2 Get HR Dashboard Summary [cite: 413, 414]
@router.get("/summary", response_model=dict)
def get_dashboard_summary(
    db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)
):
    """Get detailed HR analytics including trends and statistics[cite: 418]."""
    # Access Control: HR Admins and SuperAdmins only

    # Example: Distribution by Department
    dept_stats = (
        db.query(Employee.department, func.count(Employee.employeeId))
        .group_by(Employee.department)
        .all()
    )

    return {
        "data": {
            "departmentDistribution": {dept: count for dept, count in dept_stats},
            "message": "Comprehensive analytics retrieved",
        },
        "succeeded": True,
    }
