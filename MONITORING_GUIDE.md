# Monitoring Guide

## Prometheus Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'finrtuning'
    static_configs:
      - targets: ['localhost:9090']
```

## Grafana Dashboard

Import dashboard from `infrastructure/monitoring/grafana/dashboards/`

## Key Metrics

| Metric | Alert Threshold |
|--------|-----------------|
| GPU Utilization | > 90% for 5 min |
| GPU Memory | > 90% for 5 min |
| CPU Utilization | > 80% for 10 min |
| API Error Rate | > 1% for 5 min |
| P95 Latency | > 5000ms for 5 min |
| Disk Space | > 80% used |

## Alerts

Alerts are configured in `infrastructure/aws/monitoring.tf`:

- High GPU utilization
- High GPU memory
- High CPU utilization
- Low disk space