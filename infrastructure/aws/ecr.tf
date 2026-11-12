# ECR Repository Configuration

resource "aws_ecr_repository" "training" {
  name = "${var.environment}-training"

  tags = merge(local.common_tags, {
    Name = "${var.environment}-training"
  })
}

resource "aws_ecr_repository" "inference" {
  name = "${var.environment}-inference"

  tags = merge(local.common_tags, {
    Name = "${var.environment}-inference"
  })
}

resource "aws_ecr_repository" "monitoring" {
  name = "${var.environment}-monitoring"

  tags = merge(local.common_tags, {
    Name = "${var.environment}-monitoring"
  })
}

resource "aws_ecr_lifecycle_policy" "training" {
  repository = aws_ecr_repository.training.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expire old images"
        selection = {
          tagStatus   = "untagged"
          countType   = "countOnly"
          countNumber = 100
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_ecr_lifecycle_policy" "inference" {
  repository = aws_ecr_repository.inference.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expire old images"
        selection = {
          tagStatus   = "untagged"
          countType   = "countOnly"
          countNumber = 100
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_ecr_lifecycle_policy" "monitoring" {
  repository = aws_ecr_repository.monitoring.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expire old images"
        selection = {
          tagStatus   = "untagged"
          countType   = "countOnly"
          countNumber = 100
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}