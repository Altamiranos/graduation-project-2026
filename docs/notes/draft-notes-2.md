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

Plan for tomorrow: Adjust the resources in the cluster. Especially the disk capacity, then verify the Grafana locally and when successful - expose the monitoring through Ingress + Traefik. Finish the checklists **k3s-monitoring-checklist.md** and **k3s-monitoring-checklist-template.md** 

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

# Draft notes 29/4 2026
Progress is going to be a bit slow the coming days. Focus has shifted a bit towards writing the report for the project. This decision was made to meet deadline the 17th of May efficiently. However back to configuring the monitoring both locally and exposed through Ingress.

I needed to access the `localhost:3000` through tunneling and SSH. I used port-forwarding to verify that the Grafana was working as expected. By using the following:

- Get admin credentials and port-forwarding through `localhost:3000` 
```bash
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d

kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

- SSH tunnel
```bash
ssh -L 3000:localhost:3000 altamiranos@control-plane-1
```

After verifying the Grafana locally and that the dashboards were visualizing, and the Prometheus gathering metrics. I took some screenshots and checked the following dashboards: 

- **Kubernetes / Compute Resources** 
- / Node
- / Pod
- / Namespace
- / Cluster

This process was successful and all checked dashboards were showing metrics as expected. The results make it possible to move on and expose the monitoring through the ingress.

Created the manifest **grafana-monitoring-ingress.yaml** for exposing through the ingress found in **~/graduation-project-2026/deployment/**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-monitoring-ingress
  namespace: monitoring
spec:
  ingressClassName: traefik
  rules:
    - host: grafana.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: monitoring-grafana
                port:
                  number: 80
```
- The file was then copied to the cluster
```bash
scp deployment/grafana-monitoring-ingress.yaml altamiranos@control-plane-1:~
```
- The file was applied from the control plane
```bash
kubectl apply -f grafana-monitoring-ingress.yaml
```
- Verified the ingress and service from the control plane
```bash
kubectl get ingress -n monitoring
kubectl get svc -n monitoring | grep grafana
```

The host grafana.local was later added to the Windows hosts file and mapped to 127.0.0.1., the same process used for the FastAPI configuration. This was necessary to be able to create a tunnel from the PC and create access to the exposed Grafana

- An attempt was done by creating a tunnel through port `18080`

```powershell
ssh -N -L 127.0.0.1:18080:192.168.122.221:80 linux-laptop
```
- However this was unsuccessful and resulted in the following message:

```powershell
PS C:\Users\Sander> ssh -N -L 127.0.0.1:18080:192.168.122.221:80 linux-laptop
altamiranos@192.168.1.116's password: 
bind [127.0.0.1]:18080: Permission denied
channel_setup_fwd_listener_tcpip: cannot listen to port: 18080
Could not request local forwarding.
```
- By changing the port to `30080` the tunnel was successful.

```powershell
 ssh -L 127.0.0.1:30080:192.168.122.221:80 linux-laptop   
altamiranos@192.168.1.116's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-22-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Expanded Security Maintenance for Applications is enabled.

35 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Last login: Sun May  3 13:32:57 2026 from 192.168.1.45
```
This was also verified by accessing Grafana through `http://grafana.local:30080` in the browser. and curl in another powershell terminal.

```powershell
 curl.exe -v --max-time 10 -H "Host: grafana.local" http://127.0.0.1:30080
*   Trying 127.0.0.1:30080...
* Established connection to 127.0.0.1 (127.0.0.1 port 30080) from 127.0.0.1 port 50277 
* using HTTP/1.x
> GET / HTTP/1.1
> Host: grafana.local
> User-Agent: curl/8.18.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 302 Found
< Cache-Control: no-store
< Content-Type: text/html; charset=utf-8
< Date: Sun, 03 May 2026 12:09:00 GMT
< Location: /login
< Vary: Accept-Encoding
< X-Content-Type-Options: nosniff
< X-Frame-Options: deny
< X-Xss-Protection: 1; mode=block
< Transfer-Encoding: chunked
< 
<a href="/login">Found</a>.

* Connection #0 to host 127.0.0.1:30080 left intact
```
Grafana is now exposed internally through Traefik Ingress and can be accessed externally from the Windows machine through an SSH tunnel! 

# Draft Notes 30/4 2026

After finishing up the monitoring, it's time to wrap up the technical aspect of the requirements of the project with the RBAC implementation. This will be held to a minimum however. The RBAC will show a small dmeonstration for how roles, permissions and `ServiceAccounts` function in Kubernetes.

The goal here is to use the built-in RBAC in Kubernetes for imporving the security and authentication inside of the environment. The following will be covered:

- RBAC (Built-in)
- ServiceAccount
- Role
- RoleBinding
- Access control
- Namespace Isolation

Created and modified the following: **fastapi-serviceaccount.yaml, rbac-readonly.yaml, fastapi.yaml** found in **graduation-project-2026/deployment/**. Then moved on to copy the files to the control-plane-1:
```bash

# cpy from linux-laptop -> control plane

scp fastapi-serviceaccount.yaml altamiranos@control-plane-1:~
scp fastapi.yaml altamiranos@control-plane-1:~
scp rbac-readonly.yaml altamiranos@control-plane-1:~

# after the copy, applied the manifests from control plane

kubectl apply -f fastapi-serviceaccount.yaml
kubectl apply -f fastapi.yaml
kubectl apply -f rbac-readonly.yaml
```

An error was encountered were i recieved the Error: ErrImageNeverPull. This was resolved rather easily by importing the image a second time, and then cleaning up the Faulty pods, which the environment later replaced. 

```bash
# Import and list
sudo k3s ctr images import ~/fastapi-k3s.tar
sudo k3s ctr images list | grep fastapi

# Deleted the faulty pods
kubectl delete pod fastapi-app-55f5c64d87-n4j87 
kubectl delete pod fastapi-app-688955b895-m2f4b

# Verified the pods very terminated and running
kubectl get pods -o wide
```
- Verified RBAC permissions
```bash

# fastapi-readonly can read pods and list services
echo "Allowed in default namespace:"
kubectl auth can-i get pods --as=system:serviceaccount:default:fastapi-readonly -n default
kubectl auth can-i list services --as=system:serviceaccount:default:fastapi-readonly -n default

# fastapi-readonly is not able to delete pods, create deployments, read secrets
echo "Denied write/sensitive actions:"
kubectl auth can-i delete pods --as=system:serviceaccount:default:fastapi-readonly -n default
kubectl auth can-i create deployments --as=system:serviceaccount:default:fastapi-readonly -n default
kubectl auth can-i get secrets --as=system:serviceaccount:default:fastapi-readonly -n default

# fastapi-readonly is limited to default namespace
echo "Namespace isolation:"
kubectl auth can-i get pods --as=system:serviceaccount:default:fastapi-readonly -n monitoring
```
- Output from the verification

```bash

Allowed in default namespace:
yes
yes

Denied write/sensitive actions:
no
no
no

Namespace isolation:
no
```
This demonstrated the following: 

RBAC can control what an account is allowed to do, which resources it can access, and which namespace the access applies to. The read-only ServiceAccount was able to inspect pods and services in the default namespace, but it was not allowed to modify resources, read secrets, or access the monitoring namespace.

Created a template for the `ServiceAccount` and a hardcoded version. This concludes the technical aspects!

Created YAML
- fastapi-serviceaccount.yaml
- fastapi-serviceaccount-template.yaml
- grafana-monitoring-ingress.yaml
