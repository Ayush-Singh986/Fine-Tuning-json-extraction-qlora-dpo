"""Base configuration classes for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass


@dataclass(frozen=True)
class BaseConfig:
    """Base configuration class with YAML loading support."""
    
    @classmethod
    def from_yaml(cls, path: str | Path) -> "BaseConfig":
        """Load configuration from YAML file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path) as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseConfig":
        """Create configuration from dictionary."""
        raise NotImplementedError
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        raise NotImplementedError
    
    def to_yaml(self, path: str | Path) -> None:
        """Save configuration to YAML file."""
        path = Path(path)
        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)


class ModelConfig(BaseModel):
    """Model configuration with validation."""
    
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(..., description="Model identifier")
    huggingface_id: str = Field(..., description="Hugging Face model ID")
    chat_template: Optional[str] = Field(default=None, description="Chat template name")
    adapter_type: Optional[str] = Field(default=None, description="Adapter type")
    max_seq_length: int = Field(default=2048, ge=256, le=32768, description="Maximum sequence length")
    context_length: int = Field(default=2048, ge=256, le=32768, description="Context length")
    gpu_memory_gb: int = Field(default=16, ge=8, le=80, description="GPU memory requirement")
    
    compatible_with_qlora: bool = Field(default=True, description="Supports QLoRA")
    compatible_with_sft: bool = Field(default=True, description="Supports SFT")
    compatible_with_dpo: bool = Field(default=True, description="Supports DPO")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate model name."""
        if not v or len(v) < 1:
            raise ValueError("Model name cannot be empty")
        return v
    
    @field_validator("huggingface_id")
    @classmethod
    def validate_huggingface_id(cls, v: str) -> str:
        """Validate Hugging Face ID format."""
        if "/" not in v:
            raise ValueError("Hugging Face ID must be in format 'organization/model'")
        return v


class DatasetConfig(BaseModel):
    """Dataset configuration with validation."""
    
    model_config = ConfigDict(extra="forbid")
    
    train_path: str = Field(..., description="Training data path")
    eval_path: str = Field(..., description="Evaluation data path")
    test_path: str = Field(..., description="Test data path")
    
    split_ratios: Dict[str, float] = Field(
        default_factory=lambda: {"train": 0.8, "eval": 0.1, "test": 0.1}
    )
    
    max_seq_length: int = Field(default=2048, ge=256, le=32768)
    validate_schema: bool = Field(default=True, description="Validate against schema")
    detect_pii: bool = Field(default=True, description="Detect PII in data")
    check_leakage: bool = Field(default=True, description="Check for data leakage")


class TrainingConfig(BaseModel):
    """Training configuration with validation."""
    
    model_config = ConfigDict(extra="forbid")
    
    seed: int = Field(default=42, ge=0, le=999999)
    num_train_epochs: int = Field(default=3, ge=1, le=100)
    per_device_train_batch_size: int = Field(default=1, ge=1, le=64)
    gradient_accumulation_steps: int = Field(default=8, ge=1, le=128)
    learning_rate: float = Field(default=2e-4, gt=0, lt=1)
    
    # Quantization
    use_qlora: bool = Field(default=True, description="Use QLoRA quantization")
    load_in_4bit: bool = Field(default=True, description="Load model in 4-bit")
    bnb_4bit_quant_type: str = Field(default="nf4", description="4-bit quantization type")
    bnb_4bit_use_double_quant: bool = Field(default=True)
    compute_dtype: str = Field(default="auto", description="Compute dtype")
    
    # LoRA
    lora_r: int = Field(default=16, ge=1, le=256)
    lora_alpha: int = Field(default=32, ge=1, le=1024)
    lora_dropout: float = Field(default=0.05, ge=0, lt=1)
    
    # Training features
    gradient_checkpointing: bool = Field(default=True)
    packing: bool = Field(default=False)
    logging_steps: int = Field(default=5, ge=1, le=1000)


class EvaluationConfig(BaseModel):
    """Evaluation configuration with validation."""
    
    model_config = ConfigDict(extra="forbid")
    
    batch_size: int = Field(default=4, ge=1, le=128)
    max_new_tokens: int = Field(default=256, ge=1, le=2048)
    temperature: float = Field(default=0.0, ge=0, le=1)
    top_p: float = Field(default=1.0, ge=0, le=1)
    
    # Metrics
    compute_json_validity: bool = Field(default=True)
    compute_schema_pass: bool = Field(default=True)
    compute_field_f1: bool = Field(default=True)
    compute_latency: bool = Field(default=True)
    
    # Multiple seeds for confidence intervals
    num_evaluation_seeds: int = Field(default=3, ge=1, le=10)


class InferenceConfig(BaseModel):
    """Inference configuration with validation."""
    
    model_config = ConfigDict(extra="forbid")
    
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, ge=1, le=65535, description="API port")
    max_concurrent_requests: int = Field(default=10, ge=1, le=1000)
    
    # Rate limiting
    rate_limit_requests: int = Field(default=100, ge=1, le=10000)
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600)
    
    # CORS
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])


class MonitoringConfig(BaseModel):
    """Monitoring configuration with validation."""
    
    model_config = ConfigDict(extra="forbid")
    
    enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=9090, ge=1, le=65535)
    
    # Metrics
    collect_gpu_metrics: bool = Field(default=True)
    collect_cpu_metrics: bool = Field(default=True)
    collect_memory_metrics: bool = Field(default=True)
    collect_api_metrics: bool = Field(default=True)
    
    # Alerting
    alert_on_high_latency: bool = Field(default=True)
    high_latency_threshold_ms: int = Field(default=5000, ge=1000, le=60000)
    alert_on_gpu_memory: bool = Field(default=True)
    gpu_memory_threshold_percent: int = Field(default=90, ge=50, le=100)