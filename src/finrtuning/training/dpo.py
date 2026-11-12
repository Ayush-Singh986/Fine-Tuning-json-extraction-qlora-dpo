"""DPO training for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class DPOTrainer:
    """DPO trainer."""
    
    config: Dict[str, Any]
    
    def train(self):
        """Train model with DPO."""
        print("Training with DPO")