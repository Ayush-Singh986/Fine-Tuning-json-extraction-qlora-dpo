"""Dataset versioning with checksums and snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib
import json

from datasets import Dataset


@dataclass
class DatasetVersion:
    """Dataset version with metadata."""
    
    version_id: str
    timestamp: str
    checksum: str
    size: int
    metadata: Dict[str, Any]
    features: Dict[str, str]


class DatasetVersioning:
    """Dataset versioning system."""
    
    def __init__(self, store_path: str | Path):
        """Initialize dataset versioning."""
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self._versions: Dict[str, DatasetVersion] = {}
        self._load_versions()
    
    def _load_versions(self) -> None:
        """Load existing versions from store."""
        versions_file = self.store_path / "versions.json"
        if versions_file.exists():
            with open(versions_file) as f:
                data = json.load(f)
            
            for version_id, version_data in data.items():
                self._versions[version_id] = DatasetVersion(**version_data)
    
    def compute_checksum(self, dataset: Dataset) -> str:
        """Compute dataset checksum."""
        data_str = json.dumps(dataset.to_dict(), sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def create_version(
        self, dataset: Dataset, metadata: Dict[str, Any] | None = None
    ) -> DatasetVersion:
        """Create a new dataset version."""
        checksum = self.compute_checksum(dataset)
        version_id = f"v{checksum[:8]}"
        
        version = DatasetVersion(
            version_id=version_id,
            timestamp=datetime.utcnow().isoformat(),
            checksum=checksum,
            size=len(dataset),
            metadata=metadata or {},
            features=dict(dataset.features),
        )
        
        self._versions[version_id] = version
        self._save_versions()
        
        return version
    
    def get_version(self, version_id: str) -> Optional[DatasetVersion]:
        """Get a specific dataset version."""
        return self._versions.get(version_id)
    
    def get_latest_version(self) -> Optional[DatasetVersion]:
        """Get the latest dataset version."""
        if not self._versions:
            return None
        
        return max(
            self._versions.values(),
            key=lambda v: v.timestamp,
        )
    
    def list_versions(self) -> List[DatasetVersion]:
        """List all dataset versions."""
        return list(self._versions.values())
    
    def save_dataset(self, dataset: Dataset, version_id: str) -> Path:
        """Save dataset to versioned store."""
        version = self._versions.get(version_id)
        if not version:
            raise ValueError(f"Version not found: {version_id}")
        
        save_path = self.store_path / f"{version_id}.jsonl"
        dataset.to_json(str(save_path))
        
        return save_path
    
    def load_dataset(self, version_id: str) -> Dataset:
        """Load dataset from versioned store."""
        version = self._versions.get(version_id)
        if not version:
            raise ValueError(f"Version not found: {version_id}")
        
        load_path = self.store_path / f"{version_id}.jsonl"
        from datasets import Dataset
        
        return Dataset.from_json(str(load_path))
    
    def _save_versions(self) -> None:
        """Save versions to store."""
        versions_file = self.store_path / "versions.json"
        data = {
            vid: {
                "version_id": v.version_id,
                "timestamp": v.timestamp,
                "checksum": v.checksum,
                "size": v.size,
                "metadata": v.metadata,
                "features": v.features,
            }
            for vid, v in self._versions.items()
        }
        
        with open(versions_file, "w") as f:
            json.dump(data, f, indent=2)