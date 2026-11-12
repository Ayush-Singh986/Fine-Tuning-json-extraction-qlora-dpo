"""Configuration registry for centralized config management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from finrtuning.config.base import (
    BaseConfig,
    ConfigValidationError,
    ModelConfig,
    DatasetConfig,
    TrainingConfig,
    EvaluationConfig,
    InferenceConfig,
    MonitoringConfig,
)


@dataclass
class ConfigRegistry:
    """Centralized configuration registry."""
    
    base_path: Path
    configs: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize config registry."""
        self.configs = {}
        self._load_all_configs()
    
    def _load_all_configs(self) -> None:
        """Load all configuration files."""
        configs_dir = self.base_path / "configs"
        if not configs_dir.exists():
            return
        
        for yaml_file in configs_dir.glob("*.yaml"):
            self._load_config_file(yaml_file)
    
    def _load_config_file(self, path: Path) -> None:
        """Load a single configuration file."""
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            
            config_name = path.stem
            self.configs[config_name] = data
        except Exception as e:
            raise ConfigValidationError(f"Failed to load config {path}: {e}")
    
    def get_model_config(self, name: str) -> Optional[ModelConfig]:
        """Get model configuration by name."""
        if name not in self.configs:
            return None
        
        model_data = self.configs[name].get("model", {})
        try:
            return ModelConfig(**model_data)
        except Exception as e:
            raise ConfigValidationError(f"Invalid model config '{name}': {e}")
    
    def get_dataset_config(self) -> DatasetConfig:
        """Get dataset configuration."""
        data = self.configs.get("data_build", {})
        return DatasetConfig(**data)
    
    def get_training_config(self) -> TrainingConfig:
        """Get training configuration."""
        data = self.configs.get("training", {})
        return TrainingConfig(**data)
    
    def get_evaluation_config(self) -> EvaluationConfig:
        """Get evaluation configuration."""
        data = self.configs.get("eval", {})
        return EvaluationConfig(**data)
    
    def get_inference_config(self) -> InferenceConfig:
        """Get inference configuration."""
        data = self.configs.get("inference", {})
        return InferenceConfig(**data)
    
    def get_monitoring_config(self) -> MonitoringConfig:
        """Get monitoring configuration."""
        data = self.configs.get("monitoring", {})
        return MonitoringConfig(**data)
    
    def list_models(self) -> List[str]:
        """List all registered model configurations."""
        return list(self.configs.keys())
    
    def validate(self) -> bool:
        """Validate all configurations."""
        try:
            self.get_model_config("default")
            self.get_dataset_config()
            self.get_training_config()
            self.get_evaluation_config()
            self.get_inference_config()
            self.get_monitoring_config()
            return True
        except Exception:
            return False