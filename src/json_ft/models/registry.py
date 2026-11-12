"""Model registry and configuration-driven model loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

from finrtuning.models.adapters.base import BaseAdapter


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for a single model in the registry."""
    
    name: str
    huggingface_id: str
    chat_template: str | None
    adapter_type: str | None
    max_seq_length: int
    gpu_memory_gb: int
    context_length: int
    compatible_with_qlora: bool
    compatible_with_sft: bool
    compatible_with_dpo: bool


class ModelRegistry:
    """Configuration-driven model registry."""
    
    def __init__(self, config_path: str | Path | None = None):
        """Initialize registry from config file."""
        self.config_path = Path(config_path) if config_path else None
        self._models: dict[str, ModelConfig] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load model configurations from YAML file."""
        if self.config_path and self.config_path.exists():
            with open(self.config_path) as f:
                config = yaml.safe_load(f)
            
            models_config = config.get("models", {})
            for name, model_config in models_config.items():
                self._models[name] = ModelConfig(
                    name=name,
                    huggingface_id=model_config["huggingface_id"],
                    chat_template=model_config.get("chat_template"),
                    adapter_type=model_config.get("adapter_type"),
                    max_seq_length=model_config.get("max_seq_length", 2048),
                    gpu_memory_gb=model_config.get("gpu_memory_gb", 16),
                    context_length=model_config.get("context_length", 2048),
                    compatible_with_qlora=model_config.get("compatible_with_qlora", True),
                    compatible_with_sft=model_config.get("compatible_with_sft", True),
                    compatible_with_dpo=model_config.get("compatible_with_dpo", True),
                )
    
    def get_model(self, name: str) -> ModelConfig | None:
        """Get model configuration by name."""
        return self._models.get(name)
    
    def list_models(self) -> list[str]:
        """List all registered model names."""
        return list(self._models.keys())
    
    def get_adapter(self, model_name: str) -> type[BaseAdapter] | None:
        """Get adapter class for a model."""
        config = self._models.get(model_name)
        if not config:
            return None
        
        # Import adapter based on model type
        if "qwen" in model_name.lower():
            from finrtuning.models.adapters.qwen import QwenAdapter
            return QwenAdapter
        elif "phi" in model_name.lower():
            from finrtuning.models.adapters.phi import PhiAdapter
            return PhiAdapter
        elif "granite" in model_name.lower():
            from finrtuning.models.adapters.granite import GraniteAdapter
            return GraniteAdapter
        
        # Default to base adapter
        return BaseAdapter


def load_model(config: ModelConfig) -> tuple[Any, Any]:
    """Load a model and tokenizer from Hugging Face."""
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    tokenizer = AutoTokenizer.from_pretrained(config.huggingface_id)
    model = AutoModelForCausalLM.from_pretrained(config.huggingface_id)
    
    return model, tokenizer


def get_model_adapter(model_name: str) -> BaseAdapter | None:
    """Get an adapter instance for a model."""
    registry = ModelRegistry()
    adapter_class = registry.get_adapter(model_name)
    
    if adapter_class:
        return adapter_class()
    
    return None