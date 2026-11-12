"""QLoRA configuration for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class QLoRAConfig:
    """QLoRA configuration."""
    
    r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__