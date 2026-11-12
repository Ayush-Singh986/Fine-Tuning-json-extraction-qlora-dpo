"""SFT training with QLoRA for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class SFTTrainer:
    """SFT trainer with QLoRA support."""
    
    config: Dict[str, Any]
    
    def train(self):
        """Train model with SFT."""
        print("Training with SFT (QLoRA)")