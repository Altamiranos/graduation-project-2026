## Disclaimer

These draft notes are based on environment-specific configurations (hardcoded values such as IP addresses and hostnames).

They are intended for personal documentation and learning purposes only, and may not be directly applicable to other environments without modification.

For a generalized and reproducible setup, refer to the corresponding template-based documentation.

# Draft Notes 27/4 2026

Week 2! The core infrastructure is now complete, however some parts of the project is still not done. The next step for this and the first thing to prioritize is the monitoring. 

Since this project is supposed to be "production-like", maybe the work methods should mirror that. The configuration will therefore be done in two steps.

## Step one

Create monitoring locally first to not expose it publicly

- Create a namespace named `monitoring`
- Install Prometheus and Grafana using `kube-prometheus-stack`
- Verify that all pods are running
- Configure and verify that monitoring is functional through `kubectl port-forward`
- Service sends traffic to pod
- Prometheus gathers metrics
- Create dashboard in Grafana for visual monitoring of metrics (CPU, Memory, Pods, Nodes, Ready, NotReady)

## Step two

If step one is successful, continue with exposing Grafana through: Ingress + Traefik (already exists)

- Create a manifest that contains the configuration (IPs, NodePort, HostName)
- Create and Expose configuration through Traefik Ingress
- Point the ingress correctly to the service
- Service sends traffic to pod
- Prometheus gathers metrics
- Create a dashboard in Grafana for visual monitoring of metrics (CPU, Memory, Pods, Nodes, Ready, NotReady)

When trying to run the helm install, the kubeconfig was not correctly set. hence to why it falls back to the `localhost:8080`. This resulted in the following error:
```bash 
Error: INSTALLATION FAILED: Kubernetes cluster unreachable: Get "http://localhost:8080/version": dial tcp 127.0.0.1:8080: connect: connection refused
```
The solution was to create a `~/.kube/config.`

- Ran this to have the correct config for the cluster.
```bash
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
chmod 600 ~/.kube/config
```
- Sat the correct environment
```bash
export KUBECONFIG=$HOME/.kube/config
```
- Checked if the correct environment is set
```bash
echo $KUBECONFIG # expected output: /home/altamiranos/.kube/config
```
If the expected output is still not showing, try to `export` again and then `echo`.
---

When installing the `kube-prometheus-stack`, i had the `pending` and `evicted` when watching the pods in the stack. By describing the pod, the following event was shown
```bash
Events:
  Type     Reason     Age   From               Message
  ----     ------     ----  ----               -------
  Normal   Scheduled  49s   default-scheduler  Successfully assigned monitoring/monitoring-prometheus-node-exporter-nn74s to control-plane-1
  Warning  Evicted    50s   kubelet            The node had condition: [DiskPressure].
```

The resource allocation that had been set initially in the VMs were not enough and reaching its limit. To support the monitoring stack in the project, more resources need to be allocated. Time to scale up! 

However, after letting the cluster continue working, the environment actually self-healed. When the `kube-prometheus-stack` was being installed it seems that it was a temporary overload of resources being consumed. The pods being `evicted` and the scheduler shuffling workloads was therefore a promising outcome. This shows that the cluster is self-healing and Kubernetes is working as expected. 

Since the resources are still being pushed to their limit, the resources will be adjusted to handle the monitoring more stable. Especially the disk capacity.

Plan for tomorrow: Adjust the resources in the cluster. Especially the disk capacity, then verify the grafana locally and when successful - expose the monitoring through Ingress + Traefik. Finish the checklists **k3s-monitoring-checklist.md** and **k3s-monitoring-checklist-template.md** 

# Draft Notes 28/4 2026

The plan for today was to adjust the resources, so the cluster could run more stable since it was pushed to it's limit. The environment self-healead by having pods evicted and workloads shuffled during the `kube-prometheus-stack` installation. The control plane reported `DiskPressure`.

