from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


# Base properties shared across schemas
class LeaveBase(BaseModel):
    employeeId: int
    leaveTypeId: int
    reason: str


# Schema for submitting a Full-Day Leave
class LeaveCreate(LeaveBase):
    fromDate: date
    toDate: date
    financialYearId: int


# Schema for submitting a Half-Day Leave
class HalfDayLeaveCreate(LeaveBase):
    leaveDate: date
    leaveSession: str = Field(..., pattern="^(FirstHalf|SecondHalf)$")


# Schema for Manager/HR Approval
class LeaveApproval(BaseModel):
    hrEmployeeFullDayLeaveDetailsId: int
    approvedBy: int
    approvalComments: str
    isApproved: bool


# Schema for the Leave Summary response [cite: 175, 176]
class LeaveTypeBreakdown(BaseModel):
    leaveType: str
    total: int
    used: int
    available: int


class LeaveSummaryData(BaseModel):
    totalLeaves: int
    usedLeaves: int
    pendingLeaves: int
    availableLeaves: int
    leaveTypeBreakdown: List[LeaveTypeBreakdown]


class LeaveSummaryResponse(BaseModel):
    data: LeaveSummaryData
    succeeded: bool = True
