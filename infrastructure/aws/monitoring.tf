# Monitoring Configuration

resource "aws_cloudwatch_metric_alarm" "gpu_utilization" {
  count = var.instance_count + var.instance_count_inference

  alarm_name          = "${var.environment}-gpu-utilization-alarm-${count.index}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "GPUUtilization"
  namespace           = "CWAgent"
  period              = 300
  statistic           = "Average"
  threshold           = 90
  alarm_description   = "This metric monitors GPU utilization"

  dimensions = {
    InstanceId = count.index < var.instance_count ? aws_instance.training[count.index].id : aws_instance.inference[count.index - var.instance_count].id
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-gpu-utilization-alarm-${count.index}"
  })
}

resource "aws_cloudwatch_metric_alarm" "gpu_memory" {
  count = var.instance_count + var.instance_count_inference

  alarm_name          = "${var.environment}-gpu-memory-alarm-${count.index}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "GPUMemoryUtilization"
  namespace           = "CWAgent"
  period              = 300
  statistic           = "Average"
  threshold           = 90
  alarm_description   = "This metric monitors GPU memory utilization"

  dimensions = {
    InstanceId = count.index < var.instance_count ? aws_instance.training[count.index].id : aws_instance.inference[count.index - var.instance_count].id
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-gpu-memory-alarm-${count.index}"
  })
}

resource "aws_cloudwatch_metric_alarm" "cpu_utilization" {
  count = var.instance_count + var.instance_count_inference

  alarm_name          = "${var.environment}-cpu-utilization-alarm-${count.index}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "This metric monitors CPU utilization"

  dimensions = {
    InstanceId = count.index < var.instance_count ? aws_instance.training[count.index].id : aws_instance.inference[count.index - var.instance_count].id
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-cpu-utilization-alarm-${count.index}"
  })
}

resource "aws_cloudwatch_metric_alarm" "disk_space" {
  count = var.instance_count + var.instance_count_inference

  alarm_name          = "${var.environment}-disk-space-alarm-${count.index}"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 3
  metric_name         = "DiskSpaceUtilization"
  namespace           = "CWAgent"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "This metric monitors disk space utilization"

  dimensions = {
    InstanceId = count.index < var.instance_count ? aws_instance.training[count.index].id : aws_instance.inference[count.index - var.instance_count].id
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-disk-space-alarm-${count.index}"
  })
}