Since the original resource allocation in the VMs was enough for running the environment and the FastAPI deployment, but the environment reached its limit with the monitoring stack that was installed. Stack includes:

- Prometheus
- Grafana
- Dashboards
- Alertmanager
- node-exporter
- logs

Therefore resources allocation in the VMs were increased. This was a surprise but also crucial before moving on with the monitoring. 

### Resource allocation adjustments

- [x] Turn off the VMs.

```bash
virsh shutdown control-plane-1
virsh shutdown worker-node-1
virsh shutdown worker-node-2
virsh list --all # verify that all VMs are shutoff
```
- [x] Checked VM info

```bash
# Max memory: 1536000 KiB (1.5 GB)
# Used memory: 1536000 KiB (1.5 GB)
virsh dominfo control-plane-1
virsh dominfo worker-node-1
virsh dominfo worker-node-2 
```
- [x] Adjusted the Memory (RAM)

```bash
# control-plane-1
# Max memory: 3145728 KiB (3 GB)
# Used memory: 3145728 KiB (3 GB)
virsh setmaxmem control-plane-1 3072M --config
virsh setmem control-plane-1 3072M --config 

# worker-node-1
# Max memory: 2097152 KiB (2 GB)
# Used memory: 2097152 KiB (2 GB)
virsh setmaxmem worker-node-1 2048M --config
virsh setmem worker-node-1 2048M --config 

# worker-node-2
# Max memory: 2097152 KiB (2 GB)
# Used memory: 2097152 KiB (2 GB)
virsh setmaxmem worker-node-2 2048M --config
virsh setmem worker-node-2 2048M --config 
```
- [x] Checked the disk image path (SSD) and sizes

```bash
# The path that is displayed under Source:
virsh domblklist control-plane-1
virsh domblklist worker-node-1
virsh domblklist worker-node-2

# Current image sizes before resizing
sudo qemu-img info /var/lib/libvirt/images/control-plane-1.qcow2
sudo qemu-img info /var/lib/libvirt/images/worker-node-1.qcow2
sudo qemu-img info /var/lib/libvirt/images/worker-node-2.qcow2
```
- [x] Resized the disk images

```bash
# Resized the image size from 10 GB - 30 GB for all nodes
sudo qemu-img resize /var/lib/libvirt/images/control-plane-1.qcow2 30G
sudo qemu-img resize /var/lib/libvirt/images/worker-node-1.qcow2 30G
sudo qemu-img resize /var/lib/libvirt/images/worker-node-2.qcow2 30G
```
- [x] Start the VMs 
- [x] SSH into all nodes
- [x] Run in all nodes individually
```bash
lsblk # shows disk info
df -h # shows disk usage being used/unused
df -T # shows Filesystem Type (ext4)
```
- [x] Root-filesystem expanded, since the VM disk was resized but did not apply to the root-filesystem. 
```bash
# control-plane-1
sudo apt update
sudo apt install -y cloud-guest-utils
sudo growpart /dev/vda 3
sudo pvresize /dev/vda3
sudo lvextend -r -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv

# worker-node-1
sudo apt update
sudo apt install -y cloud-guest-utils
sudo growpart /dev/vda 2
sudo resize2fs /dev/vda2

# worker-node-2
sudo apt update
sudo apt install -y cloud-guest-utils
sudo growpart /dev/vda 2
sudo resize2fs /dev/vda2
```
---

## Round-up
The resource adjustments took more time than expected, so the monitoring setup is still WIP, however it is more than 50 % done. The complete `kube-prometheus-stack` is downloaded. The next step would be to verify the monitoring functionality locally before moving on to exposing it through Ingress + Traefik. 
Checklists were created for monitoring, but also a new document named **environment-requirements.md** found in **~/graduation-project-2026/docs/**. 

This will be a requirements document that will list recommended specifications before even installing VMs. This is to avoid the resource allocation limitations early.
