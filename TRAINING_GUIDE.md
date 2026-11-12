# Training Guide

## Quick Start

```bash
# Build dataset manifests
python scripts/build_dataset_manifests.py --profile full

# Train SFT (QLoRA)
python scripts/train_sft.py --config configs/sft.yaml --profile colab_full --run-name sft-full

# Build preference pairs
python scripts/build_preference_pairs.py --config configs/dpo.yaml --profile colab_full --run-name dpo-full

# Train DPO
python scripts/train_dpo.py --config configs/dpo.yaml --profile colab_full --run-name dpo-full

# Evaluate
python scripts/eval_model.py --config configs/eval.yaml --run-name baseline-qwen2.5-1.5b
```

## Training Profiles

| Profile | Use Case | Batch Size | Steps |
|---------|----------|------------|-------|
| `dev` | Development/smoke test | 1 x 2 = 2 | 5 steps |
| `colab_full` | Colab training | 1 x 8 = 8 | 3 epochs |
| `large_gpu_full` | Large GPU | 4 x 4 = 16 | 4 epochs |

## Configuration

Edit `configs/sft.yaml` or `configs/dpo.yaml`:

```yaml
lora:
  r: 16          # LoRA rank
  alpha: 32      # LoRA alpha
  dropout: 0.05  # LoRA dropout

training:
  num_train_epochs: 3
  per_device_train_batch_size: 1
  gradient_accumulation_steps: 8
  learning_rate: 2.0e-4
```

## Monitoring

Trainings logs metrics to:
- Terminal output
- `artifacts/metrics/` JSON files
- MLflow (if configured)

## Resume Training

```bash
# Resume from checkpoint
python scripts/train_sft.py \
  --config configs/sft.yaml \
  --profile full \
  --resume-from-checkpoint artifacts/checkpoints/latest
```

## GPU Memory Optimization

1. Enable QLoRA: `quantization.enabled: true`
2. Use gradient checkpointing
3. Reduce batch size
4. Use smaller sequence length