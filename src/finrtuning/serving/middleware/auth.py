"""Authentication middleware for Finr-Tuning API."""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


async def authenticate(request: Request, credentials: HTTPAuthorizationCredentials):
    """Authenticate request with bearer token."""
    # In production, validate token against auth server
    # For now, accept any valid token
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authentication token",
        )
    return credentials.credentials