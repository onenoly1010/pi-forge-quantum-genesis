"""
JWT authentication for guardian-protected endpoints
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

# JWT configuration
GUARDIAN_JWT_SECRET = os.getenv("GUARDIAN_JWT_SECRET")
ALGORITHM = "HS256"

# Security scheme
security = HTTPBearer()


class JWTPayload:
    """JWT token payload"""
    def __init__(self, sub: str, role: str, **kwargs):
        self.sub = sub  # Subject (user identifier)
        self.role = role  # User role
        self.extra = kwargs  # Additional claims


def verify_jwt_token(token: str) -> JWTPayload:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        JWTPayload with decoded claims
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    if not GUARDIAN_JWT_SECRET:
        logger.error("GUARDIAN_JWT_SECRET not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT authentication not properly configured"
        )

    if len(GUARDIAN_JWT_SECRET) < 32:
        logger.error("GUARDIAN_JWT_SECRET is too short (must be at least 32 characters)")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT authentication not properly configured"
        )

    try:
        payload = jwt.decode(token, GUARDIAN_JWT_SECRET, algorithms=[ALGORITHM])
        
        # Extract required claims
        sub = payload.get("sub")
        role = payload.get("role")
        
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject"
            )
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing role"
            )
        
        return JWTPayload(sub=sub, role=role, **payload)
        
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> JWTPayload:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        JWTPayload with user information
    """
    return verify_jwt_token(credentials.credentials)


def require_guardian_role(
    current_user: JWTPayload = Depends(get_current_user)
) -> JWTPayload:
    """
    Dependency to require guardian role.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        JWTPayload if user has guardian role
        
    Raises:
        HTTPException: If user doesn't have guardian role
    """
    if current_user.role != "guardian":
        logger.warning(f"User {current_user.sub} attempted guardian action with role {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Guardian role required for this operation"
        )
    
    return current_user


# Helper function to create JWT tokens (for testing/development)
def create_jwt_token(sub: str, role: str, **extra_claims) -> str:
    """
    Create a JWT token (for testing purposes).
    
    Args:
        sub: Subject (user identifier)
        role: User role
        **extra_claims: Additional claims to include
        
    Returns:
        JWT token string
    """
    if not GUARDIAN_JWT_SECRET:
        raise ValueError("GUARDIAN_JWT_SECRET not configured")

    payload = {
        "sub": sub,
        "role": role,
        **extra_claims
    }
    
    return jwt.encode(payload, GUARDIAN_JWT_SECRET, algorithm=ALGORITHM)
