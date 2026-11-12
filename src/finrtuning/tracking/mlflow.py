"""MLflow integration for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class MLflowTracker:
    """MLflow experiment tracker."""
    
    tracking_uri: str = "mlruns"
    
    def __post_init__(self):
        """Import mlflow."""
        import mlflow
        mlflow.set_tracking_uri(self.tracking_uri)
    
    def start_run(self, run_name: str = "default"):
        """Start a new MLflow run."""
        import mlflow
        return mlflow.start_run(run_name=run_name)
    
    def log_param(self, key: str, value: Any):
        """Log a parameter."""
        import mlflow
        mlflow.log_param(key, value)
    
    def log_metric(self, key: str, value: float):
        """Log a metric."""
        import mlflow
        mlflow.log_metric(key, value)
    
    def log_artifact(self, local_path: str | Path):
        """Log an artifact."""
        import mlflow
        mlflow.log_artifact(local_path)