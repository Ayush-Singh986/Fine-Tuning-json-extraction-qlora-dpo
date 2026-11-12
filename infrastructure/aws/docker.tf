# Docker Build Configuration

resource "null_resource" "docker_build_training" {
  provisioner "local-exec" {
    command = <<EOT
      cd ${path.module}/../../docker/train
      docker build -t ${var.environment}-training:latest .
      docker tag ${var.environment}-training:latest ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.environment}-training:latest
      aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com
      docker push ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.environment}-training:latest
    EOT
  }

  depends_on = [aws_ecr_repository.training]
}

resource "null_resource" "docker_build_inference" {
  provisioner "local-exec" {
    command = <<EOT
      cd ${path.module}/../../docker/inference
      docker build -t ${var.environment}-inference:latest .
      docker tag ${var.environment}-inference:latest ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.environment}-inference:latest
      aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com
      docker push ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.environment}-inference:latest
    EOT
  }

  depends_on = [aws_ecr_repository.inference]
}

data "aws_caller_identity" "current" {}