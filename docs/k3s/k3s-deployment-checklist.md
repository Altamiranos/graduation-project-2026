## Disclaimer

This checklist is based on environment-specific configurations (hardcoded values such as IP addresses and hostnames).

it is intended for personal documentation and learning purposes only, and may not be directly applicable to other environments without modification.

For a generalized and reproducible setup, refer to the corresponding template-based documentation.
---

## Application
- [x] FastAPI application created
- [x] Application includes `/`, `/health`, and `/info` endpoints
- [x] Application tested locally before containerization
---

### Container Image
- [x] Container image built with Podman
```bash
podman build -t fastapi-k3s:1.0 .
```
- [x] image exported as tar file
```bash
podman save -o fastapi-k3s.tar localhost/fastapi-k3s:1.0
```
- [x] image copied to cluster-nodes
```bash
scp fastapi-k3s.tar control-plane-1:~ # fastapi-k3s.tar -> control-plane-1
scp fastapi-k3s.tar worker-node-1:~ # fastapi-k3s.tar -> worker-node-1
scp fastapi-k3s.tar worker-node-2:~ # fastapi-k3s.tar -> worker-node-2
```
- [x] image imported on all nodes (run this on all the nodes) 
```bash
sudo k3s ctr images import fastapi-k3s.tar
```
- [x] verify the image imported
```bash
sudo k3s ctr images ls | grep fastapi # expected output: localhost/fastapi-k3s:1.0
```

## Deployment

- [x] .yaml created with deployment and service
```bash
fastapi.yaml # deployment.yaml & service.yaml
```
- [x] .yaml file applied
```bash
sudo kubectl apply -f fastapi.yaml # apply the .yaml
```
- [x] deployment rollout restarted
```bash
sudo kubectl rollout restart deployment fastapi-app # restart the deployment if image needs adjustment
```
## Verification
- [x] Check if pods are running
```bash
sudo kubectl get pods # the pods should have status: running
```
- [x] Check if pods are scheduled correctly
```bash
sudo kubectl get pods -o wide # the pods should show readiness: 1/1
``` 
- [x] Check if application is reachable trough service and endpoints
```bash
curl http://192.168.122.113:32300 # worker-node-1 
curl http://192.168.122.113:32300/health # check health endpoint
curl http://192.168.122.113:32300/info # check info endpoint
```
- [x] Load balancing verified by repeated requests
---
## External Access (SSH Tunnel)
- [x] Created SSH tunnel for reaching host machine outside of internal VM-network
```bash
ssh -L 8080:192.168.122.113:32300 linux-laptop # remember to leave tunnel open in powershell (windows host)
```
- [x] Check if application is reachable in windows browser
```html
http://localhost:8080
```
## Troubleshooting
This is based on the **ErrImageNeverPull** event.
- [x] Check if the image matches in the .yaml and the image list on all nodes
```bash
kubectl set image deployment/fastapi-app fastapi=localhost/fastapi-k3s:1.0 # update the image to the correct one
sudo kubectl rollout restart deployment fastapi-app # restart the deployment if image is updated
sudo ctr images list | grep fastapi # check if the correct image is applied on every node
```
This should resolve the **ErrImageNeverPull** to **Running** status

## Validation
- [x] FastApi application deployed
- [x] Service exposes application
- [x] Application reachable (curl & browser)
- [x] Load balancing verified (repeated requests)
