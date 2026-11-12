"""S3 artifact storage for Finr-Tuning."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional


class S3Storage:
    """S3 storage for artifacts."""
    
    def __init__(self, bucket_name: str, prefix: str = "artifacts"):
        """Initialize S3 storage."""
        self.bucket_name = bucket_name
        self.prefix = prefix
        self._client = None
    
    @property
    def client(self):
        """Lazy import boto3 client."""
        if self._client is None:
            import boto3
            self._client = boto3.client("s3")
        return self._client
    
    def upload_file(self, local_path: str | Path, s3_key: str):
        """Upload a file to S3."""
        self.client.upload_file(
            str(local_path), self.bucket_name, f"{self.prefix}/{s3_key}"
        )
    
    def download_file(self, s3_key: str, local_path: str | Path):
        """Download a file from S3."""
        self.client.download_file(
            self.bucket_name, f"{self.prefix}/{s3_key}", str(local_path)
        )
    
    def list_files(self, prefix: str = "") -> List[str]:
        """List files in S3."""
        response = self.client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=f"{self.prefix}/{prefix}",
        )
        return [
            obj["Key"]
            for obj in response.get("Contents", [])
            if obj["Key"] != f"{self.prefix}/"
        ]