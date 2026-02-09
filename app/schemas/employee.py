from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

class EmployeeBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    mobileNo: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    roles: List[str] = ["Employee"]

    # This allows Pydantic to read data even if it's an ORM object
    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str
    # employeeId: str

class EmployeeUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobileNo: Optional[str] = None
    centerId: Optional[int] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    roles: Optional[List[str]] = None

class EmployeeResponse(BaseModel):
    succeeded: bool
    message: Optional[str] = None
    data: Optional[EmployeeBase] = None