# Evaluation Guide

## Quick Start

```bash
# Evaluate baseline model
python scripts/eval_model.py --config configs/eval.yaml --run-name baseline-qwen2.5-1.5b

# Evaluate trained models
python scripts/eval_model.py --config configs/eval.yaml --run-name sft-full-colab

# Compare stages
python scripts/compare_stages.py --run-name comparison
```

## Metrics

| Metric | Description |
|--------|-------------|
| `json_validity` | Percentage of valid JSON outputs |
| `schema_pass` | Percentage passing schema validation |
| `micro_f1` | Micro-averaged F1 score |
| `macro_f1` | Macro-averaged F1 score |
| `p50_latency_ms` | 50th percentile latency |
| `p95_latency_ms` | 95th percentile latency |

## Confidence Intervals

Evaluation runs with 3 seeds by default for confidence intervals.

## Comparison Reports

```bash
python scripts/compare_stages.py \
  --config configs/eval.yaml \
  --run-name stage_comparison \
  --baseline baseline-qwen2.5-1.5b \
  --sft sft-full-colab \
  --dpo dpo-full-colab
```