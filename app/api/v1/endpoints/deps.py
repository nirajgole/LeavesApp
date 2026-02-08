from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import TokenData
from app.api.v1.endpoints.auth import get_current_user

# Level 1: Anyone logged in
def is_authenticated(current_user: TokenData = Depends(get_current_user)):
    return current_user

# Level 2: Any HR Admin (can create employees)
def is_hr_admin(current_user: TokenData = Depends(get_current_user)):
    if "HR Admin" not in current_user.roles and "SuperAdmin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="HR Admin rights required")
    return current_user

# Level 3: ONLY the Super Admin (can delete users or change system settings)
def is_super_admin(current_user: TokenData = Depends(get_current_user)):
    if "SuperAdmin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Only the Super Admin can do this")
    return current_user

# Endpoint,Logic,Access Control
# Apply Leave,Depends(get_current_user),All authenticated employees
# Create Employee,Depends(get_current_admin),HR Admins and SuperAdmins only
# Approve Attendance,Depends(get_current_admin),HR Admins and SuperAdmins only
