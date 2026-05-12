# Screenshots

This document contains screenshots from the implementation and verification process of the project.

## 1. Cluster nodes ready

![Cluster nodes ready](screenshots/01-cluster-nodes-ready.png)

Shows that the K3s cluster consists of one control-plane node and two worker nodes, all in Ready state.

## 2. Workloads across all namespaces

![Workloads across all namespaces](screenshots/02-cluster-workloads-all-namespaces.png)

Shows workloads running across the cluster, including the default, kube-system and monitoring namespaces.

## 3. FastAPI pods and ServiceAccount

![FastAPI pods and ServiceAccount](screenshots/03-fastapi-pods-serviceaccount.png)

Shows the FastAPI pods running and using the dedicated ServiceAccount for the application workload.

## 4. FastAPI service through NodePort

![FastAPI service](screenshots/04-fastapi-service-nodeport.png)

Shows the FastAPI Kubernetes Service and the NodePort used during verification.

## 5. FastAPI browser access through ingress

![FastAPI browser ingress success](screenshots/05-fastapi-browser-ingress-success.png)

Shows the FastAPI application reachable from the browser after ingress and SSH tunneling were configured.

## 6. Traefik ingress resources

![Ingress resources Traefik](screenshots/06-ingress-resources-traefik.png)

Shows the FastAPI and Grafana ingress resources exposed through Traefik.

## 7. Grafana exposed through ingress

![Grafana ingress login](screenshots/07-grafana-ingress-login.png)

Shows Grafana reachable through the browser using the grafana.local hostname and SSH tunnel.

## 8. Prometheus data source in Grafana

![Grafana Prometheus data source](screenshots/08-grafana-prometheus-datasource-success.png)

Shows that Grafana is configured with Prometheus as a provisioned data source.

## 9. Grafana dashboards list

![Grafana dashboards list](screenshots/09-grafana-dashboards-list.png)

Shows the available Grafana dashboards installed through the monitoring stack.

## 10. Grafana node dashboard

![Grafana node dashboard](screenshots/10-grafana-node-dashboard.png)

Shows node-level metrics such as CPU and memory usage.

## 11. Grafana FastAPI pod dashboard

![Grafana FastAPI pod dashboard](screenshots/11-grafana-fastapi-pod-dashboard.png)

Shows metrics for the FastAPI pods running in the default namespace.

## 12. RBAC verification

![RBAC verification](screenshots/12-rbac-verification.png)

Shows that the read-only ServiceAccount is allowed to read pods, but denied write access, secret access and access to the monitoring namespace.
