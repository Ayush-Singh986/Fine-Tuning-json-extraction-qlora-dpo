"""Multi-model comparison and analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ComparativeAnalysis:
    """Multi-model comparative analysis."""
    
    def compare(
        self, results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare multiple model results."""
        comparison = {
            "models": [],
            "metrics_summary": {},
        }
        
        for result in results:
            model_name = result.get("model_name", "unknown")
            comparison["models"].append(model_name)
        
        return comparison