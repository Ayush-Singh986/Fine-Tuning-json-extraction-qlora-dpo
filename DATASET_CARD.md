# Dataset Card

## Overview

Finr-Tuning uses structured JSON extraction datasets for fine-tuning language models on support-ticket extraction tasks.

## Dataset Statistics

| Split | Size | Source |
|-------|------|--------|
| Train | 80%  | CFPB + Customer Support |
| Validation | 10% | CFPB + Customer Support |
| Test | 10% | CFPB + Customer Support |

## Schema

The extraction schema follows the `SupportTicketExtraction` format:

```python
{
    "summary": str,                    # Issue summary
    "issue_category": str,            # Primary category
    "priority": str,                  # Urgency level
    "product_area": str,              # Product surface
    "customer": {                     # Customer metadata
        "name": str | None,
        "account_id": str | None,
        "plan_tier": str | None
    },
    "sentiment": str,                 # Customer sentiment
    "requires_human_followup": bool,  # Human action needed
    "actions_requested": List[str]    # Requested actions
}
```

## Data Sources

1. **Consumer Financial Protection Bureau (CFPB)** - Financial complaint data
2. **Customer Support Tickets** - General support ticket data
3. **Fixtures** - Small dataset for development/testing

## Data Quality

- Schema compliance validation
- PII detection and redaction
- Duplicate removal
- Leakage detection between splits
- Near-duplicate detection

## Versioning

Datasets are versioned with SHA256 checksums for reproducibility.

## License

Public domain / Open data sources.