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