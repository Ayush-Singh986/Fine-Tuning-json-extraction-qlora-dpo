"""Leaderboard scoring for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ScoringWeights:
    """Scoring weights for leaderboard."""
    
    json_validity: float = 0.25
    schema_pass: float = 0.20
    micro_f1: float = 0.25
    macro_f1: float = 0.10
    p50_latency: float = 0.10
    gpu_hours: float = 0.10


class LeaderboardScorer:
    """Calculate leaderboard scores."""
    
    def __init__(self, weights: ScoringWeights | None = None):
        """Initialize leaderboard scorer."""
        self.weights = weights or ScoringWeights()
    
    def calculate_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate leaderboard score from metrics."""
        score = 0.0
        
        score += self.weights.json_validity * metrics.get("json_validity", 0)
        score += self.weights.schema_pass * metrics.get("schema_pass", 0)
        score += self.weights.micro_f1 * metrics.get("micro_f1", 0)
        score += self.weights.macro_f1 * metrics.get("macro_f1", 0)
        
        # Normalize latency (lower is better)
        latency = metrics.get("p50_latency_ms", 0)
        normalized_latency = max(0, 1 - latency / 50000)
        score += self.weights.p50_latency * normalized_latency
        
        # Normalize cost (lower is better)
        gpu_hours = metrics.get("gpu_hours", 0)
        normalized_cost = max(0, 1 - gpu_hours / 10)
        score += self.weights.gpu_hours * normalized_cost
        
        return score
    
    def calculate_all_scores(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate scores for all results."""
        for result in results:
            result["leaderboard_score"] = self.calculate_score(result)
        
        results.sort(
            key=lambda x: x.get("leaderboard_score", 0), reverse=True
        )
        
        for i, result in enumerate(results):
            result["rank"] = i + 1
        
        return results