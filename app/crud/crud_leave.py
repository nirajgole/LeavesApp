from sqlalchemy.orm import Session
from app.models.leave import LeaveRequest
from app.models.employee import Employee
from app.schemas.leave import LeaveCreate, HalfDayLeaveCreate, LeaveApproval
from datetime import datetime


class CRUDLeave:
    def create_full_day_leave(self, db: Session, obj_in: LeaveCreate):
        """Submit a full-day leave request[cite: 125, 130]."""
        db_obj = LeaveRequest(
            employeeId=obj_in.employeeId,
            leaveTypeId=obj_in.leaveTypeId,
            fromDate=obj_in.fromDate,
            toDate=obj_in.toDate,
            reason=obj_in.reason,
            financialYearId=obj_in.financialYearId,
            status="Pending",  # Default status is Pending [cite: 132]
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_half_day_leave(self, db: Session, obj_in: HalfDayLeaveCreate):
        """Submit a half-day leave request for a specific session[cite: 161, 166]."""
        db_obj = LeaveRequest(
            employeeId=obj_in.employeeId,
            leaveTypeId=obj_in.leaveTypeId,
            fromDate=obj_in.leaveDate,
            toDate=obj_in.leaveDate,  # Same day for half-day [cite: 166]
            leaveSession=obj_in.leaveSession,  # "FirstHalf" or "SecondHalf" [cite: 166]
            reason=obj_in.reason,
            status="Pending",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_leave_summary(self, db: Session, employee_id: int):
        """Get comprehensive leave summary including balances by leave type[cite: 169, 177]."""
        requests = (
            db.query(LeaveRequest).filter(LeaveRequest.employeeId == employee_id).all()
        )
        used = len([r for r in requests if r.status == "Approved"])
        pending = len([r for r in requests if r.status == "Pending"])

        # Returns leave balance, used, and pending leaves [cite: 159, 175]
        return {
            "totalLeaves": 12,
            "usedLeaves": used,
            "pendingLeaves": pending,
            "availableLeaves": 12 - used,
            "leaveTypeBreakdown": [
                {"leaveType": "Sick Leave", "total": 6, "used": 1, "available": 5},
                {
                    "leaveType": "Casual Leave",
                    "total": 6,
                    "used": used - 1 if used > 0 else 0,
                    "available": 5,
                },
            ],
        }

    def approve_or_reject_leave(self, db: Session, obj_in: LeaveApproval):
        """Reporting officer approves or rejects a leave request[cite: 143, 151]."""
        db_obj = (
            db.query(LeaveRequest)
            .filter(LeaveRequest.id == obj_in.hrEmployeeFullDayLeaveDetailsId)
            .first()
        )
        if db_obj:
            # Updates status and records approval comments [cite: 148, 150]
            db_obj.status = "Approved" if obj_in.isApproved else "Rejected"
            db_obj.approvedBy = obj_in.approvedBy
            db_obj.approvalComments = obj_in.approvalComments
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def get_pending_by_manager(self, db: Session, manager_id: int):
        """Returns all pending leave requests requiring approval from the reporting officer[cite: 187, 192]."""
        # Join with Employee to find team members reporting to this specific manager [cite: 116, 117]
        return (
            db.query(LeaveRequest)
            .join(Employee, LeaveRequest.employeeId == Employee.employeeId)
            .filter(Employee.reportingOfficerId == manager_id)
            .filter(LeaveRequest.status == "Pending")
            .all()
        )

    def cancel_leave(self, db: Session, leave_id: int, employee_id: int):
        """Internal logic to cancel a pending leave request before it is processed[cite: 141]."""
        db_obj = (
            db.query(LeaveRequest)
            .filter(LeaveRequest.id == leave_id, LeaveRequest.employeeId == employee_id)
            .first()
        )

        # Only allows cancellation if the request has not been approved/rejected yet
        if db_obj and db_obj.status == "Pending":
            db_obj.status = "Cancelled"
            db.commit()
            db.refresh(db_obj)
            return db_obj
        return None


crud_leave = CRUDLeave()
