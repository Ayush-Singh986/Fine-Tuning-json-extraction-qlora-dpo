#!/bin/bash
# Deployment script for Finr-Tuning

set -e

ENVIRONMENT=${1:-production}
AWS_REGION=${AWS_REGION:-us-east-1}

echo "Deploying to $ENVIRONMENT environment..."

# Configure AWS credentials
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set region $AWS_REGION

# Build Docker images
echo "Building Docker images..."
docker build -t finrtuning/training:${CI_COMMIT_SHA} .
docker build -t finrtuning/inference:${CI_COMMIT_SHA} -f docker/inference/Dockerfile .

# Push to ECR
ECR_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
docker tag finrtuning/training:${CI_COMMIT_SHA} ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/finrtuning/training:${CI_COMMIT_SHA}
docker push ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/finrtuning/training:${CI_COMMIT_SHA}

docker tag finrtuning/inference:${CI_COMMIT_SHA} ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/finrtuning/inference:${CI_COMMIT_SHA}
docker push ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/finrtuning/inference:${CI_COMMIT_SHA}

# Deploy to EC2
echo "Deploying to EC2..."
aws ecs update-service --cluster finrtuning-${ENVIRONMENT} --service finrtuning --force-new-deployment

echo "Deployment complete!"