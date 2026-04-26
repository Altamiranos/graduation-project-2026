## K3s Deployment checklist
**Deployment should always be done from the top**
> Replace placeholder values with environment-specific configuration. <br>
> Mark each step as completed [x] during the installation process.
---

## Application
- [ ] FastAPI application created
- [ ] Application includes `/`, `/health`, and `/info` endpoints
- [ ] Application tested locally before containerization
---

### Container Image
- [ ] Container image built with Podman
```bash
podman build -t <IMAGE_NAME>:<IMAGE_TAG>
```
- [ ] image exported as tar file
```bash
podman save -o <IMAGE_TAR_FILE> <LOCAL_IMAGE_NAME>:<IMAGE_TAG>
```
- [ ] image copied to all cluster-nodes
```bash
scp <IMAGE_TAR_FILE> <CONTROL_PLANE_HOST>:~ 
scp <IMAGE_TAR_FILE> <WORKER_NODE_1>:~
scp <IMAGE_TAR_FILE> <WORKER_NODE_2>:~
```
- [ ] image imported on all nodes (run this on all the nodes) 
```bash
sudo k3s ctr images import <IMAGE_TAR_FILE>
```
- [ ] verify the imported image name
```bash
sudo k3s ctr images ls | grep <IMAGE_NAME> # expected output example: <IMAGE_REGISTRY>/<IMAGE_NAME>:<IMAGE_TAG>
```
## Deployment

- [ ] Kubernetes .yaml created (Deployment + Service)
```yaml
<DEPLOYMENT_FILE>.yaml # deployment.yaml & service.yaml
```

- [ ] Deployment references adjusted correctly
```yaml
image: <IMPORTED_IMAGE_NAME>:<IMAGE_TAG> # The imported <IMAGE_TAR_FILE>
imagePullPolicy: Never
```

- [ ] .yaml file applied
```bash
sudo kubectl apply -f <DEPLOYMENT_FILE>.yaml
```

- [ ] deployment rollout restarted (if needed)
```bash
sudo kubectl rollout restart deployment <DEPLOYMENT_NAME>
```

## Verification

- [ ] Check if pods are running
```bash
sudo kubectl get pods # the pods should have status: running
```

- [ ] Check if pods are scheduled correctly
```bash
sudo kubectl get pods -o wide # the pods should show readiness: 1/1
```

- [ ] Check if application is reachable trough service and endpoints
```bash
curl http://<NODE_IP>:<NODE_PORT>
curl http://<NODE_IP>:<NODE_PORT>/health # health endpoint
curl http://<NODE_IP>:<NODE_PORT>/info # info endpoint
```

- [ ] Load balancing verified (repeated requests)
```bash
curl http://<NODE_IP>:<NODE_PORT>
```
---

## External Access (SSH Tunnel) (OPTIONAL)
This step is completely optional, this only applies if access is being done outside of the internal VM-network. For example working from a Desktop PC -> Laptop (Project)

- [ ] SSH tunnel created (if required)
```bash
ssh -L <LOCAL_PORT>:<NODE_IP>:<NODE_PORT> <SSH_HOST> # Remember to leave the tunnel open.
```

- [ ] Check if application is reachable in windows browser
```html
http://localhost:<LOCAL_PORT>
```
DISCLAIMER: Check that tunnel is open if not on the internal VM-network, if working within the internal VM-network: Ignore.
## Troubleshooting

This is based on the **ErrImageNeverPull** event. Possible causes:

- Image not available locally on node
- Image name mismatch between Deployment and container runtime
- imagePullPolicy set to Never
---
- [ ] Verify image exists on node
```bash
sudo k3s ctr images ls | grep <IMAGE_NAME>
```
- [ ] Update deployment image
```bash
kubectl set image deployment/<DEPLOYMENT_NAME> <CONTAINER_NAME>=<IMPORTED_IMAGE_NAME>:<IMAGE_TAG>
```
- [ ] Restart deployment
```bash
sudo kubectl rollout restart deployment <DEPLOYMENT_NAME>
```

This should resolve the **ErrImageNeverPull** to **Running** status

## Validation

- [ ] FastApi application deployed
- [ ] Service exposes application
- [ ] Application reachable (curl & browser)
- [ ] Load balancing verified (repeated requests)
