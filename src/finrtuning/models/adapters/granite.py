"""Granite-specific adapter configuration."""

from finrtuning.models.adapters.base import BaseAdapter, AdapterConfig


class GraniteAdapter(BaseAdapter):
    """Adapter for IBM Granite family models."""
    
    adapter_type = "granite"
    default_target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ]
    
    def get_tokenizer_config(self):
        """Granite-specific tokenizer configuration."""
        return {
            "pad_token": "<|endoftext|>",
            "eos_token": "<|endoftext|>",
        }
    
    def get_generation_config(self):
        """Granite-specific generation configuration."""
        return {
            "pad_token_id": 49152,
            "eos_token_id": 49152,
        }