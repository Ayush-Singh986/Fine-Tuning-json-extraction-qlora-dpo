# EC2 Instance Configuration

data "aws_ami" "gpu_ami" {
  most_recent = true
  owners      = ["898012104705"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

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

output "training_instance_ids" {
  value = aws_instance.training[*].id
}

output "inference_instance_ids" {
  value = aws_instance.inference[*].id
}

output "training_instance_public_ips" {
  value = aws_instance.training[*].public_ip
}

output "inference_instance_public_ips" {
  value = aws_instance.inference[*].public_ip
}

output "training_instance_private_ips" {
  value = aws_instance.training[*].private_ip
}

output "inference_instance_private_ips" {
  value = aws_instance.inference[*].private_ip
}