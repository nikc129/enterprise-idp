# Enterprise Internal Developer Platform (IDP)

A production-inspired **Internal Developer Platform (IDP)** built on AWS using **Terraform**, **Docker**, and modern DevOps practices.

This project demonstrates how Platform Engineering teams automate infrastructure provisioning, application deployment, monitoring, and developer self-service while remaining AWS Free Tier friendly.

---

## Project Goals

- Infrastructure as Code using Terraform
- Modular AWS architecture
- Production-style networking
- Docker-based application platform
- CI/CD automation
- Monitoring & Logging
- Developer self-service platform
- AI-assisted Platform Engineering

---

# Architecture

```
                 Internet
                     │
                     ▼
               EC2 Instance
                     │
              Docker Engine
                     │
              Docker Compose
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      Nginx Reverse Proxy   Docker Network
          │                     │
     ┌────┴─────┐          ┌────┴─────┐
     ▼          ▼          ▼          ▼
 Frontend   Backend    Future DB   Monitoring
```

---

# Repository Structure

```
enterprise-idp/

├── docs/
│
├── scripts/
│   └── user-data.sh
│
├── docker/
│   ├── docker-compose.yml
│   ├── nginx/
│   ├── frontend/
│   └── backend/
│
├── terraform/
│   ├── bootstrap/
│   ├── environments/
│   │   ├── dev/
│   │   ├── stage/
│   │   └── prod/
│   │
│   └── modules/
│       ├── ec2/
│       ├── iam/
│       ├── networking/
│       ├── security-group/
│       └── vpc/
│
├── .gitignore
└── README.md
```

---

# Technology Stack

## Cloud

- AWS EC2
- Amazon VPC
- IAM
- Security Groups
- Route Tables
- Internet Gateway
- NAT Gateway

## Infrastructure

- Terraform

## Containers

- Docker
- Docker Compose
- Nginx

## Version Control

- Git
- GitHub

---

# Completed Modules

## Module 1 — Infrastructure Foundation

- Remote Terraform State (S3)
- State Locking (DynamoDB)
- Custom VPC
- Public & Private Subnets
- Internet Gateway
- NAT Gateway
- Route Tables
- Security Groups
- IAM Roles
- Modular Terraform Structure

**Status:** ✅ Completed

---

## Module 2 — Compute Platform

- Ubuntu EC2 Instance
- IAM Instance Profile
- User Data Bootstrap
- Docker Installation
- Docker Compose Installation
- Git Installation
- AWS CLI Installation
- Docker Platform
- Reverse Proxy using Nginx
- Multi-container Architecture

**Status:** ✅ Completed

---

# Upcoming Modules

## Module 3 — CI/CD

- GitHub Actions
- Docker Image Build
- Automatic Deployment
- Zero-downtime Deployment

---

## Module 4 — Monitoring

- Prometheus
- Grafana
- Node Exporter
- cAdvisor
- Alertmanager

---

## Module 5 — Developer Portal

- Internal Developer Portal
- Service Catalog
- Self-service Templates

---

## Module 6 — AI Platform Assistant

- AI-powered troubleshooting
- Infrastructure recommendations
- Automated documentation
- Developer assistance

---

# Current Progress

| Module | Status |
|----------|--------|
| Infrastructure | ✅ |
| Compute Platform | ✅ |
| CI/CD | ⬜ |
| Monitoring | ⬜ |
| Developer Portal | ⬜ |
| AI Assistant | ⬜ |

---

# Current Features

- Infrastructure as Code
- Modular Terraform
- Secure AWS Networking
- EC2 Compute Platform
- Docker Engine
- Docker Compose
- Reverse Proxy
- Enterprise Folder Structure
- Production-ready Project Organization

---

# Future Improvements

- SSL using Let's Encrypt
- Auto Scaling
- Load Balancer
- Private Container Registry (ECR)
- Kubernetes (EKS Version)
- Observability Stack
- Cost Monitoring
- Policy as Code
- GitOps

---

# Learning Outcomes

This project demonstrates practical experience with:

- AWS Infrastructure
- Platform Engineering
- DevOps
- Docker
- Infrastructure as Code
- Cloud Security
- Networking
- CI/CD
- Monitoring
- Enterprise Project Architecture

---

## Author

**Nikhil Chary**

Enterprise Internal Developer Platform (IDP)
Built for learning Platform Engineering, Cloud Infrastructure, and DevOps using AWS Free Tier.