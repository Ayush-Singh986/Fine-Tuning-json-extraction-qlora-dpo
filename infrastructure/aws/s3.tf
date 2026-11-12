# S3 Bucket Configuration

resource "aws_s3_bucket" "mlflow" {
  bucket = "${var.environment}-mlflow-${random_id.bucket_suffix.hex}"

  tags = merge(local.common_tags, {
    Name = "${var.environment}-mlflow"
  })
}

resource "aws_s3_bucket_versioning" "mlflow" {
  bucket = aws_s3_bucket.mlflow.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "mlflow" {
  bucket = aws_s3_bucket.mlflow.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "docker_images" {
  bucket = "${var.environment}-docker-images-${random_id.bucket_suffix.hex}"

  tags = merge(local.common_tags, {
    Name = "${var.environment}-docker-images"
  })
}

resource "aws_s3_bucket_versioning" "docker_images" {
  bucket = aws_s3_bucket.docker_images.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "docker_images" {
  bucket = aws_s3_bucket.docker_images.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}