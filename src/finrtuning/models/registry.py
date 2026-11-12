"""Model registry and configuration-driven model loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from finrtuning.models.adapters.base import BaseAdapter


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for a single model in the registry."""
    
    name: str
    huggingface_id: str
    chat_template: Optional[str]
    adapter_type: Optional[str]
    max_seq_length: int
    gpu_memory_gb: int
    context_length: int
    compatible_with_qlora: bool
    compatible_with_sft: bool
    compatible_with_dpo: bool


class ModelRegistry:
    """Configuration-driven model registry."""
    
    def __init__(self, config_path: Optional[str | Path] = None):
        """Initialize model registry."""
        self._models: Dict[str, ModelConfig] = {}
        self._adapters: Dict[str, type[BaseAdapter]] = {}
        self._config_path = Path(config_path) if config_path else None
        self._load_default_models()
    
    def _load_default_models(self) -> None:
        """Load default model configurations."""
        # Qwen2.5-1.5B-Instruct (reference)
        self.register_model(
            name="qwen2.5-1.5b-instruct",
            huggingface_id="Qwen/Qwen2.5-1.5B-Instruct",
            chat_template="chatml",
            adapter_type="qwen",
            max_seq_length=2048,
            gpu_memory_gb=16,
            context_length=2048,
            compatible_with_qlora=True,
            compatible_with_sft=True,
            compatible_with_dpo=True,
        )
        
        # Qwen3.5-2B (new)
        self.register_model(
            name="qwen3.5-2b",
            huggingface_id="Qwen/Qwen3.5-2B",
            chat_template="chatml",
            adapter_type="qwen",
            max_seq_length=2048,
            gpu_memory_gb=16,
            context_length=2048,
            compatible_with_qlora=True,
            compatible_with_sft=True,
            compatible_with_dpo=True,
        )
        
        # Phi-4-mini-instruct (new)
        self.register_model(
            name="phi-4-mini-instruct",
            huggingface_id="microsoft/phi-4-mini-instruct",
            chat_template="phi",
            adapter_type="phi",
            max_seq_length=2048,
            gpu_memory_gb=16,
            context_length=2048,
            compatible_with_qlora=True,
            compatible_with_sft=True,
            compatible_with_dpo=True,
        )
        
        # Granite 4.2-3B (new)
        self.register_model(
            name="granite-4.2-3b",
            huggingface_id="ibm/granite-4.2-3b-instruct",
            chat_template="chatml",
            adapter_type="granite",
            max_seq_length=2048,
            gpu_memory_gb=24,
            context_length=2048,
            compatible_with_qlora=True,
            compatible_with_sft=True,
            compatible_with_dpo=True,
        )
    
    def register_model(self, **kwargs) -> ModelConfig:
        """Register a new model configuration."""
        config = ModelConfig(**kwargs)
        self._models[config.name] = config
        return config
    
    def get_model(self, name: str) -> Optional[ModelConfig]:
        """Get model configuration by name."""
        return self._models.get(name)
    
    def get_model_by_huggingface_id(self, hf_id: str) -> Optional[ModelConfig]:
        """Get model configuration by Hugging Face ID."""
        for config in self._models.values():
            if config.huggingface_id == hf_id:
                return config
        return None
    
    def list_models(self) -> List[str]:
        """List all registered model names."""
        return list(self._models.keys())
    
    def register_adapter(self, model_name: str, adapter_class: type[BaseAdapter]) -> None:
        """Register an adapter class for a model."""
        self._adapters[model_name] = adapter_class
    
    def get_adapter(self, model_name: str) -> Optional[type[BaseAdapter]]:
        """Get adapter class for a model."""
        return self._adapters.get(model_name)
    
    def get_default_adapter(self, model_name: str) -> Optional[type[BaseAdapter]]:
        """Get default adapter class based on model name."""
        if model_name in self._adapters:
            return self._adapters[model_name]
        
        # Try to detect adapter type from model name
        if "qwen" in model_name.lower():
            from finrtuning.models.adapters.qwen import QwenAdapter
            return QwenAdapter
        elif "phi" in model_name.lower():
            from finrtuning.models.adapters.phi import PhiAdapter
            return PhiAdapter
        elif "granite" in model_name.lower():
            from finrtuning.models.adapters.granite import GraniteAdapter
            return GraniteAdapter
        
        return None
    
    def validate_model_compatibility(
        self, model_name: str, method: str
    ) -> tuple[bool, str]:
        """Validate if a model is compatible with a training method."""
        config = self._models.get(model_name)
        if not config:
            return False, f"Model '{model_name}' not found in registry"
        
        if method == "qlora" and not config.compatible_with_qlora:
            return False, f"Model '{model_name}' is not compatible with QLoRA"
        
        if method == "sft" and not config.compatible_with_sft:
            return False, f"Model '{model_name}' is not compatible with SFT"
        
        if method == "dpo" and not config.compatible_with_dpo:
            return False, f"Model '{model_name}' is not compatible with DPO"
        
        return True, "Model is compatible"


def load_model_from_registry(model_name: str) -> tuple[Any, Any]:
    """Load a model and tokenizer from Hugging Face using registry."""
    registry = ModelRegistry()
    config = registry.get_model(model_name)
    
    if not config:
        raise ValueError(f"Model '{model_name}' not found in registry")
    
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    tokenizer = AutoTokenizer.from_pretrained(config.huggingface_id)
    model = AutoModelForCausalLM.from_pretrained(config.huggingface_id)
    
    return model, tokenizer


def get_adapter_for_model(model_name: str) -> Optional[BaseAdapter]:
    """Get an adapter instance for a model."""
    registry = ModelRegistry()
    adapter_class = registry.get_default_adapter(model_name)
    
    if adapter_class:
        return adapter_class()
    
    return None