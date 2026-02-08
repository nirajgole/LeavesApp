from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.db.session import get_db
from app.models.employee import Employee
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.auth import ApiResponse, LoginRequest, TokenData
from app.schemas.employee import EmployeeCreate
from app.core.config import settings
from app.crud.crud_employee import employee_crud

# Define where the token is extracted from (the Login URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/Account/authenticate")

router = APIRouter()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Employee:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")  #
        uid: str = payload.get("uid")  #
        roles: list = payload.get("roles", [])  #

        if email is None or uid is None:
            raise credentials_exception

        token_data = TokenData(email=email, uid=uid, roles=roles)
    except JWTError:
        raise credentials_exception

    user = db.query(Employee).filter(Employee.employeeId == int(token_data.uid)).first()
    if user is None:
        raise credentials_exception

    # We attach the roles from the token to the user object temporarily
    # so downstream routes can check them without another DB query.
    user.current_roles = token_data.roles
    return user


def get_current_admin(current_user: Employee = Depends(get_current_user)) -> Employee:
    """
    Ensures the authenticated user has HR Admin or SuperAdmin roles.
    """
    admin_roles = {"SuperAdmin"}
    user_roles = set(getattr(current_user, "current_roles", []))

    if not admin_roles.intersection(user_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Control: Only SuperAdmins are allowed",
        )
    return current_user


@router.post("/authenticate", response_model=ApiResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # 1. Look up user by email
    user = db.query(Employee).filter(Employee.email == login_data.email).first()
    print(f"Login attempt for email: {login_data}, User found: {user }")

    # 2. Verify password
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # 3. Create the token payload (claims) as per documentation
    token_data = {
        "email": user.email,
        "uid": str(user.employeeId),
        "roles": user.roles,  # List of roles: ["HR Admin", "Employee"]
    }

    jwt_token = create_access_token(email=user.email, uid=str(user.employeeId), roles=user.roles)

    response_data = TokenData(
        jwToken=jwt_token,  # Generated via Secret Key
        email=user.email,  # From Model
        userName=f"{user.firstName} {user.lastName}",  # Combined from Model fields
        roles=user.roles,  # From Model (JSON field)
        isVerified=True,
        uid=str(user.employeeId)
    )

    return ApiResponse(data=response_data.model_dump(), succeeded=True)


@router.post("/super-admin/setup", response_model=ApiResponse)
def admin_signup(payload: EmployeeCreate, db: Session = Depends(get_db)):
    # 1. Check if ANY SuperAdmin already exists
    # We can use a raw query or add a specific method to CRUD
    existing_super = db.query(Employee).filter(Employee.roles.contains(["SuperAdmin"])).first()
    if existing_super:
        raise HTTPException(status_code=403, detail="Super Admin already initialized")

    # 2. Use the CRUD class to create
    employee_crud.create_super_admin(db=db, obj_in=payload)

    return ApiResponse(succeeded=True, message="Super Admin created successfully")
