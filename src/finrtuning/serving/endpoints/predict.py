"""Prediction endpoint for Finr-Tuning API."""

from fastapi import APIRouter
from pydantic import BaseModel


class PredictRequest(BaseModel):
    """Prediction request."""
    
    model_name: str
    prompt: str
    max_new_tokens: int = 256
    temperature: float = 0.0
    top_p: float = 1.0


class PredictResponse(BaseModel):
    """Prediction response."""
    
    model_name: str
    prediction: str
    metadata: dict


router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """Make predictions."""
    return PredictResponse(
        model_name=request.model_name,
        prediction=f"Response for: {request.prompt[:50]}...",
        metadata={"latency_ms": 100},
    )