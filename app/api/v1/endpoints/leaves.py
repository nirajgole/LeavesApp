from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.crud_leave import crud_leave
from app.api.v1.endpoints.deps import get_current_user
from app.models.employee import Employee
from app.schemas.leave import (
    LeaveCreate,
    HalfDayLeaveCreate,
    LeaveApproval,
    LeaveSummaryResponse,
)

router = APIRouter()


# 3.2.1 Apply Full-Day Leave
# Accessible to all authenticated employees [cite: 134]
@router.post("/LeaveDetails", response_model=dict)
def apply_full_day_leave(
    leave_in: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    # Ensure users can only apply for themselves unless they are HR/Admin
    if leave_in.employeeId != current_user.employeeId:
        raise HTTPException(
            status_code=403, detail="You can only apply leave for yourself"
        )

    leave = crud_leave.create_full_day_leave(db, obj_in=leave_in)
    return {
        "data": {
            "hrEmployeeFullDayLeaveDetailsId": leave.id,
            "status": leave.status,
            "message": "Leave request submitted successfully",
        },
        "succeeded": True,
    }


# 3.2.5 Apply Half-Day Leave
# Accessible to all authenticated employees [cite: 134, 167]
@router.post("/HalfDayLeaveDetails", response_model=dict)
def apply_half_day_leave(
    leave_in: HalfDayLeaveCreate,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    if leave_in.employeeId != current_user.employeeId:
        raise HTTPException(
            status_code=403, detail="You can only apply leave for yourself"
        )

    leave = crud_leave.create_half_day_leave(db, obj_in=leave_in)
    return {
        "data": {
            "hrEmployeeHalfDayLeaveDetailsId": leave.id,
            "status": leave.status,
            "message": "Half-day leave request submitted successfully",
        },
        "succeeded": True,
    }


# 3.2.3 Approve Leave Request
# Access Control: Reporting officers and HR admins only
@router.post("/LeaveDetails/approve", response_model=dict)
def approve_leave(
    approval_in: LeaveApproval,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    # Business Logic: Check if current_user is the reporting officer or an Admin
    # This assumes 'roles' is a field in your Employee model
    is_admin = "Admin" in getattr(current_user, "roles", [])
    if approval_in.approvedBy != current_user.employeeId and not is_admin:
        raise HTTPException(
            status_code=403, detail="Unauthorized to approve this request"
        )

    leave = crud_leave.approve_or_reject_leave(db, obj_in=approval_in)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return {
        "data": {
            "message": f"Leave request {'approved' if approval_in.isApproved else 'rejected'} successfully"
        },
        "succeeded": True,
    }


# 3.2.6 Get Leave Summary
# Access Control: Employees view own, Managers view team [cite: 75, 177]
@router.get(
    "/LeaveAccounts/GetLeaveSummarybyEmployeeId/{HREmployeeId}",
    response_model=LeaveSummaryResponse,
)
def get_leave_summary(
    HREmployeeId: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    # Check permissions [cite: 75]
    is_own_profile = HREmployeeId == current_user.employeeId
    # Logic for manager check could be added here

    if not is_own_profile:
        # Simplified check: only allow own summary for now unless Admin
        if "Admin" not in getattr(current_user, "roles", []):
            raise HTTPException(
                status_code=403, detail="Access denied to other employee summaries"
            )

    summary = crud_leave.get_leave_summary(db, employee_id=HREmployeeId)
    return {"data": summary, "succeeded": True}

    # 3.2.8 Get Leave Requests by Reporting Officer


# Access Control: Reporting Officer only [cite: 187, 193]
@router.get(
    "/LeaveDetails/GetByReportingOfficerId/{ReportingOfficerId}", response_model=dict
)
def get_manager_pending_leaves(
    ReportingOfficerId: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    # Ensure the manager is viewing their own team [cite: 193]
    if ReportingOfficerId != current_user.employeeId:
        raise HTTPException(
            status_code=403, detail="Unauthorized to view this manager's team"
        )

    requests = crud_leave.get_pending_by_manager(db, manager_id=ReportingOfficerId)
    return {"data": requests, "succeeded": True}


# Cancel Leave Request (New Functionality)
# Access Control: Employee can cancel their own 'Pending' leaves [cite: 134]
@router.delete("/LeaveDetails/Cancel/{LeaveId}", response_model=dict)
def cancel_leave_request(
    LeaveId: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    leave = crud_leave.cancel_leave(
        db, leave_id=LeaveId, employee_id=current_user.employeeId
    )
    if not leave:
        raise HTTPException(
            status_code=400,
            detail="Leave request not found or cannot be cancelled (already processed)",
        )
    return {
        "data": {"message": "Leave request cancelled successfully"},
        "succeeded": True,
    }
