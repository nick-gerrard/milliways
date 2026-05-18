#!/bin/bash
set -e

# Run once on a fresh server as root (or with sudo)
# Usage: bash setup.sh

# Install dependencies
apt-get update
apt-get install -y nginx nodejs npm python3 python3-pip certbot python3-certbot-nginx

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Create deploy user if it doesn't exist
id -u deploy &>/dev/null || useradd -m -s /bin/bash deploy

# Clone repo
sudo -u deploy git clone git@github.com:nickgerrard/milliways.git /home/deploy/milliways

# Install backend dependencies and run migrations
cd /home/deploy/milliways
sudo -u deploy uv sync
cd backend
sudo -u deploy uv run alembic upgrade head

# Install frontend dependencies and build
cd /home/deploy/milliways/frontend
sudo -u deploy npm ci
sudo -u deploy npm run build

# Install systemd services
cp /home/deploy/milliways/server/milliways-api.service /etc/systemd/system/
cp /home/deploy/milliways/server/milliways-frontend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable milliways-api milliways-frontend
systemctl start milliways-api milliways-frontend

# Install nginx config
cp /home/deploy/milliways/server/nginx.conf /etc/nginx/sites-available/milliways
ln -sf /etc/nginx/sites-available/milliways /etc/nginx/sites-enabled/milliways
# rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# Issue TLS certificates (requires DNS to be pointed at this server first)
certbot --nginx -d milliways.nickgerrard.dev -d api.milliways.nickgerrard.dev --non-interactive --agree-tos -m nick.gerrard16@gmail.com

echo "Done. Check status with: systemctl status milliways-api milliways-frontend"
