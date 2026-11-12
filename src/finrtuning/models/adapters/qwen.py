"""Qwen-specific adapter configuration."""

from finrtuning.models.adapters.base import BaseAdapter, AdapterConfig


class QwenAdapter(BaseAdapter):
    """Adapter for Qwen family models (Qwen2.5, Qwen3)."""
    
    adapter_type = "qwen"
    default_target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ]
    
    def get_tokenizer_config(self):
        """Qwen-specific tokenizer configuration."""
        return {
            "pad_token": "<|endoftext|>",
            "eos_token": "<|endoftext|>",
        }
    
    def get_generation_config(self):
        """Qwen-specific generation configuration."""
        return {
            "pad_token_id": 151643,
            "eos_token_id": 151645,
        }