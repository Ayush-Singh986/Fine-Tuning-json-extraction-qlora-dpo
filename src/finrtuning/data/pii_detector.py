"""PII detection and redaction utilities."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PIIEntity:
    """Detected PII entity."""
    
    entity_type: str
    start: int
    end: int
    text: str


class PIIDetector:
    """PII detection and redaction."""
    
    # Common PII patterns
    PATTERNS = {
        "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
        "phone": r"\b\+?[\d\s\-\(\)]{10,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "url": r"https?://[^\s]+",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "date": r"\b\d{4}-\d{2}-\d{2}\b",
    }
    
    def __init__(self, redact: bool = True, redact_char: str = "*"):
        """Initialize PII detector."""
        self.redact = redact
        self.redact_char = redact_char
    
    def detect(self, text: str) -> List[PIIEntity]:
        """Detect PII in text."""
        entities = []
        
        for entity_type, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                entities.append(PIIEntity(
                    entity_type=entity_type,
                    start=match.start(),
                    end=match.end(),
                    text=match.group(),
                ))
        
        # Sort by position
        entities.sort(key=lambda x: x.start)
        return entities
    
    def redact_text(self, text: str) -> str:
        """Redact PII from text."""
        entities = self.detect(text)
        
        # Process from end to avoid index shifting
        result = text
        for entity in reversed(entities):
            replacement = self.redact_char * len(entity.text)
            result = result[:entity.start] + replacement + result[entity.end:]
        
        return result
    
    def check_dataset(self, dataset: Any) -> Dict[str, Any]:
        """Check dataset for PII."""
        results = {
            "total_rows": 0,
            "rows_with_pii": 0,
            "pii_types": {},
            "redacted": [],
        }
        
        for i in range(len(dataset)):
            row = dataset[i]
            results["total_rows"] += 1
            
            row_has_pii = False
            for field, value in row.items():
                if isinstance(value, str):
                    entities = self.detect(value)
                    if entities:
                        row_has_pii = True
                        results["rows_with_pii"] += 1
                        
                        for entity in entities:
                            pii_type = entity.entity_type
                            if pii_type not in results["pii_types"]:
                                results["pii_types"][pii_type] = 0
                            results["pii_types"][pii_type] += 1
        
        return results