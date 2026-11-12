# Variables

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

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
  default     = ""
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