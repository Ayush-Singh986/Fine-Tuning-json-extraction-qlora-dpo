# Monitoring Docker image for Finr-Tuning
FROM grafana/grafana:latest

# Add Prometheus datasource
COPY infrastructure/monitoring/prometheus/datasources.yml /etc/grafana/provisioning/datasources/
COPY infrastructure/monitoring/grafana/dashboards.yml /etc/grafana/provisioning/dashboards/

EXPOSE 3000