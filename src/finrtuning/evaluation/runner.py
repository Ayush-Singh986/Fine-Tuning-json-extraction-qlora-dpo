"""Unified evaluation runner with confidence intervals."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from datasets import Dataset


@dataclass
class EvaluationResult:
    """Single evaluation result."""
    
    model_name: str
    metrics: Dict[str, float]
    metadata: Dict[str, Any]


class EvaluationRunner:
    """Unified evaluation runner with multiple seeds."""
    
    def __init__(
        self,
        model_loader: Any,
        metrics_calculator: Any,
        config: Dict[str, Any] | None = None,
    ):
        """Initialize evaluation runner."""
        self.model_loader = model_loader
        self.metrics_calculator = metrics_calculator
        self.config = config or {}
        self.results: List[EvaluationResult] = []
    
    def run_evaluation(
        self,
        model_name: str,
        test_dataset: Dataset,
        num_seeds: int = 3,
        seed_range: range = range(42, 45),
    ) -> List[EvaluationResult]:
        """Run evaluation with multiple seeds for confidence intervals."""
        results = []
        
        for seed in seed_range:
            result = self._run_single_seed(model_name, test_dataset, seed)
            results.append(result)
        
        self.results.extend(results)
        return results
    
    def _run_single_seed(
        self, model_name: str, dataset: Dataset, seed: int
    ) -> EvaluationResult:
        """Run evaluation with a single seed."""
        # Load model
        model, tokenizer = self.model_loader.load(model_name)
        
        # Run inference
        predictions = []
        for i in range(min(100, len(dataset))):  # Sample for demo
            row = dataset[i]
            prompt = row.get("prompt", row.get("input", ""))
            
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
                seed=seed,
            )
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            predictions.append(response)
        
        # Calculate metrics
        metrics = self.metrics_calculator.calculate(dataset, predictions)
        
        return EvaluationResult(
            model_name=model_name,
            metrics=metrics,
            metadata={"seed": seed},
        )
    
    def compute_confidence_intervals(self) -> Dict[str, Dict[str, Any]]:
        """Compute confidence intervals across seeds."""
        from statistics import mean, stdev
        
        if not self.results:
            return {}
        
        # Aggregate metrics by name
        metrics_by_name: Dict[str, List[float]] = {}
        for result in self.results:
            for metric_name, metric_value in result.metrics.items():
                if metric_name not in metrics_by_name:
                    metrics_by_name[metric_name] = []
                metrics_by_name[metric_name].append(metric_value)
        
        # Compute statistics
        confidence_intervals = {}
        for metric_name, values in metrics_by_name.items():
            if len(values) < 2:
                confidence_intervals[metric_name] = {
                    "mean": values[0] if values else 0,
                    "ci_lower": values[0] if values else 0,
                    "ci_upper": values[0] if values else 0,
                    "count": len(values),
                }
            else:
                m = mean(values)
                s = stdev(values)
                confidence_intervals[metric_name] = {
                    "mean": m,
                    "ci_lower": m - 1.96 * s / (len(values) ** 0.5),
                    "ci_upper": m + 1.96 * s / (len(values) ** 0.5),
                    "count": len(values),
                }
        
        return confidence_intervals