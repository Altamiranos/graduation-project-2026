## K3s Monitoring - Prometheus/Grafana
**Configuration should always be done from the control plane node first**
> Replace placeholder values with environment-specific configuration. <br>
> Mark each step as completed [x] during the installation process.

---

## Helm

- [ ] Check Helm version

```bash
helm version
```
- [ ] If helm is not present, install it and check version again
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

- [ ] Add Prometheus Community Helm repository
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
- [ ] Create monitoring namespace
```bash
kubectl create namespace <MONITORING_NAMESPACE>

# verify the created namespace
kubectl get ns
```
- [ ] Install `kube-prometheus-stack` in the monitoring namespace
```bash
helm install <HELM_RELEASE_NAME> prometheus-community/kube-prometheus-stack \
  --namespace <MONITORING_NAMESPACE>

# Verify the pods and services
kubectl get pods -n <MONITORING_NAMESPACE>
kubectl get pods -n <MONITORING_NAMESPACE> -o wide
kubectl get svc -n <MONITORING_NAMESPACE>
```
- Expected results: Prometheus, Grafana, Alertmanager, node-exporter and kube-state-metrics pods should be running.

- [ ] Retrieve Grafana admin password
```bash
kubectl get secret -n <MONITORING_NAMESPACE> <GRAFANA_SECRET_NAME> \
  -o jsonpath="{.data.admin-password}" | base64 -d
```
Expected login:
- Username: admin
- Password: <RETRIEVED_GRAFANA_SECRET>
---

## Local Verification with Port-forwarding

This step is optional but recommended before exposing Grafana through ingress.

- [ ] Access Grafana through port-forwarding
```bash
kubectl port-forward -n <MONITORING_NAMESPACE> svc/<GRAFANA_SERVICE_NAME> <LOCAL_PORT>:80
```
- [ ] Access Grafana in browser: `http://localhost:<LOCAL_PORT>`
- Expected result: Grafana login page is reachable through localhost
---
- [ ] Verify Prometheus data source in Grafana
Grafana path: connections -> data sources -> Prometheus

- [ ] Verify Kubernetes dashboards in Grafana

- Kubernetes / Compute Resources / Cluster
- Kubernetes / Compute Resources / Node
- Kubernetes / Compute Resources / Namespace
- Kubernetes / Compute Resources / Pod

- Expected results: Grafana dashboards should show Kubernetes metrics for cluster, nodes, namespaces and pods.
---

### Monitoring exposed through ingress
- [ ] Create Grafana ingress manifest, another template can be found in the deployment section of the repository.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <GRAFANA_INGRESS_NAME>
  namespace: <MONITORING_NAMESPACE>
spec:
  ingressClassName: traefik
  rules:
    - host: <GRAFANA_HOSTNAME>
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: <GRAFANA_SERVICE_NAME>
                port:
                  number: 80
```
---
- [ ] Apply Grafana ingress manifest
```bash
kubectl apply -f <GRAFANA_INGRESS_FILE>.yaml
```
- [ ] Verify Grafana ingress
```bash
kubectl get ingress -n <MONITORING_NAMESPACE>
```
- Expected result: Grafana Ingress should be created and point to <GRAFANA_HOSTNAME>.

### Direct ingress access
Use this if the machine can reach the Kubernetes node network directly 

- [ ] Add <GRAFANA_HOSTNAME> to hosts file

- Linux/macOS: /etc/hosts
- Windows: C:\Windows\System32\drivers\etc\hosts

- Type the IP off the node and hostname set: <NODE_IP> <GRAFANA_HOSTNAME>

- [ ] Verify Grafana through ingress with curl (Terminal)
```bash
curl -v --max-time 10 -H "Host: <GRAFANA_HOSTNAME>" http://<NODE_IP>

```

## Troubleshooting 

- Helm cannot reach the Kubernetes cluster
- Kubeconfig is not correctly set
- Monitoring pods are pending or evicted
- Node has resource pressure
- Grafana service name is incorrect
- Hostname does not resolve correctly
- SSH tunnel is not running
- Ingress manifest points to the wrong namespace or service

Verification list:
```bash
# Verify the correct kubeconfig
echo $KUBECONFIG
kubectl get nodes

# Verify pods
kubectl get pods -n <MONITORING_NAMESPACE>
kubectl describe pod <POD_NAME> -n <MONITORING_NAMESPACE>

# Verify nodes
kubectl describe node <NODE_NAME> | grep -A10 -E "DiskPressure|MemoryPressure|Conditions"

# Verify Grafana service
kubectl get svc -n <MONITORING_NAMESPACE>

# Verify ingress config
kubectl get ingress -n <MONITORING_NAMESPACE>
kubectl describe ingress <GRAFANA_INGRESS_NAME> -n <MONITORING_NAMESPACE>
```
## Validation list 

Monitoring namespace created
- [ ] kube-prometheus-stack installed
- [ ] Prometheus running
- [ ] Grafana running
- [ ] Grafana credentials retrieved
- [ ] Grafana verified locally through port-forwarding
- [ ] Prometheus data source verified in Grafana
- [ ] Kubernetes dashboards verified
- [ ] Grafana exposed through Traefik Ingress
- [ ] Grafana reachable through browser
- [ ] Optional SSH tunnel verified, if required