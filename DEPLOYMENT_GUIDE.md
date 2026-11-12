# Deployment Guide

## Quick Start

```bash
# Build Docker images
docker build -t finrtuning/training:latest .
docker build -t finrtuning/inference:latest -f docker/inference/Dockerfile .

# Start inference server
docker run -p 8000:8000 finrtuning/inference:latest
```

## AWS Deployment

```bash
# Initialize Terraform
cd infrastructure/aws
terraform init

# Plan deployment
terraform plan -var environment=production

# Apply deployment
terraform apply -var environment=production
```

## Model Serving

### FastAPI Server

```bash
# Start server
python -m finrtuning.serving.api --port 8000

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/models
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"model_name": "qwen2.5-1.5b", "prompt": "Test"}'
```

### vLLM Backend

```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct

# Test with OpenAI client
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## Production Checklist

- [ ] SSL/TLS configured
- [ ] Rate limiting enabled
- [ ] Authentication configured
- [ ] Monitoring dashboards created
- [ ] Alerts configured
- [ ] Backup strategy in place
- [ ] CI/CD pipeline tested
- [ ] Documentation updated