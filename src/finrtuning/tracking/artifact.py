"""Artifact management for Finr-Tuning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Artifact:
    """Artifact metadata."""
    
    name: str
    path: str
    type: str
    metadata: Dict[str, Any]


class ArtifactManager:
    """Artifact manager for tracking and versioning."""
    
    def __init__(self, storage_path: str | Path = "artifacts"):
        """Initialize artifact manager."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._artifacts: Dict[str, Artifact] = {}
    
    def register(
        self,
        name: str,
        path: str | Path,
        artifact_type: str,
        metadata: Dict[str, Any] | None = None,
    ) -> Artifact:
        """Register a new artifact."""
        artifact = Artifact(
            name=name,
            path=str(path),
            type=artifact_type,
            metadata=metadata or {},
        )
        self._artifacts[name] = artifact
        return artifact
    
    def get(self, name: str) -> Optional[Artifact]:
        """Get artifact by name."""
        return self._artifacts.get(name)
    
    def list(self) -> List[Artifact]:
        """List all artifacts."""
        return list(self._artifacts.values())