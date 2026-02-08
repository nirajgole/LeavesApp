from pydantic import BaseModel, EmailStr
from typing import Optional, List

class TokenData(BaseModel):
    """
    Unified Schema for JWT payload and Response data.
    Removed 'TokenDataResponse' and merged it here.
    """
    email: EmailStr
    uid: Optional[str] = None
    roles: List[str] = []
    # These fields are used for the API response specifically
    jwToken: Optional[str] = None
    userName: Optional[str] = None
    isVerified: bool = False

class LoginRequest(BaseModel):
    """The data expected from the login form."""
    email: EmailStr
    password: str

# --- GENERIC API WRAPPERS ---
class ApiResponse(BaseModel):
    """
    Standard API wrapper. Instead of creating 'EmployeeResponse'
    and 'TokenResponse', we use this generic format.
    """
    succeeded: bool
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    data: Optional[dict] = None # Can hold TokenData, EmployeeBase, etc.