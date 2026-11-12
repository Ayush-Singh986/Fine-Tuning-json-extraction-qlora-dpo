# AWS Infrastructure for Finr-Tuning
# Multi-Model Fine-Tuning Platform

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "instance_type" {
  description = "EC2 instance type for training"
  type        = string
  default     = "g4dn.xlarge"
}

variable "instance_type_inference" {
  description = "EC2 instance type for inference"
  type        = string
  default     = "g4dn.xlarge"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "allowed_ssh_cidr_blocks" {
  description = "CIDR blocks allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_http_cidr_blocks" {
  description = "CIDR blocks allowed for HTTP access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_https_cidr_blocks" {
  description = "CIDR blocks allowed for HTTPS access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "instance_count" {
  description = "Number of training instances"
  type        = number
  default     = 1
}

variable "instance_count_inference" {
  description = "Number of inference instances"
  type        = number
  default     = 1
}

variable "ebs_volume_size" {
  description = "EBS volume size in GB"
  type        = number
  default     = 100
}

variable "ebs_volume_type" {
  description = "EBS volume type"
  type        = string
  default     = "gp3"
}

variable "ebs_volume_iops" {
  description = "EBS volume IOPS"
  type        = number
  default     = 3000
}

variable "ebs_volume_throughput" {
  description = "EBS volume throughput"
  type        = number
  default     = 125
}

variable "s3_artifact_bucket_name" {
  description = "S3 bucket name for artifacts"
  type        = string
  default     = ""
}

variable "s3_artifact_bucket_versioning" {
  description = "Enable versioning for artifact bucket"
  type        = bool
  default     = true
}

variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable CloudWatch logging"
  type        = bool
  default     = true
}

variable "enable_tracing" {
  description = "Enable X-Ray tracing"
  type        = bool
  default     = true
}

variable "enable_backup" {
  description = "Enable backup"
  type        = bool
  default     = true
}

variable "backup_vault_name" {
  description = "Backup vault name"
  type        = string
  default     = ""
}

variable "backup_plan_rules" {
  description = "Backup plan rules"
  type = list(object({
    schedule = string
    start_time = string
    start_window = string
    completion_window = string
  }))
  default = [
    {
      schedule     = "cron(0 2 ? * *)"
      start_time   = "02:00"
      start_window = "01:00"
      completion_window = "02:00"
    }
  ]
}

variable "backup_resource_selection" {
  description = "Backup resource selection"
  type = list(object({
    backup_vault_name = string
    resources         = list(string)
  }))
  default = []
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

locals {
  common_tags = merge(var.tags, {
    Environment = var.environment
    Project     = "Finr-Tuning"
  })
}

# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 4.0"

  name = "${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = true
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true
  enable_dns_support     = true
  map_public_ip_on_launch = false

  tags = local.common_tags
}

# Security Groups
resource "aws_security_group" "training" {
  name        = "${var.environment}-training-sg"
  description = "Security group for training instances"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "SSH from allowed CIDRs"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr_blocks
  }

  ingress {
    description = "Jupyter from allowed CIDRs"
    from_port   = 8888
    to_port     = 8888
    protocol    = "tcp"
    cidr_blocks = var.allowed_http_cidr_blocks
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.environment}-training-sg" })
}

resource "aws_security_group" "inference" {
  name        = "${var.environment}-inference-sg"
  description = "Security group for inference instances"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "HTTP from allowed CIDRs"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = var.allowed_http_cidr_blocks
  }

  ingress {
    description = "Prometheus from allowed CIDRs"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = var.allowed_http_cidr_blocks
  }

  ingress {
    description = "Grafana from allowed CIDRs"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = var.allowed_http_cidr_blocks
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.environment}-inference-sg" })
}

# EC2 Instances
resource "aws_instance" "training" {
  count = var.instance_count

  ami                    = data.aws_ami.gpu_ami.id
  instance_type          = var.instance_type
  subnet_id              = module.vpc.private_subnets[count.index % length(module.vpc.private_subnets)]
  vpc_security_group_ids = [aws_security_group.training.id]
  iam_instance_profile   = aws_iam_instance_profile.training.name
  key_name               = var.key_name

  root_block_device {
    volume_size = var.ebs_volume_size
    volume_type = var.ebs_volume_type
    iops        = var.ebs_volume_iops
    throughput  = var.ebs_volume_throughput
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-training-${count.index + 1}"
  })
}

resource "aws_instance" "inference" {
  count = var.instance_count_inference

  ami                    = data.aws_ami.gpu_ami.id
  instance_type          = var.instance_type_inference
  subnet_id              = module.vpc.private_subnets[count.index % length(module.vpc.private_subnets)]
  vpc_security_group_ids = [aws_security_group.inference.id]
  iam_instance_profile   = aws_iam_instance_profile.inference.name
  key_name               = var.key_name

  root_block_device {
    volume_size = var.ebs_volume_size
    volume_type = var.ebs_volume_type
    iops        = var.ebs_volume_iops
    throughput  = var.ebs_volume_throughput
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-inference-${count.index + 1}"
  })
}

# IAM
data "aws_iam_policy_document" "training_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "inference_assume_role" {
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
  assume_role_policy = data.aws_iam_policy_document.training_assume_role.json
}

resource "aws_iam_role" "inference" {
  name               = "${var.environment}-inference-role"
  assume_role_policy = data.aws_iam_policy_document.inference_assume_role.json
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

# S3 Buckets
resource "aws_s3_bucket" "artifacts" {
  bucket = coalesce(var.s3_artifact_bucket_name, "${var.environment}-finrtuning-artifacts-${random_id.bucket_suffix.hex}")

  tags = merge(local.common_tags, {
    Name = "${var.environment}-artifacts"
  })
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = var.s3_artifact_bucket_versioning ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}