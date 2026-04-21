## K3s Pre-Installation Checklist

> Replace placeholder values with environment-specific configuration.

### Infrastructure
- [ ] 3 virtual machines created
- [ ] Node roles defined:
  - control-plane node
  - worker nodes
- [ ] Ubuntu Server LTS installed on all nodes

---

### Networking
- [ ] All nodes are on the same internal network (e.g. 192.168.x.x)
- [ ] Each node has a reachable IP address
- [ ] Verified connectivity between nodes (SSH works)
- [ ] Control plane IP identified: <CONTROL_PLANE_IP>
- [ ] Worker node IPs identified: <WORKER_NODE_IP_1>, <WORKER_NODE_IP_2>

---

### SSH Access
- [ ] SSH access from host → all nodes
- [ ] SSH aliases configured in ~/.ssh/config
- [ ] Able to connect using:
  - ssh <CONTROL_PLANE_HOST>
  - ssh <WORKER_NODE_1>
  - ssh <WORKER_NODE_2>

---

### System Preparation
- [ ] System packages updated on all nodes
```bash
sudo apt update && sudo apt upgrade -y