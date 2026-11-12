"""Phi-specific adapter configuration."""

from finrtuning.models.adapters.base import BaseAdapter, AdapterConfig


class PhiAdapter(BaseAdapter):
    """Adapter for Microsoft Phi family models (Phi-4, Phi-3)."""
    
    adapter_type = "phi"
    default_target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "fc1", "fc2",
    ]
    
    def get_tokenizer_config(self) -> dict[str, Any]:
        """Phi-specific tokenizer configuration."""
        return {
            "pad_token": "<|endoftext|>",
            "eos_token": "<|endoftext|>",
        }
    
    def get_generation_config(self) -> dict[str, Any]:
        """Phi-specific generation configuration."""
        return {
            "pad_token_id": 50256,
            "eos_token_id": 50256,
        }
    
    def get_peft_config(self) -> dict[str, Any]:
        """Phi-specific PEFT configuration."""
        config = super().get_peft_config()
        # Phi models work well with standard LoRA settings
        config["r"] = 8
        config["lora_alpha"] = 16
        config["lora_dropout"] = 0.05
        return config