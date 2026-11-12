"""Granite-specific adapter configuration."""

from finrtuning.models.adapters.base import BaseAdapter, AdapterConfig


class GraniteAdapter(BaseAdapter):
    """Adapter for IBM Granite family models."""
    
    adapter_type = "granite"
    default_target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ]
    
    def get_tokenizer_config(self) -> dict[str, Any]:
        """Granite-specific tokenizer configuration."""
        return {
            "pad_token": "<|endoftext|>",
            "eos_token": "<|endoftext|>",
        }
    
    def get_generation_config(self) -> dict[str, Any]:
        """Granite-specific generation configuration."""
        return {
            "pad_token_id": 49152,
            "eos_token_id": 49152,
        }
    
    def get_peft_config(self) -> dict[str, Any]:
        """Granite-specific PEFT configuration."""
        config = super().get_peft_config()
        # Granite models work well with higher LoRA ranks
        config["r"] = 32
        config["lora_alpha"] = 64
        config["lora_dropout"] = 0.1
        return config