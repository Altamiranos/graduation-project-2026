# Requirements Specification – Thesis Project

- **Name:** Sander Altamirano
- **Class:** Cloud24
- **Date:** 1/3 2026

---

## Background

Since many organizations use Kubernetes to run production environments and container-based applications, it is important to understand how these environments are designed and configured. Knowledge of cluster architecture, networking, security, and monitoring is a key part of working in Cloud and infrastructure. Major cloud providers offer managed Kubernetes services where much of the infrastructure is abstracted, making the underlying architecture often "invisible" to both developers and users. To gain a deeper understanding of how a production-like environment is built, such an environment needs to be designed and implemented from scratch. The project therefore focuses on creating a smaller, open source-based Kubernetes environment in a local lab environment, independent of hyperscalers and their ecosystems.

The project is based on the need to understand the infrastructure behind modern platforms without relying on abstracted cloud services.

---

## Goals and Scope

The purpose of the thesis is to design and implement a smaller, reproducible and production-like Kubernetes environment based on Ubuntu. The environment consists of one control plane node and two worker nodes. At least one application shall be deployed and exposed via an ingress controller. Monitoring is implemented using open source tools to get an overview of the cluster's health and functions. Secure access is managed through Kubernetes built-in RBAC. The project is scoped to a local environment and does not include integration with hyperscalers such as AWS, Azure or GCP. High availability at an enterprise level, CI/CD automation or multi-region architecture are not part of the project. The scope ensures a realistic timeframe while still meeting the project's goals and resource constraints.

---

## Three questions to be answered by the end of the project

1. How can a smaller production-like Kubernetes environment be designed and implemented using open source tools in a local infrastructure?
2. How can an application be deployed and exposed via an ingress controller in the cluster?
3. How can monitoring and observability be implemented with open source tools to ensure visibility into the cluster's health and function?

---

## Technologies

The project is carried out in a local Ubuntu-based environment and builds on a smaller Kubernetes setup consisting of one control plane node and two worker nodes. The environment is implemented with K3s, a lightweight distribution of Kubernetes built for resource-constrained systems. This choice is motivated by the project's local infrastructure and the need for a manageable and reproducible solution. K3s also supports multi-node setups.

Containerization is done with Docker and at least one test application is deployed in the cluster to demonstrate functionality, communication between nodes and how applications run. Services are exposed via the ingress controller Traefik, which is compatible with K3s and enables routing and external access to the application. Traefik is well established in container-based environments. For monitoring and observability, Prometheus is used for metrics collection while Grafana is used for visualization and analysis of the cluster's health and function. These tools are well established in the industry and relevant for Cloud and infrastructure roles.

Access control is implemented through Kubernetes built-in RBAC to manage access and permissions in the cluster. The environment is documented through an overview, installation steps and reasoning behind configuration choices, with the goal of creating a reproducible and structured solution.

---

## Added Afterwards – Terraform, GitHub Repository

Since the project is about creating a smaller production-like Kubernetes-based environment with open source tools, I had originally planned to use Terraform for automation. However, Terraform moved to a business license and is therefore no longer open source as of 2023, which is why OpenTofu will be used for IaC. Since Terraform is still the industry standard, OpenTofu is relevant given its 95–100% compatibility.

A GitHub repository will be created alongside the project to build a portfolio and further reinforce the idea of creating a reproducible environment.

---

## Added Afterwards 2.0

Since my desktop PC at home runs Windows, I want to set it up so I can SSH or work from that machine for convenience. The project itself will remain the same and will be carried out on my Linux laptop where I use KVM for the project.

The only difference is that the work is done from my stationary PC at home.
