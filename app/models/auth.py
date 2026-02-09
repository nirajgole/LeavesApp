# from pydantic import BaseModel, EmailStr
# from typing import List, Optional

# # Data received from the user during login
# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# # Detailed data inside the token response
# class TokenDataResponse(BaseModel):
#     accessToken: str
#     email: str
#     userName: str
#     roles: List[str]
#     isVerified: bool

# # The top-level response wrapper
# class TokenResponse(BaseModel):
#     data: TokenDataResponse
#     succeeded: bool
#     message: Optional[str] = None
#     errors: Optional[List[str]] = None