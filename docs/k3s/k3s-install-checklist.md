## K3s Install

**installation should always be done from the control plane node first**
---

## Control Plane
- [ ] SSH into control-plane-1
```bash
ssh control-plane-1
```
- [ ] Install control plane on control-plane-1
```bash
curl -sfL https://get.k3s.io | sh -
```
- [ ] Verify if the control plane is ready
```bash
sudo kubectl get nodes
```
- [ ] Generated token from control plane
```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```
- [ ] Checked the IP for control plane
```bash
hostname -I
```
---
## Worker Nodes
- [ ] SSH into worker-node-1
```bash
ssh worker-node-1
```
- [ ] Worker-node-1 joined the control plane via Token and IP (Remember to replace <TOKEN> with generated one.)
```bash
curl -sfL https://get.k3s.io | K3S_URL=https://192.168.122.221:6443 K3S_TOKEN=<TOKEN> sh -
```
- [ ] Checked if the worker-node-1 is ready (needs to be done from the control-plane-1)
```bash
sudo kubectl get nodes
```
- [ ] Worker-node-2 joined the control plane via Token and IP (Remember to replace <TOKEN> with generated one.)
```bash
curl -sfL https://get.k3s.io | K3S_URL=https://192.168.122.221:6443 K3S_TOKEN=<TOKEN> sh -
```
- [ ] Checked if the worker-node-2 is ready (needs to be done from the control-plane-1)
```bash
sudo kubectl get nodes
```

