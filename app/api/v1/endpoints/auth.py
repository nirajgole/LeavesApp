from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.db.session import get_db
from app.models.employee import Employee
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.auth import ApiResponse, LoginRequest, TokenData
from app.schemas.employee import EmployeeCreate
from app.core.config import settings
from app.crud.crud_employee import employee_crud

# Define where the token is extracted from (the Login URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1.0/Account/login")

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
        email = payload.get("email")
        uid = payload.get("uid")
        roles = payload.get("roles", [])

        print("gcu: payload:", payload)  # Debugging line to check the decoded token
        print("gcu: email:", email)  # Debugging line to check the email claim
        print("gcu: uid:", uid)  # Debugging line to check the uid claim

        if (email is None) or (uid is None):
            raise credentials_exception

        token_data = TokenData(email=email, uid=uid, roles=roles)
        print(
            "gcu: token_data:", token_data
        )  # Debugging line to check the TokenData object
    except JWTError as exc:
        raise credentials_exception from exc

    user = db.query(Employee).filter(Employee.employeeId == token_data.uid).first()
    print(
        "gcu: user from DB:", user
    )  # Debugging line to check the user fetched from DB
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


@router.post("/login")
def login(
    # Use OAuth2PasswordRequestForm to support the Swagger "Authorize" box
    # It will extract 'username' (email) and 'password' from the form data
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # 1. Look up user by email (OAuth2 uses 'username' field for the email)
    user = db.query(Employee).filter(Employee.email == form_data.username).first()

    # 2. Verify password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # 3. Create Token Payload
    token_payload = {
        "email": user.email,  # 'sub' is the standard JWT field for subject
        "uid": str(user.employeeId),
        "roles": user.roles,
    }

    access_token = create_access_token(**token_payload)

    # 4. Prepare Response
    # To satisfy Swagger's "Authorize" button, the response MUST include
    # 'access_token' and 'token_type' at the top level or in the 'data' if you handle it manually.
    # response_data = TokenData(
    #     access_token=access_token, # Swagger looks for this exact name
    #     token_type="bearer",       # And this
    #     email=user.email,
    #     userName=f"{user.firstName} {user.lastName}",
    #     roles=user.roles,
    #     isVerified=True,
    #     uid=str(user.employeeId)
    # )

    # return ApiResponse(data=response_data.model_dump(), succeeded=True)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "succeeded": True,
        "data": {
            "access_token": access_token,
            "email": user.email,
            "userName": f"{user.firstName} {user.lastName}",
            "roles": user.roles,
            "uid": str(user.employeeId),
        },
    }


@router.post("/superAdmin/setup", response_model=ApiResponse)
def admin_signup(payload: EmployeeCreate, db: Session = Depends(get_db)):
    # 1. Check if ANY SuperAdmin already exists
    # We can use a raw query or add a specific method to CRUD
    existing_super = (
        db.query(Employee).filter(Employee.roles.contains(["SuperAdmin"])).first()
    )
    if existing_super:
        raise HTTPException(status_code=403, detail="Super Admin already initialized")

    # 2. Use the CRUD class to create
    employee_crud.create_super_admin(db=db, obj_in=payload)

    return ApiResponse(succeeded=True, message="Super Admin created successfully")
