## K3s Pre-Installation Checklist

### Infrastructure
- [x] 3 virtual machines created
- [x] Node roles defined:
  - control-plane-1
  - worker-node-1
  - worker-node-2
- [x] Ubuntu Server LTS installed on all nodes

---

### Networking
- [x] All nodes are on the same network (192.168.122.x)
- [x] Each node has a reachable IP address
- [x] Verified connectivity between nodes (SSH works)
- [x] Control plane IP identified
- [x] Worker node IPs identified

---

### SSH Access
- [x] SSH access from laptop → all nodes
- [x] SSH aliases configured in ~/.ssh/config
- [x] Able to connect using:
  - ssh control-plane-1
  - ssh worker-node-1
  - ssh worker-node-2

---

### System Preparation
- [x] Disabled swapoff on all nodes
```bash
sudo swapoff -a
```

- [x] System packages updated on all nodes
```bash
sudo apt update && sudo apt upgrade -y
```
---

### System Validation
- [x] Checked that the system clock is in sync
- [x] Checked that the NTP service is active
- [x] Checked that curl exists
- [x] Checked all the previous steps

---

**Now go on and install k3s!**