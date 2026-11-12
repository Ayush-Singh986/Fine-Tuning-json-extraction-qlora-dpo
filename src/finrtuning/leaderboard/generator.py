"""Leaderboard generation for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ModelRanking:
    """Model ranking in leaderboard."""
    
    model_name: str
    rank: int
    score: float
    metrics: Dict[str, float]


class LeaderboardGenerator:
    """Generate model leaderboards from evaluation results."""
    
    def __init__(self, config: Dict[str, Any] | None = None):
        """Initialize leaderboard generator."""
        self.config = config or {}
        self.rankings: Dict[str, List[ModelRanking]] = {}
    
    def generate_rankings(
        self, results: List[Dict[str, Any]]
    ) -> Dict[str, List[ModelRanking]]:
        """Generate rankings from evaluation results."""
        rankings = {}
        
        # Quality ranking
        quality_results = sorted(
            results, key=lambda x: x.get("json_validity", 0), reverse=True
        )
        rankings["quality"] = [
            ModelRanking(
                model_name=r["model_name"],
                rank=i + 1,
                score=r["json_validity"],
                metrics=r,
            )
            for i, r in enumerate(quality_results)
        ]
        
        # Cost ranking
        cost_results = sorted(
            results, key=lambda x: x.get("gpu_hours", float("inf"))
        )
        rankings["cost"] = [
            ModelRanking(
                model_name=r["model_name"],
                rank=i + 1,
                score=r["gpu_hours"],
                metrics=r,
            )
            for i, r in enumerate(cost_results)
        ]
        
        # Latency ranking
        latency_results = sorted(
            results, key=lambda x: x.get("p50_latency_ms", float("inf"))
        )
        rankings["latency"] = [
            ModelRanking(
                model_name=r["model_name"],
                rank=i + 1,
                score=r["p50_latency_ms"],
                metrics=r,
            )
            for i, r in enumerate(latency_results)
        ]
        
        self.rankings = rankings
        return rankings
    
    def get_model_rankings(self, model_name: str) -> Dict[str, int]:
        """Get model rankings across all categories."""
        rankings = {}
        for category, category_rankings in self.rankings.items():
            for ranking in category_rankings:
                if ranking.model_name == model_name:
                    rankings[category] = ranking.rank
                    break
        return rankings