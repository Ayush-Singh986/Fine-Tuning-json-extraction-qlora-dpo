"""Base adapter interface for all model architectures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AdapterConfig:
    """Base configuration for all adapters."""
    
    r: int = 16
    alpha: int = 32
    dropout: float = 0.05
    bias: str = "none"
    task_type: str = "CAUSAL_LM"
    target_modules: list[str] | None = None


class BaseAdapter:
    """Base class for architecture-specific adapters."""
    
    adapter_type: str = "base"
    default_target_modules: list[str] = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ]
    
    def __init__(self, config: AdapterConfig | None = None):
        """Initialize adapter with optional custom config."""
        self.config = config or AdapterConfig()
    
    def get_peft_config(self) -> dict[str, Any]:
        """Return PEFT configuration for this adapter."""
        return {
            "r": self.config.r,
            "lora_alpha": self.config.alpha,
            "lora_dropout": self.config.dropout,
            "bias": self.config.bias,
            "task_type": self.config.task_type,
            "target_modules": self.config.target_modules or self.default_target_modules,
        }
    
    def get_tokenizer_config(self) -> dict[str, Any]:
        """Return tokenizer-specific configuration."""
        return {}
    
    def get_generation_config(self) -> dict[str, Any]:
        """Return generation-specific configuration."""
        return {}
    
    def validate_model_compatibility(self, model_name: str) -> tuple[bool, str]:
        """Validate if a model is compatible with this adapter."""
        return True, "Model is compatible"