## K3s Ingress (Traefik) Checklist
**configuration should always be done from the top**
> Replace placeholder values with environment-specific configuration. <br>
> Mark each step as completed [x] during the installation process.
---

## Ingress (Traefik) Configuration

- [ ] Check that Traefik is running

```bash
sudo kubectl get pods -n kube-system | grep traefik
```
- [ ] Check if Traefik is exposed through service

```bash 
sudo kubectl get svc -n kube-system | grep traefik
```
---
- [ ] Createe <INGRESS_FILE>.yaml
- [ ] Configure values in the <INGRESS_FILE>.yaml
- [ ] Host added to ingress:
```yaml
host: <APPLICATION_HOST>
host: <LOCAL_TEST_HOST> # optional second domain if needed
```
- [ ] Copy <INGRESS_FILE>.yaml to control-plane node

```bash
scp <INGRESS_FILE>.yaml <CONTROL_PLANE_HOST>:~
```
- [ ] Applied ingress configuration

```bash
kubectl apply -f <INGRESS_FILE>.yaml
```

## Verification

- [ ] ingress resources and details inspected

```bash
kubectl get ingress # verification
kubectl describe ingress <INGRESS_NAME> # more details
```

## Connectivity

- [ ] test routing through the terminal

```bash
curl -H "Host: <APPLICATION_HOST>" http://<NODE_IP>/ # run from control-plane-1
```

- [ ] SSH tunnel for external host testing
```bash
ssh -L <LOCAL_PORT>:<NODE_IP>:80 <SSH_HOST> # remember to leave tunnel open
```

- [ ] test connectivity through tunnel
```bash
curl -H "Host: <APPLICATION_HOST>" http://localhost:<LOCAL_PORT>
```

- [ ] Browser testing
```html
http://localhost:<LOCAL_PORT>
```