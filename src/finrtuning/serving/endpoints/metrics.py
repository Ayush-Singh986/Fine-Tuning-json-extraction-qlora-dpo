"""Metrics endpoint for Finr-Tuning API."""

from fastapi import APIRouter
from pydantic import BaseModel


class MetricsResponse(BaseModel):
    """Prometheus metrics response."""
    
    gpu_utilization: float
    gpu_memory_used: int
    gpu_memory_total: int
    requests_per_second: float
    latency_p50_ms: float
    latency_p95_ms: float


router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    """Get Prometheus metrics."""
    return MetricsResponse(
        gpu_utilization=0.0,
        gpu_memory_used=0,
        gpu_memory_total=16000,
        requests_per_second=0.0,
        latency_p50_ms=0.0,
        latency_p95_ms=0.0,
    )