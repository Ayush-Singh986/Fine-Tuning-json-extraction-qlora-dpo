# Outputs

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "training_instance_ids" {
  description = "Training instance IDs"
  value       = aws_instance.training[*].id
}

output "inference_instance_ids" {
  description = "Inference instance IDs"
  value       = aws_instance.inference[*].id
}

output "training_instance_public_ips" {
  description = "Training instance public IPs"
  value       = aws_instance.training[*].public_ip
}

output "inference_instance_public_ips" {
  description = "Inference instance public IPs"
  value       = aws_instance.inference[*].public_ip
}

output "training_instance_private_ips" {
  description = "Training instance private IPs"
  value       = aws_instance.training[*].private_ip
}

output "inference_instance_private_ips" {
  description = "Inference instance private IPs"
  value       = aws_instance.inference[*].private_ip
}

output "s3_artifacts_bucket_name" {
  description = "S3 artifacts bucket name"
  value       = aws_s3_bucket.artifacts.id
}

output "ecr_training_repository_url" {
  description = "ECR training repository URL"
  value       = aws_ecr_repository.training.repository_url
}

output "ecr_inference_repository_url" {
  description = "ECR inference repository URL"
  value       = aws_ecr_repository.inference.repository_url
}

output "training_security_group_id" {
  description = "Training security group ID"
  value       = aws_security_group.training.id
}

output "inference_security_group_id" {
  description = "Inference security group ID"
  value       = aws_security_group.inference.id
}