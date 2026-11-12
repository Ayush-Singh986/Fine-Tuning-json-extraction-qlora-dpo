"""Health check endpoint for Finr-Tuning API."""

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    timestamp: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp="2026-11-12T00:00:00Z",
    )


@router.get("/ready")
def ready_check():
    """Readiness check endpoint."""
    return {"status": "ready"}