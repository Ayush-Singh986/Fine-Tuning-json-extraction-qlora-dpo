"""Data pipeline for dataset processing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

import pandas as pd
from datasets import Dataset, DatasetDict, load_dataset


@dataclass
class DatasetSplit:
    """Dataset split with metadata."""
    
    name: str
    dataset: Dataset
    size: int
    checksum: str


class DataPipeline:
    """Data pipeline for dataset processing."""
    
    def __init__(self, config: Dict[str, Any] | None = None):
        """Initialize data pipeline."""
        self.config = config or {}
        self.splits: Dict[str, DatasetSplit] = {}
    
    def load_from_jsonl(self, path: str | Path) -> Dataset:
        """Load dataset from JSONL file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")
        
        return Dataset.from_json(str(path))
    
    def load_from_csv(self, path: str | Path) -> Dataset:
        """Load dataset from CSV file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")
        
        return Dataset.from_pandas(pd.read_csv(path))
    
    def load_from_parquet(self, path: str | Path) -> Dataset:
        """Load dataset from Parquet file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")
        
        return Dataset.from_parquet(str(path))
    
    def train_validation_test_split(
        self, dataset: Dataset, ratios: Dict[str, float], seed: int = 42
    ) -> DatasetDict:
        """Split dataset into train/validation/test."""
        from datasets import DatasetDict, train_test_split
        
        # Normalize ratios
        total = sum(ratios.values())
        normalized = {k: v / total for k, v in ratios.items()}
        
        # Perform splits
        dataset_dict = DatasetDict()
        
        # First split: train vs (val + test)
        train_val_test = dataset.train_test_split(
            test_size=1 - normalized["train"], seed=seed
        )
        dataset_dict["train"] = train_val_test["train"]
        
        # Second split: val vs test
        val_test_size = normalized["test"] / (normalized["val"] + normalized["test"])
        val_test = train_val_test["test"].train_test_split(
            test_size=val_test_size, seed=seed
        )
        dataset_dict["validation"] = val_test["train"]
        dataset_dict["test"] = val_test["test"]
        
        return dataset_dict
    
    def save_split(self, dataset: Dataset, name: str, path: str | Path) -> None:
        """Save dataset split to file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        dataset.to_json(str(path))
        
        # Store split metadata
        self.splits[name] = DatasetSplit(
            name=name,
            dataset=dataset,
            size=len(dataset),
            checksum=self._compute_checksum(dataset),
        )
    
    def _compute_checksum(self, dataset: Dataset) -> str:
        """Compute dataset checksum."""
        import hashlib
        
        data_str = json.dumps(dataset.to_dict(), sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]