# IAM Configuration

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "training" {
  name               = "${var.environment}-training-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role" "inference" {
  name               = "${var.environment}-inference-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "training_s3" {
  role       = aws_iam_role.training.name
  policy_arn = aws_iam_policy.training_s3.arn
}

resource "aws_iam_role_policy_attachment" "inference_s3" {
  role       = aws_iam_role.inference.name
  policy_arn = aws_iam_policy.inference_s3.arn
}

resource "aws_iam_role_policy_attachment" "training_logging" {
  role       = aws_iam_role.training.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_role_policy_attachment" "inference_logging" {
  role       = aws_iam_role.inference.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_role_policy_attachment" "training_ecr" {
  role       = aws_iam_role.training.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "inference_ecr" {
  role       = aws_iam_role.inference.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_policy" "training_s3" {
  name        = "${var.environment}-training-s3"
  description = "Policy for training S3 access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
        ]
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "inference_s3" {
  name        = "${var.environment}-inference-s3"
  description = "Policy for inference S3 access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_instance_profile" "training" {
  name = "${var.environment}-training-profile"
  role = aws_iam_role.training.name
}

resource "aws_iam_instance_profile" "inference" {
  name = "${var.environment}-inference-profile"
  role = aws_iam_role.inference.name
}