"""Dataset validation with PII detection and leakage checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import json
import re

from datasets import Dataset


@dataclass
class ValidationIssue:
    """Single validation issue."""
    
    row_index: int
    field: str
    issue_type: str
    message: str


@dataclass
class ValidationResult:
    """Dataset validation result."""
    
    is_valid: bool
    issues: List[ValidationIssue]
    statistics: Dict[str, Any]


class DatasetValidator:
    """Dataset validator with PII detection and leakage checks."""
    
    # Common PII patterns
    PII_PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\+?[\d\s\-\(\)]{10,}",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "url": r"https?://[^\s]+",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    }
    
    def __init__(self, config: Dict[str, Any] | None = None):
        """Initialize dataset validator."""
        self.config = config or {}
        self.issues: List[ValidationIssue] = []
        self.statistics: Dict[str, Any] = {}
    
    def validate_schema(
        self, dataset: Dataset, schema: Dict[str, Any]
    ) -> ValidationResult:
        """Validate dataset against schema."""
        issues = []
        
        for row_idx in range(len(dataset)):
            row = dataset[row_idx]
            for field, field_schema in schema.items():
                if field not in row:
                    issues.append(
                        ValidationIssue(
                            row_index=row_idx,
                            field=field,
                            issue_type="missing_field",
                            message=f"Missing required field: {field}",
                        )
                    )
                    continue
                
                value = row[field]
                if field_schema.get("required") and value is None:
                    issues.append(
                        ValidationIssue(
                            row_index=row_idx,
                            field=field,
                            issue_type="empty_value",
                            message=f"Required field is empty: {field}",
                        )
                    )
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            statistics={"total_rows": len(dataset)},
        )
    
    def detect_pii(self, dataset: Dataset) -> ValidationResult:
        """Detect PII in dataset."""
        issues = []
        
        for row_idx in range(len(dataset)):
            row = dataset[row_idx]
            for field, value in row.items():
                if not isinstance(value, str):
                    continue
                
                for pii_type, pattern in self.PII_PATTERNS.items():
                    if re.search(pattern, value):
                        issues.append(
                            ValidationIssue(
                                row_index=row_idx,
                                field=field,
                                issue_type=f"pii_detected_{pii_type}",
                                message=f"PII pattern '{pii_type}' detected in field '{field}'",
                            )
                        )
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            statistics={"pii_count": len(issues)},
        )
    
    def detect_duplicates(self, dataset: Dataset) -> ValidationResult:
        """Detect duplicate records."""
        seen: Set[str] = set()
        issues = []
        
        for row_idx in range(len(dataset)):
            row = dataset[row_idx]
            row_key = json.dumps(row, sort_keys=True)
            
            if row_key in seen:
                issues.append(
                    ValidationIssue(
                        row_index=row_idx,
                        field="full_row",
                        issue_type="duplicate",
                        message="Duplicate record detected",
                    )
                )
            seen.add(row_key)
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            statistics={"duplicate_count": len(issues)},
        )
    
    def detect_leakage(
        self, dataset: Dataset, reference_dataset: Dataset
    ) -> ValidationResult:
        """Detect data leakage between datasets."""
        issues = []
        
        # Create set of reference records
        reference_keys: Set[str] = set()
        for row in reference_dataset:
            reference_keys.add(json.dumps(row, sort_keys=True))
        
        # Check for leakage
        for row_idx in range(len(dataset)):
            row = dataset[row_idx]
            row_key = json.dumps(row, sort_keys=True)
            
            if row_key in reference_keys:
                issues.append(
                    ValidationIssue(
                        row_index=row_idx,
                        field="full_row",
                        issue_type="data_leakage",
                        message="Record appears in reference dataset (potential leakage)",
                    )
                )
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            statistics={"leakage_count": len(issues)},
        )
    
    def get_statistics(self, dataset: Dataset) -> Dict[str, Any]:
        """Compute dataset statistics."""
        stats = {"total_rows": len(dataset)}
        
        if len(dataset) > 0:
            # Get field types
            sample = dataset[0]
            stats["fields"] = list(sample.keys())
            stats["field_types"] = {
                k: type(v).__name__ for k, v in sample.items()
            }
        
        return stats