# Troubleshooting Guide

## Common Issues

### Issue: CUDA Out of Memory

**Solution:**
- Reduce `per_device_train_batch_size` in configs
- Enable gradient checkpointing
- Use smaller model or sequence length
- Enable QLoRA quantization

### Issue: Model Not Loading

**Solution:**
- Check Hugging Face token access
- Verify model identifier format
- Check internet connectivity
- Try with `trust_remote_code=True`

### Issue: Datasets Not Found

**Solution:**
- Run `python scripts/build_dataset_manifests.py --profile full`
- Verify data paths in configs
- Check file permissions

### Issue: API Service Not Starting

**Solution:**
- Check port 8000 is available
- Verify model is loaded
- Check inference config
- Review logs for errors

### Issue: Tests Failing

**Solution:**
- Run with `pytest tests/ -v --tb=short`
- Check dependencies: `pip install -e ".[dev]"`
- Verify environment: `python -c "import finrtuning"`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_data_build.py -v

# Run with coverage
pytest tests/ -v --cov=finrtuning
```

## Logs

Logs are written to:
- Training logs: `runtime/logs/`
- Inference logs: `runtime/logs/inference/`
- MLflow logs: `mlruns/`

## Support

- GitHub Issues: https://github.com/Ayush-Singh986/json-extraction-qlora-dpo/issues
- Documentation: https://github.com/Ayush-Singh986/json-extraction-qlora-dpo/wiki