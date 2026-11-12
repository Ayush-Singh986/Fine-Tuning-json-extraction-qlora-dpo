"""Pydantic validation schemas for Finr-Tuning."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError


class PathValidator:
    """Path validation utilities."""
    
    @staticmethod
    def validate_absolute_path(path: str) -> str:
        """Validate path is absolute."""
        p = Path(path)
        if not p.is_absolute():
            raise ValueError(f"Path must be absolute: {path}")
        return path
    
    @staticmethod
    def validate_directory(path: str) -> str:
        """Validate path is an existing directory."""
        p = Path(path)
        if not p.exists():
            raise ValueError(f"Directory does not exist: {path}")
        if not p.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        return path
    
    @staticmethod
    def validate_file(path: str) -> str:
        """Validate path is an existing file."""
        p = Path(path)
        if not p.exists():
            raise ValueError(f"File does not exist: {path}")
        if not p.is_file():
            raise ValueError(f"Path is not a file: {path}")
        return path


class ModelPathConfig(BaseModel):
    """Model path configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    model_name_or_path: str = Field(..., description="Model identifier or path")
    tokenizer_name_or_path: Optional[str] = Field(default=None, description="Tokenizer path")
    revision: Optional[str] = Field(default=None, description="Model revision")
    
    @field_validator("model_name_or_path")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validate model name format."""
        if "/" not in v and not Path(v).exists():
            raise ValueError("Model must be in format 'organization/model' or a valid path")
        return v


class QuantizationConfig(BaseModel):
    """Quantization configuration for QLoRA."""
    
    model_config = ConfigDict(extra="forbid")
    
    enabled: bool = Field(default=True)
    load_in_4bit: bool = Field(default=True)
    bnb_4bit_quant_type: str = Field(default="nf4", pattern="^(nf4|fp4)$")
    bnb_4bit_use_double_quant: bool = Field(default=True)
    bnb_4bit_compute_dtype: str = Field(default="auto")


class LoRAConfig(BaseModel):
    """LoRA configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    r: int = Field(default=16, ge=1, le=256, description="LoRA rank")
    lora_alpha: int = Field(default=32, ge=1, le=1024, description="LoRA alpha")
    lora_dropout: float = Field(default=0.05, ge=0, lt=1, description="LoRA dropout")
    bias: str = Field(default="none", pattern="^(none|all|lora_only)$")
    task_type: str = Field(default="CAUSAL_LM", description="Task type")
    target_modules: Optional[List[str]] = Field(
        default=None, description="Target modules for LoRA"
    )
    
    def to_peft_config(self) -> Dict[str, Any]:
        """Convert to PEFT configuration format."""
        return {
            "r": self.r,
            "lora_alpha": self.lora_alpha,
            "lora_dropout": self.lora_dropout,
            "bias": self.bias,
            "task_type": self.task_type,
            "target_modules": self.target_modules or ["q_proj", "k_proj", "v_proj", "o_proj"],
        }


class TrainingRunConfig(BaseModel):
    """Complete training run configuration."""
    
    model: ModelPathConfig
    data: Dict[str, Any]
    quantization: QuantizationConfig
    lora: LoRAConfig
    training: Dict[str, Any]