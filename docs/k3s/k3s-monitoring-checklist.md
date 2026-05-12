## Disclaimer

This checklist is based on environment-specific configurations (hardcoded values such as IP addresses and hostnames).

it is intended for personal documentation and learning purposes only, and may not be directly applicable to other environments without modification.

For a generalized and reproducible setup, refer to the corresponding template-based documentation.

# installation

- [x] Check helm version
- [x] If helm is not present, install it and check version again
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```
- [x] Added Repo with Prometheus helm
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

- [x] Create monitoring space
```bash
kubectl create namespace monitoring 
```

- [x] Install the stack in the created monitoring space
```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring
  ```
- [x] Verify the namespace, pods, services
```bash
kubectl get ns
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

- [x] Get grafana admin password
```bash
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d
```
## Port-forwarding and testing Grafana locally. (Optional but recommended)
Since the recurring work method of this project is done in two steps, the monitoring stack was first tested locally through port-forwarding and later exposed through Ingress.

- [x] Access grafana through port-forwarding
```bash
# Leave this running for browser access: http://localhost:3000 
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80 
```

- Access browser: http://localhost:3000
- Expected output: Grafana login page is reachable through localhost:3000

Login with username and password:
Username: Admin
Password: <Retrieved Kubernetes secret>

- Verify that the dashboards are visualizing metrics

Kubernetes / Compute Resources / Cluster
Kubernetes / Compute Resources / Node
Kubernetes / Compute Resources / Namespace
Kubernetes / Compute Resources / Pod

## Monitoring exposed through ingress (Traefik)

- [x] Create Grafana Ingress manifest
```yaml
# Created manifest YAML
deployment/grafana-monitoring-ingress.yaml
```
- Copy, apply and verify
```bash

# Copy from linux-laptop to the cluster control-plane
scp deployment/grafana-monitoring-ingress.yaml altamiranos@control-plane-1:~

# Apply Grafana Ingress manifest from the control-plane
kubectl apply -f grafana-monitoring-ingress.yaml

# Verify Grafana Ingress
kubectl get ingress -n monitoring
```
- [x] Verify connection
```bash
# Terminal access
curl -v --max-time 10 -H "Host: grafana.local" http://192.168.122.221
```
access through browser: http://grafana.local

---

## SSH Tunneling from external workstation (Optional)

This step is optional and specific to this project environment.

In this project, `grafana.local` was mapped to `127.0.0.1` on the Windows workstation because access was done through an SSH tunnel. If working directly from the Linux laptop, SSH tunneling is not required as long as the laptop can reach the KVM/libvirt network.

- [x] Add `grafana.local` to hosts file

- Windows hosts file: C:\Windows\System32\drivers\etc\hosts
- Entry: 127.0.0.1 grafana local
---

- [x] Create SSH tunnel from Windows workstation

```powershell
# Leave the SSH running when accessing Grafana from browser
ssh -L 127.0.0.1:30080:192.168.122.221:80 linux-laptop

---

# Access Grafana through browser from workstation
browser: http://grafana.local:30080

---

# Verify Grafana access with curl from workstation
curl.exe -v --max-time 10 -H "Host: grafana.local" http://127.0.0.1:30080
```
