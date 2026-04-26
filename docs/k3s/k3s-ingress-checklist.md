## Disclaimer

This checklist is based on environment-specific configurations (hardcoded values such as IP addresses and hostnames).

it is intended for personal documentation and learning purposes only, and may not be directly applicable to other environments without modification.

For a generalized and reproducible setup, refer to the corresponding template-based documentation.
---
## Ingress (Traefik) configuration

- [x] Check that Traefik is running
```bash
sudo kubectl get pods -n kube-system | grep traefik
```
- [x] Check if Traefik is exposed trough service
```bash 
sudo kubectl get svc -n kube-system | grep traefik
```
---
- [x] Created **ingress.yaml**
- [x] Configured the values in the **ingress.yaml**
- [x] Host added to ingress:
```yaml
host: fastapi.local
host: localhost # second domain added for browser access
```
- [x] Copied the .yaml to control-plane-1
```bash
scp ingress.yaml control-plane-1:~
```
- [x] Applied ingress in control-plane-1
```bash
sudo kubectl apply -f ingress.yaml
```

## verification
- [x] ingress resources and details inspected
```bash
sudo kubectl get ingress # verification
sudo kubectl describe ingress fastapi-ingress # more details
```
## Connectivity
- [x] test routing trough the terminal
```bash
curl -H "Host: fastapi.local" http://192.168.122.113/ # run from control-plane-1
```
- [x] SSH tunnel for external host testing
```powershell
ssh -L 18080:192.168.122.113:80 linux-laptop # remember to leave tunnel open
```
- [x] test connectivity trough tunnel
```powershell
curl -H "Host: fastapi.local" http://localhost:18080
```
- [x] Browser testing
```html
http://localhost:18080
```