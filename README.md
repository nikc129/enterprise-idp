# Enterprise Internal Developer Platform (IDP)

> **A self-service Internal Developer Platform that enables developers to provision cloud infrastructure and deploy applications with a single click using AWS, Terraform, Kubernetes, and GitOps.**

---

# Overview

Modern development teams spend significant time manually creating infrastructure, configuring cloud resources, setting up Kubernetes clusters, managing CI/CD pipelines, and configuring monitoring before they can deploy an application.

The **Enterprise Internal Developer Platform (IDP)** aims to eliminate these repetitive tasks by providing a centralized self-service platform where developers can request infrastructure and deploy applications automatically.

Instead of manually configuring AWS resources, developers simply fill out a deployment form in the portal. The platform provisions infrastructure, deploys applications, configures monitoring, and manages the deployment lifecycle automatically.

---

# Problem Statement

Provisioning production-ready infrastructure requires multiple manual steps:

* Creating VPCs and networking
* Configuring IAM permissions
* Setting up Kubernetes clusters
* Creating container registries
* Building CI/CD pipelines
* Configuring monitoring and logging
* Managing DNS and SSL certificates

These repetitive tasks consume engineering time, introduce inconsistencies, and increase operational risk.

---

# Solution

This project provides a self-service Internal Developer Platform where developers can:

* Request infrastructure
* Deploy applications
* Manage environments
* Monitor deployments
* View logs
* Roll back releases

All infrastructure is provisioned using Infrastructure as Code (Terraform), while application deployment follows GitOps principles using Kubernetes and ArgoCD.

---

# Project Goals

* Build a production-inspired Internal Developer Platform.
* Automate AWS infrastructure provisioning.
* Implement reusable Terraform modules.
* Deploy applications to Amazon EKS.
* Automate CI/CD using GitHub Actions.
* Implement GitOps using ArgoCD.
* Integrate monitoring and centralized logging.
* Follow security best practices with IAM and Secrets Manager.
* Demonstrate Platform Engineering concepts used by modern engineering organizations.

---

# High-Level Architecture

```text
                     Developer

                         │

              Internal Developer Portal

                         │

                    Backend API

                         │

                  Terraform Engine

                         │

                AWS Infrastructure

        VPC • IAM • EKS • ECR • RDS

                         │

                 GitHub Actions

                         │

                   Docker Build

                         │

                    Amazon ECR

                         │

                      ArgoCD

                         │

                Kubernetes (EKS)

                         │

       Prometheus • Grafana • Loki
```

---

# Technology Stack

## Cloud

* Amazon Web Services (AWS)
* Amazon VPC
* Amazon EKS
* Amazon ECR
* Amazon Route53
* AWS IAM
* AWS Secrets Manager
* Amazon RDS

## Infrastructure as Code

* Terraform
* Terraform Modules
* Remote State
* S3 Backend
* DynamoDB State Locking

## Containers

* Docker
* Kubernetes
* Helm

## GitOps & CI/CD

* GitHub Actions
* ArgoCD

## Monitoring

* Prometheus
* Grafana
* Loki
* Alertmanager

## Backend

* FastAPI (planned)

## Frontend

* React (planned)

---

# Repository Structure

```text
enterprise-idp/

├── terraform/
│   ├── bootstrap/
│   ├── modules/
│   ├── environments/
│   └── root/
│
├── backend/
│
├── portal/
│
├── kubernetes/
│
├── monitoring/
│
├── argocd/
│
├── github/
│
├── docs/
│
└── README.md
```

---

# Development Roadmap

| Module                                 | Status         |
| -------------------------------------- | -------------- |
| Module 1 – Infrastructure Provisioning | 🚧 In Progress |
| Module 2 – Amazon EKS                  | ⏳ Planned      |
| Module 3 – Amazon ECR                  | ⏳ Planned      |
| Module 4 – CI/CD Pipeline              | ⏳ Planned      |
| Module 5 – GitOps with ArgoCD          | ⏳ Planned      |
| Module 6 – Monitoring                  | ⏳ Planned      |
| Module 7 – Logging                     | ⏳ Planned      |
| Module 8 – Developer Portal            | ⏳ Planned      |
| Module 9 – Backend API                 | ⏳ Planned      |
| Module 10 – Security & Policy          | ⏳ Planned      |

---

# Module 1 – Infrastructure Provisioning

## Objective

Build a reusable, modular, and production-ready AWS networking foundation using Terraform.

This module establishes the core infrastructure that all remaining modules will build upon.

---

## Module Scope

The following AWS resources will be provisioned:

* VPC
* Public Subnets
* Private Subnets
* Internet Gateway
* NAT Gateway
* Elastic IP
* Route Tables
* Route Table Associations
* Security Groups
* IAM Roles
* Remote Terraform Backend
* S3 State Bucket
* DynamoDB State Lock Table

---

## Module 1 Architecture

```text
                 AWS Account

                      │

            Terraform Backend

          S3 + DynamoDB Lock

                      │

                  VPC Module

                      │

      ┌───────────────┴───────────────┐

 Public Subnets                 Private Subnets

      │                                 │

Internet Gateway                  NAT Gateway

      │                                 │

  Public Routing                 Private Routing
```

---

## Learning Objectives

By completing Module 1, the project will demonstrate:

* Infrastructure as Code (IaC)
* Terraform Modules
* Terraform State Management
* Remote Backends
* AWS Networking Fundamentals
* IAM Best Practices
* Modular Infrastructure Design
* Environment Separation
* Production-ready Repository Structure

---

# Current Progress

### Completed

* Project planning
* Architecture design
* Technology selection
* Repository structure

### In Progress

* Module 1

  * Terraform project initialization
  * Backend bootstrap
  * VPC module
  * Networking module
  * IAM module
  * Security group module

### Upcoming

* Amazon EKS
* GitHub Actions
* ArgoCD
* Monitoring Stack
* Developer Portal

---

# Future Features

* One-click application deployment
* Multi-environment support (Development, Staging, Production)
* Self-service infrastructure provisioning
* GitOps-based deployments
* Centralized monitoring and logging
* Slack deployment notifications
* Cost dashboard
* Policy as Code (OPA)
* Role-Based Access Control (RBAC)
* AI Infrastructure Assistant
* Automatic rollback
* Self-healing deployments

---

# Project Status

**Current Phase:** Module 1 – Infrastructure Provisioning

This repository is actively being developed as a production-style Platform Engineering project to demonstrate modern DevOps, Cloud Engineering, and Infrastructure Automation practices.

---

# License

This project is intended for educational and portfolio purposes.
