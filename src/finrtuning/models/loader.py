"""Model loader with adapter support."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
import torch

from finrtuning.models.adapters.base import BaseAdapter
from finrtuning.models.registry import ModelRegistry, ModelConfig


@dataclass
class LoadedModel:
    """A loaded model with tokenizer and adapter."""
    
    model: Any
    tokenizer: Any
    adapter: Optional[BaseAdapter]
    model_config: ModelConfig


class ModelLoader:
    """Loader for models with adapter support."""
    
    def __init__(self, device_map: Optional[str] = None):
        """Initialize model loader."""
        self.device_map = device_map
        self.registry = ModelRegistry.get_instance()
    
    def load(
        self,
        model_name: str,
        adapter_path: Optional[str | Path] = None,
        torch_dtype: str = "auto",
        trust_remote_code: bool = False,
    ) -> LoadedModel:
        """Load a model with optional adapter."""
        config = self.registry.get_model(model_name)
        if not config:
            raise ValueError(f"Model '{model_name}' not found in registry")
        
        # Load tokenizer and model
        tokenizer = self._load_tokenizer(
            config.huggingface_id,
            trust_remote_code=trust_remote_code,
        )
        model = self._load_model(
            config.huggingface_id,
            torch_dtype=torch_dtype,
            device_map=self.device_map,
            trust_remote_code=trust_remote_code,
        )
        
        # Load adapter if specified
        adapter = None
        if adapter_path:
            adapter = self._load_adapter(model, adapter_path, config)
        
        return LoadedModel(
            model=model,
            tokenizer=tokenizer,
            adapter=adapter,
            model_config=config,
        )
    
    def _load_tokenizer(
        self,
        model_name_or_path: str,
        trust_remote_code: bool = False,
    ) -> Any:
        """Load tokenizer from Hugging Face."""
        from transformers import AutoTokenizer
        
        return AutoTokenizer.from_pretrained(
            model_name_or_path,
            trust_remote_code=trust_remote_code,
        )
    
    def _load_model(
        self,
        model_name_or_path: str,
        torch_dtype: str = "auto",
        device_map: Optional[str] = None,
        trust_remote_code: bool = False,
    ) -> Any:
        """Load model from Hugging Face."""
        from transformers import AutoModelForCausalLM
        
        # Resolve torch dtype
        if torch_dtype == "auto":
            if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
                torch_dtype = torch.bfloat16
            else:
                torch_dtype = torch.float16
        elif hasattr(torch, torch_dtype):
            torch_dtype = getattr(torch, torch_dtype)
        
        return AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            torch_dtype=torch_dtype,
            device_map=device_map,
            trust_remote_code=trust_remote_code,
        )
    
    def _load_adapter(
        self,
        model: Any,
        adapter_path: str | Path,
        config: ModelConfig,
    ) -> BaseAdapter:
        """Load adapter and attach to model."""
        from peft import PeftModel
        
        adapter_path = Path(adapter_path)
        if not adapter_path.exists():
            raise ValueError(f"Adapter path does not exist: {adapter_path}")
        
        # Load PEFT adapter
        model = PeftModel.from_pretrained(model, adapter_path)
        
        # Get adapter instance
        adapter_class = self.registry.get_default_adapter(config.name)
        if adapter_class:
            adapter = adapter_class()
            return adapter
        
        return None