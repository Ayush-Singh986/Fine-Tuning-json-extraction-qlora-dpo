# Architecture Documentation

## Overview

Finr-Tuning is a modular, extensible ML engineering platform built for multi-model fine-tuning workflows. This document describes the system architecture, design patterns, and component interactions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Finr-Tuning Platform                             │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Data       │  │  Model      │  │  Training   │  │  Evaluation │ │
│  │  Engineering│  │  Registry   │  │  Pipeline   │  │  Framework  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Tracking   │  │  Serving    │  │  Leaderboard│  │  Monitor    │ │
│  │  (MLflow)   │  │  (FastAPI)  │  │  & Selection│  │  (Prometheus│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Module Architecture

### Data Engineering Module

```
src/finrtuning/data/
├── __init__.py
├── pipeline.py          # Data pipeline operations
├── validation.py        # Schema, PII, leakage detection
└── versioning.py        # Dataset versioning with checksums
```

**Key Classes:**
- `DataPipeline` - Data loading, splitting, and saving
- `DatasetValidator` - Schema, PII, and leakage detection
- `DatasetVersioning` - Version control for datasets

### Model Registry Module

```
src/finrtuning/models/
├── __init__.py
├── registry.py          # Model registration and loading
├── loader.py            # Model loading with adapters
└── adapters/
    ├── __init__.py
    ├── base.py          # Base adapter interface
    ├── qwen.py          # Qwen-specific adapter
    ├── phi.py           # Phi-specific adapter
    └── granite.py       # Granite-specific adapter
```

**Key Classes:**
- `ModelRegistry` - Configuration-driven model registry
- `ModelLoader` - Model loading with adapter support
- `BaseAdapter` - Architecture-specific adapter interface

### Training Module

```
src/finrtuning/training/
├── __init__.py
├── sft.py               # SFT training with QLoRA
├── dpo.py               # DPO training
└── qlora.py             # QLoRA configuration
```

### Evaluation Module

```
src/finrtuning/evaluation/
├── __init__.py
├── runner.py            # Unified evaluation runner
├── comparative.py       # Multi-model comparison
└── confidence.py        # Confidence interval calculation
```

### Tracking Module

```
src/finrtuning/tracking/
├── __init__.py
├── mlflow.py            # MLflow integration
├── s3.py                # S3 artifact storage
└── artifact.py          # Artifact management
```

### Serving Module

```
src/finrtuning/serving/
├── __init__.py
├── api.py               # FastAPI application
├── endpoints/           # API endpoints
│   ├── health.py
│   ├── models.py
│   ├── predict.py
│   └── metrics.py
└── middleware/          # Middleware
    ├── auth.py
    └── rate_limit.py
```

### Leaderboard Module

```
src/finrtuning/leaderboard/
├── __init__.py
├── generator.py         # Leaderboard generation
└── scorer.py            # Scoring algorithm
```

## Data Flow

### Training Pipeline

```
Data Sources → Data Pipeline → Validation → Splitting
    ↓
Training (SFT → DPO) → Evaluation → Leaderboard
    ↓
Model Selection → Production Deploy
```

### Inference Pipeline

```
API Request → Model Loading → Prediction → Response
                ↓
          (vLLM Backend)
```

## Configuration System

The configuration system uses Pydantic schemas for type-safe configuration:

```python
# Example configuration
from finrtuning.config.base import ModelConfig, TrainingConfig

model_config = ModelConfig(
    name="qwen2.5-1.5b-instruct",
    huggingface_id="Qwen/Qwen2.5-1.5B-Instruct",
    max_seq_length=2048,
    gpu_memory_gb=16,
)

training_config = TrainingConfig(
    seed=42,
    num_train_epochs=3,
    use_qlora=True,
    lora_r=16,
    lora_alpha=32,
)
```

## Extension Points

### Adding a New Model

1. Register in `ModelRegistry`
2. Create architecture-specific adapter
3. Test training pipeline
4. Update documentation

### Adding a New Metric

1. Implement metric in `evaluation/metrics.py`
2. Register in evaluation runner
3. Update leaderboard scoring

## Security

- No model weights committed to Git
- Secrets managed via environment variables
- IAM least-privilege access
- VPC isolation for GPU instances

## Scalability

- Stateless API servers
- S3 for artifact storage
- GPU instance scaling
- Distributed training support