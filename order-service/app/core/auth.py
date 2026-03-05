from fastapi import Depends, HTTPException, status, Header
from typing import Annotated, Optional
from jose import jwt, JWTError
import logging
from enum import Enum

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class CurrentUser:
    """Current authenticated user"""
    def __init__(self, user_id: int, role: UserRole):
        self.user_id = user_id
        self.role = role
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


async def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None
) -> CurrentUser:
    """
    Extract and validate JWT token from Authorization header
    
    Returns: CurrentUser object with user_id and role
    Raises: HTTPException if token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    
    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract user_id from payload (sub claim)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing user_id",
            )
        
        # Extract role (default to USER if not present)
        role_str = payload.get("role", "USER")
        try:
            role = UserRole(role_str)
        except ValueError:
            role = UserRole.USER
        
        return CurrentUser(user_id=int(user_id), role=role)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.error(f"JWT validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_admin_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)]
) -> CurrentUser:
    """
    Verify that current user has ADMIN role
    
    Raises: HTTPException if user is not admin
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# Type aliases for dependency injection
AuthUser = Annotated[CurrentUser, Depends(get_current_user)]
AdminUser = Annotated[CurrentUser, Depends(get_admin_user)]