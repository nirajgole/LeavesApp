from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.core.security import get_password_hash

class CRUDEmployee:
    def get_by_email(self, db: Session, email: str):
        """Find an employee by their email address."""
        return db.query(Employee).filter(Employee.email == email).first()

    def get_by_id(self, db: Session, emp_id: int):
        """Find an employee by their primary ID."""
        return db.query(Employee).filter(Employee.employeeId == emp_id).first()

    def create_super_admin(self, db: Session, obj_in: EmployeeCreate):
        """Initializes the one-time Super Admin."""
        print(obj_in)
        db_obj = Employee(
            **obj_in.model_dump(exclude={"password"}),
            hashed_password=get_password_hash(obj_in.password),
            # roles=["SuperAdmin"],
            onBoardingStatus="Completed"
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_employee(self, db: Session, obj_in: EmployeeCreate):
        """Admin creates a standard employee or HR Admin."""
        db_obj = Employee(
            **obj_in.model_dump(exclude={"password"}),
            hashed_password=get_password_hash(obj_in.password),
            onBordingStatus="Pending" # Employees must change password later
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_roles(self, db: Session, db_obj: Employee, roles: list):
        """Update roles for an existing employee."""
        db_obj.roles = roles
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Employee, obj_in: EmployeeUpdate):
        """Dynamically update employee fields."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deactivate(self, db: Session, db_obj: Employee):
        """Soft delete: change status to Inactive."""
        db_obj.onBordingStatus = "Inactive"
        db_obj.isActive = False
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Instantiate the class for use in routes
employee_crud = CRUDEmployee()