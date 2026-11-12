#!/bin/bash
# Monitoring setup script for Finr-Tuning

# Install Prometheus node exporter
curl -LO https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter.linux-amd64.tar.gz
tar xzf node_exporter.linux-amd64.tar.gz
sudo cp node_exporter-*/node_exporter /usr/local/bin/

# Install Grafana
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O /usr/share/keyrings/grafana-keyring https://apt.grafana.com/gpg.key
echo "deb [signed-by=/usr/share/keyrings/grafana-keyring] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana

# Start services
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

echo "Monitoring setup complete"