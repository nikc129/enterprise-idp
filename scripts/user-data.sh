#!/bin/bash

#############################################################
# Enterprise IDP
# EC2 Bootstrap Script
#
# This script runs automatically on the first boot
# of the EC2 instance.
#############################################################

set -e

echo "Starting bootstrap..." > /var/log/user-data.log

#############################################################
# Update Ubuntu
#############################################################

apt-get update -y

apt-get upgrade -y

#############################################################
# Install packages
#############################################################

apt-get install -y \
    docker.io \
    git \
    unzip \
    curl \
    wget

#############################################################
# Enable Docker
#############################################################

systemctl enable docker

systemctl start docker

#############################################################
# Allow ubuntu user to run Docker
#############################################################

usermod -aG docker ubuntu

#############################################################
# Install Docker Compose
#############################################################

mkdir -p /usr/local/lib/docker/cli-plugins

curl -SL \
https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
-o /usr/local/lib/docker/cli-plugins/docker-compose

chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

#############################################################
# Install AWS CLI v2
#############################################################

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
-o "awscliv2.zip"

unzip awscliv2.zip

./aws/install

#############################################################
# Create project directory
#############################################################

mkdir -p /opt/enterprise-idp

chown ubuntu:ubuntu /opt/enterprise-idp

#############################################################
# Verify installations
#############################################################

docker --version >> /var/log/user-data.log

docker compose version >> /var/log/user-data.log

aws --version >> /var/log/user-data.log

echo "Bootstrap Complete" >> /var/log/user-data.log
