"""FastAPI inference service for Finr-Tuning."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    timestamp: str


class ModelInfo(BaseModel):
    """Model information."""
    
    name: str
    huggingface_id: str
    loaded: bool


class PredictRequest(BaseModel):
    """Prediction request."""
    
    model_name: str = Field(..., description="Model name")
    prompt: str = Field(..., description="Input prompt")
    max_new_tokens: int = Field(default=256, ge=1, le=2048)
    temperature: float = Field(default=0.0, ge=0, le=1)
    top_p: float = Field(default=1.0, ge=0, le=1)


class PredictResponse(BaseModel):
    """Prediction response."""
    
    model_name: str
    prediction: str
    metadata: Dict[str, Any]


class MetricsResponse(BaseModel):
    """Prometheus metrics response."""
    
    gpu_utilization: float
    gpu_memory_used: int
    gpu_memory_total: int
    requests_per_second: float
    latency_p50_ms: float
    latency_p95_ms: float


class APIServer:
    """FastAPI inference server."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """Initialize API server."""
        self.host = host
        self.port = port
        self.app = FastAPI(title="Finr-Tuning Inference API")
        self._model_loader: Any = None
        self._metrics: Dict[str, Any] = {}
        
        self._setup_routes()
        self._setup_middleware()
    
    def _setup_routes(self) -> None:
        """Setup API routes."""
        self.app.get("/health")(self.health_check)
        self.app.get("/models")(self.list_models)
        self.app.post("/predict")(self.predict)
        self.app.get("/metrics")(self.get_metrics)
    
    def _setup_middleware(self) -> None:
        """Setup middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def health_check(self) -> HealthResponse:
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            timestamp="2026-11-12T00:00:00Z",
        )
    
    def list_models(self) -> List[ModelInfo]:
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
    
    def predict(self, request: PredictRequest) -> PredictResponse:
        """Make predictions."""
        if not self._model_loader:
            raise HTTPException(
                status_code=503,
                detail="Model loader not initialized",
            )
        
        try:
            # Load model if not already loaded
            loaded_model = self._model_loader.load(request.model_name)
            
            # Generate response
            inputs = loaded_model.tokenizer(
                request.prompt, return_tensors="pt"
            )
            outputs = loaded_model.model.generate(
                **inputs,
                max_new_tokens=request.max_new_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                do_sample=request.temperature > 0,
            )
            response = loaded_model.tokenizer.decode(
                outputs[0], skip_special_tokens=True
            )
            
            return PredictResponse(
                model_name=request.model_name,
                prediction=response,
                metadata={"latency_ms": 100},
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Inference failed: {str(e)}",
            )
    
    def get_metrics(self) -> MetricsResponse:
        """Get Prometheus metrics."""
        return MetricsResponse(
            gpu_utilization=self._metrics.get("gpu_utilization", 0.0),
            gpu_memory_used=self._metrics.get("gpu_memory_used", 0),
            gpu_memory_total=self._metrics.get("gpu_memory_total", 0),
            requests_per_second=self._metrics.get("requests_per_second", 0.0),
            latency_p50_ms=self._metrics.get("latency_p50_ms", 0.0),
            latency_p95_ms=self._metrics.get("latency_p95_ms", 0.0),
        )
    
    def run(self) -> None:
        """Run the API server."""
        import uvicorn
        
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )