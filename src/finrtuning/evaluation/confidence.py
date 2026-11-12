"""Confidence interval calculation for evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
from statistics import mean, stdev


@dataclass
class ConfidenceInterval:
    """Confidence interval for a metric."""
    
    mean: float
    ci_lower: float
    ci_upper: float
    count: int


def calculate_ci(
    values: List[float], confidence: float = 0.95
) -> ConfidenceInterval:
    """Calculate confidence interval for a list of values."""
    if len(values) < 2:
        return ConfidenceInterval(
            mean=values[0] if values else 0,
            ci_lower=values[0] if values else 0,
            ci_upper=values[0] if values else 0,
            count=len(values),
        )
    
    m = mean(values)
    s = stdev(values)
    from math import sqrt
    from scipy import stats
    
    # Use z-score for large samples, t-score for small
    if len(values) >= 30:
        z = 1.96  # 95% confidence
    else:
        z = stats.t.ppf((1 + confidence) / 2, len(values) - 1)
    
    margin = z * s / sqrt(len(values))
    
    return ConfidenceInterval(
        mean=m,
        ci_lower=m - margin,
        ci_upper=m + margin,
        count=len(values),
    )