from datetime import datetime, timedelta, timezone
from typing import Any, Union, List
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import uuid

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    email: str,
    uid: str,
    roles: List[str],
    ip_address: str = "0.0.0.0"
) -> str:
    """
    Generates a JWT token with claims defined in API Documentation
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Claims mapping based on documentation table
    to_encode = {
        "exp": expire,
        "email": email,             # User email
        "uid": uid,                 # User ID (GUID)
        "roles": roles,             # List of roles
        "ip": ip_address,           # IP address
        "jti": str(uuid.uuid4())    # Unique token identifier
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)