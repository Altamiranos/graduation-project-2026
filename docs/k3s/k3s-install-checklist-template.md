## K3s Install
**installation should always be done from the control plane node first**
> Replace placeholder values with environment-specific configuration. <br>
> Mark each step as completed [x] during the installation process.
---

## Control Plane
- [ ] SSH into control plane 1
```bash
ssh <CONTROL_PLANE_HOST>
```
- [ ] Install control plane on <CONTROL_PLANE_HOST>
```bash
curl -sfL https://get.k3s.io | sh -
```
- [ ] Verify if the control plane is ready
```bash
sudo kubectl get nodes
```
- [ ] Retrieve node token from control plane
```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```
- [ ] Verify the IP for <CONTROL_PLANE_HOST> (e.g. 192.168.x.x)
```bash
hostname -I
```
---
## Worker Nodes
- [ ] SSH into worker node 1
```bash
ssh <WORKER_NODE_1>
```
- [ ] Join worker node 1 to the control-plane via Token and IP (Remember to replace <CONTROL_PLANE_IP> and <TOKEN> with environment-specific values)
```bash
curl -sfL https://get.k3s.io | K3S_URL=https://<CONTROL_PLANE_IP>:6443 K3S_TOKEN=<TOKEN> sh -
```
- [ ] Check if the worker node 1 is ready (needs to be done from the <CONTROL_PLANE_HOST>)
```bash
sudo kubectl get nodes
```
- [ ] SSH into worker node 2
```bash
ssh <WORKER_NODE_2>
```
- [ ] join worker node 2 to the control plane via Token and IP (Remember to replace <CONTROL_PLANE_IP> and <TOKEN> with environment-specific values)
```bash
curl -sfL https://get.k3s.io | K3S_URL=https://<CONTROL_PLANE_IP>:6443 K3S_TOKEN=<TOKEN> sh -
```
- [ ] Check if the worker node 2 is ready (needs to be done from the <CONTROL_PLANE_HOST>)
```bash
sudo kubectl get nodes
```

