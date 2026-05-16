# Graduation Project 2026 - Local Production-Like K3s Environment

This repository contains my thesis project for Cloud & ICT Engineer. The project focuses on designing, implementing and documenting a smaller production-like Kubernetes environment using open source tools on limited local hardware.

The environment is built locally with Ubuntu virtual machines and K3s. It includes a containerized FastAPI application, Kubernetes deployment and service manifests, Traefik ingress, monitoring with Prometheus and Grafana, and a minimal RBAC implementation.

The goal of the project is not to build a full enterprise production environment, but to make the underlying Kubernetes infrastructure visible and understandable by building the main components manually instead of relying on managed cloud services.

---

## Project Goals

The project is based on the following goals:

- Build a smaller production-like Kubernetes environment locally.
- Use one control-plane node and two worker nodes.
- Deploy and expose at least one containerized application.
- Use an ingress controller for external access.
- Implement monitoring and observability with open source tools.
- Demonstrate Kubernetes RBAC and least privilege concepts.
- Document the environment in a reproducible way.

---

## Environment Overview

The final environment consists of:

- Ubuntu-based virtual machines
- K3s Kubernetes cluster
- 1 control-plane node
- 2 worker nodes
- FastAPI application deployed with 3 replicas
- Kubernetes Service for stable internal access
- Traefik Ingress for routing external traffic
- Prometheus and Grafana for monitoring and observability
- Kubernetes RBAC with ServiceAccounts, Role and RoleBinding
- SSH tunneling for access from an external workstation

Simplified architecture:

```text
Windows Workstation
        |
        | SSH / SSH tunnel
        v
Linux Laptop
        |
        | KVM / libvirt
        v
K3s Cluster
  ├── control-plane-1
  ├── worker-node-1
  └── worker-node-2
        |
        v
Traefik Ingress -> Kubernetes Service -> FastAPI Pods
        |
        v
Prometheus + Grafana Monitoring
```

---

## Technologies Used

- Ubuntu / Ubuntu Server LTS
- KVM / libvirt / virsh
- K3s
- Kubernetes
- kubectl
- Podman
- FastAPI
- Traefik
- Helm
- Prometheus
- Grafana
- Git / GitHub

---

## Repository Structure

```text
.
├── app/
│   ├── Dockerfile
│   └── main.py
│
├── deployment/
│   ├── fastapi.yaml
│   ├── fastapi-template.yaml
│   ├── fastapi-serviceaccount.yaml
│   ├── fastapi-serviceaccount-template.yaml
│   ├── ingress.yaml
│   ├── ingress-template.yaml
│   ├── grafana-monitoring-ingress.yaml
│   ├── grafana-monitoring-ingress-template.yaml
│   ├── rbac-readonly.yaml
│   └── rbac-readonly-template.yaml
│
├── docs/
│   ├── environment-requirements.md
│   ├── screenshots.md
│   ├── k3s/
│   ├── notes/
│   ├── specs/
│   ├── screenshots/
│   └── archive/
│
├── LICENSE
└── README.md
```

---

## Application

The application is a small FastAPI service built from scratch for the project. It includes three endpoints:

```text
/        - browser-friendly root page
/health  - health endpoint used by Kubernetes probes
/info    - application and pod information
```

The application is containerized with Podman and deployed to the K3s cluster with Kubernetes manifests.

The deployment includes:

- 3 replicas
- liveness probe
- readiness probe
- environment variable
- dedicated ServiceAccount
- disabled automatic ServiceAccount token mounting

---

## Container Image Workflow

This project does not use an external container registry. The image workflow is intentionally manual to make the container distribution process visible.

The workflow is:

```text
Application code -> Podman build -> image tar export -> copy to nodes -> import into K3s container runtime -> Kubernetes deployment
```

This made it easier to understand how Kubernetes depends on the container image being available on the node where a pod is scheduled.

One troubleshooting example from this workflow was `ErrImageNeverPull`, which occurred when the image was not available locally on the node or did not match the image name in the deployment manifest.

---

## Kubernetes Deployment

The FastAPI application is deployed using Kubernetes manifests in the `deployment/` directory.

Main files:

- `fastapi.yaml`
- `ingress.yaml`
- `fastapi-serviceaccount.yaml`
- `rbac-readonly.yaml`

Template versions are also included for reproducibility.

---

## Ingress and External Access

Traefik is used as the ingress controller. It is included by default in K3s, which made it a natural choice for this project.

The FastAPI application is exposed through Traefik Ingress using host-based routing.

Grafana is also exposed through a separate ingress manifest:

- `grafana-monitoring-ingress.yaml`

SSH tunneling was used when working from a Windows workstation outside the internal VM network.

---

## Monitoring and Observability

Monitoring is implemented with the `kube-prometheus-stack` Helm chart in a dedicated `monitoring` namespace.

The stack includes:

- Prometheus
- Grafana
- Alertmanager
- node-exporter
- kube-state-metrics

Grafana dashboards were used to verify metrics for:

- cluster resources
- nodes
- namespaces
- pods
- CPU usage
- memory usage

---

## RBAC and Access Control

RBAC is implemented in a limited but relevant way to demonstrate Kubernetes access control and least privilege concepts.

The project includes:

- a dedicated ServiceAccount for the FastAPI workload
- disabled automatic ServiceAccount token mounting for the application pod
- a separate read-only ServiceAccount
- a Role with read permissions for pods and services
- a RoleBinding connecting the Role to the ServiceAccount

The read-only ServiceAccount was verified with `kubectl auth can-i`.

It was allowed to read pods and services in the default namespace, but denied access to actions such as deleting pods, creating deployments, reading secrets and accessing the monitoring namespace.

---

## Documentation

The `docs/` directory contains project documentation, notes, screenshots and checklists.

Important documentation:

- `docs/environment-requirements.md`
- `docs/screenshots.md`
- `docs/specs/requirements-en.md`
- `docs/specs/requirements-sv.md`
- `docs/k3s/`

The `docs/k3s/` directory includes both hardcoded checklists used in this specific environment and template-based versions for reproducibility.

For non-hardcoded doucumentations refer to the checklists with `template`
---

## Screenshots

Final screenshots are documented in:

```text
docs/screenshots.md
```

The screenshots show the final state of the environment, including:

- cluster nodes
- workloads across namespaces
- FastAPI pods and ServiceAccount
- Kubernetes Service
- Traefik Ingress
- Grafana access
- Prometheus data source
- Grafana dashboards
- RBAC verification

---

## Scope and Limitations

This project is intentionally limited in scope.

Included:

- local Kubernetes environment
- K3s multi-node cluster
- application deployment
- ingress routing
- monitoring and observability
- basic RBAC
- documentation and reproducibility

Not included:

- managed cloud provider integration
- enterprise high availability
- multi-region architecture
- external container registry
- CI/CD pipeline
- infrastructure as code
- automated backups
- external storage solution

These limitations were chosen to keep the project realistic within the timeframe while still demonstrating important production-like Kubernetes concepts.

---

## Future Improvements

Possible future improvements include:

- adding a container registry
- implementing CI/CD
- adding Infrastructure as Code with OpenTofu
- adding automated backups
- improving RBAC with more detailed roles and policies
- adding persistent storage
- separating workloads more clearly between control-plane and worker nodes
- improving monitoring alerts

---

## Status

The technical implementation is complete.

The project includes:

- working K3s cluster
- running FastAPI application
- ingress exposure
- monitoring stack
- RBAC demonstration
- screenshots
- checklists
- template files
- project documentation

---
