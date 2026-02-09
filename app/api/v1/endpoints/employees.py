from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.crud_employee import employee_crud
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.auth import ApiResponse
from app.api.v1.endpoints.auth import get_current_user, get_current_admin
from app.models.employee import Employee

router = APIRouter()

@router.post("/CreateEmployee", response_model=ApiResponse)
def create_new_employee(
    *,
    db: Session = Depends(get_db),
    employee_in: EmployeeCreate,
    current_admin: Employee = Depends(get_current_admin)
):
    """Admin-only: Create a new employee."""
    user = employee_crud.get_by_email(db, email=employee_in.email)
    
    if user:
        raise HTTPException(
            status_code=400,
            detail="An employee with this email already exists."
        )

    new_employee = employee_crud.create_employee(db=db, obj_in=employee_in)

    return ApiResponse(
        succeeded=True,
        message=f"Employee {new_employee.firstName} created successfully.",
        data={"employeeId": new_employee.employeeId}
    )


@router.put("/UpdateEmployeeBasic/{employeeId}", response_model=ApiResponse)
def update_employee(
    employeeId: int,
    employee_in: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
):
    """
    Update profile:
    - Employees can update their own data.
    - HR Admins/SuperAdmins can update anyone's data.
    """
    # Permission logic
    is_own_profile = employeeId == current_user.employeeId
    is_admin = any(role in ["HR Admin", "SuperAdmin"] for role in current_user.roles)

    if not (is_own_profile or is_admin):
        raise HTTPException(
            status_code=403, detail="Unauthorized to update this profile"
        )

    # Fetch the employee record first
    db_obj = employee_crud.get_by_id(db, emp_id=employeeId)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Use a standard update method in your CRUD class
    updated_user = employee_crud.update(db, db_obj=db_obj, obj_in=employee_in)

    return ApiResponse(succeeded=True, data=updated_user)


@router.delete("/DeactivateEmployee/{employeeId}", response_model=ApiResponse)
def deactivate_employee(
    employeeId: int,
    db: Session = Depends(get_db),
    current_admin: Employee = Depends(get_current_admin),
):
    """Admin-only: Deactivate an employee account."""
    db_obj = employee_crud.get_by_id(db, emp_id=employeeId)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Logic to set isActive = False instead of deleting
    deactivated_user = employee_crud.deactivate(db, db_obj=db_obj)

    return ApiResponse(
        succeeded=True,
        message="Employee deactivated successfully"
    )