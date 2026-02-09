from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Generic, Optional, List, TypeVar
T = TypeVar("T")

class TokenData(BaseModel):
    """
    Unified Schema for JWT payload and Response data.
    Removed 'TokenDataResponse' and merged it here.
    """
    accessToken: Optional[str] = None
    token_type: str = "Bearer"
    email: str
    uid: str
    roles: List[str] = []
    # These fields are used for the API response specifically
    userName: Optional[str] = None
    isVerified: Optional[bool] = False

class LoginRequest(BaseModel):
    """The data expected from the login form."""
    email: EmailStr
    password: str

# --- GENERIC API WRAPPERS ---
class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API wrapper. Instead of creating 'EmployeeResponse'
    and 'TokenResponse', we use this generic format.
    """
    succeeded: bool
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    data: Optional[T] = None # Can hold TokenData, EmployeeBase, etc.