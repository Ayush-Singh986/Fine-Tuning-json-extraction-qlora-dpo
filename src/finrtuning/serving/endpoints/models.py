"""Model listing endpoint for Finr-Tuning API."""

from fastapi import APIRouter
from pydantic import BaseModel


class ModelInfo(BaseModel):
    """Model information."""
    
    name: str
    huggingface_id: str
    loaded: bool


router = APIRouter()


@router.get("/models", response_model=list[ModelInfo])
def list_models():
    """List available models."""
    return [
        ModelInfo(
            name="qwen2.5-1.5b-instruct",
            huggingface_id="Qwen/Qwen2.5-1.5B-Instruct",
            loaded=True,
        ),
        ModelInfo(
            name="qwen3.5-2b",
            huggingface_id="Qwen/Qwen3.5-2B",
            loaded=False,
        ),
        ModelInfo(
            name="phi-4-mini-instruct",
            huggingface_id="microsoft/phi-4-mini-instruct",
            loaded=False,
        ),
        ModelInfo(
            name="granite-4.2-3b",
            huggingface_id="ibm/granite-4.2-3b-instruct",
            loaded=False,
        ),
    ]