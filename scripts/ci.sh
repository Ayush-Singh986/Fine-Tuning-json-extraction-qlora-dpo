#!/bin/bash
# CI/CD helper script for Finr-Tuning

set -e

echo "Running CI/CD pipeline..."

# Check Python version
python3 --version

# Install dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# Run linters
echo "Running linters..."
black --check src/ scripts/ tests/
ruff check src/ scripts/ tests/
mypy src/

# Run tests
echo "Running tests..."
pytest tests/ -v --cov=finrtuning --cov-report=xml

# Validate configs
echo "Validating configurations..."
python -c "import yaml; [yaml.safe_load(open(f)) for f in ['configs/data_build.yaml', 'configs/data_sources.yaml', 'configs/dpo.yaml', 'configs/eval.yaml', 'configs/inference.yaml', 'configs/model.yaml', 'configs/sft.yaml']]"

echo "CI/CD pipeline passed!"