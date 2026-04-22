## Disclaimer

These draft notes are based on environment-specific configurations (hardcoded values such as IP addresses and hostnames).

They are intended for personal documentation and learning purposes only, and may not be directly applicable to other environments without modification.

For a generalized and reproducible setup, refer to the corresponding template-based documentation.

# Draft notes 20/4 2026

These are the initial steps for the project. This document will be used as a checklist for technical advancements and progress made along the way. However this document is stricly made for personal use and personal progression. Relevant documents and technical attachments will be added as the project progresses.

- Created a repository named **graduation-project-2026**
- Created 3 VMs: **control-plane-1, worker-node-1, worker-node-2**
- CPU Cores and memory for **control-plane-1: 2 CPU cores. 1500 memory**
- CPU Cores and memory for **worker-node-1, worker-node-2: 1 CPU cores, 1500 memory**
- All VM's have Linux Ubuntu server LTS installed and configured.

# Draft notes 21/4 2026

Since i'm using my desktop that has Windows and my project is on my Linux laptop. The morning was dedicated to create a SSH setup that can connect smoothly. VS Code Remote SSH makes this possible to create a Git workflow that will become useful down the line when connecting to the Kubernetes environment.

- Enabled and installed SSH on the Linux Laptop.
- Became more familiar with commands for connecting remotely
- Succesfully created a SSH connection between the desktop and laptop.
- Created checklists that are hardcoded for personal use and generalized for non personal use
- everything named **template** is for non personal use
- Adjusted the `.ssh` config:

 ```ssh
 Host linux-laptop
    HostName 192.168.1.116
    User altamiranos
 ```
 ```ssh
 Host control-plane-1
    HostName 192.168.122.221
    User altamiranos
 ```
 ```ssh
 Host worker-node-1
    HostName 192.168.122.113
    User altamiranos
 ```
 ```ssh
 Host worker-node-2
    HostName 192.168.122.42
    User altamiranos
 ```
"
Since the KVM has a "built in" DHCP i decided to leave the IP:s as they are. The ideal would be to assign Static IP:S but since the scope is on a smaller scaler it is doable this way. 

The virtualized environment is using a default network that should be enough. Aliases were also added for smoother access and easier navigation. 

Tomorrows plan is to use the checklist to perform a thorough preflight before installing k3s.  

# Draft notes 22/4 2026 

The day commenced with starting up all the VMs. I've noticed that i needed to enable SSH on both the worker-nodes. This was a quick fix. Now that i have SSH working for every component i started the preflight check. This is based on the **preflight-checklist.md** found in **~/docs/k3s/**

- Infrastructure
- Networking
- SSH Access
- System Preparation
- System Validation

After the preflight is done, it was time to install k3s. The first step is to create the control-plane and later move on to create the worker-nodes. 

### k3s install

The installation went very smooth, i had no issues getting the cluster up and running. However all the documentation that i decided to make (hardcoded and non-hardcoded) is taking a bit of time, this is still important to have project reproducible, so this is important. The installation process is based on the **k3s-install-checklist.md**  found in **~/docs/k3s/**

- Control plane installed on control-plane-1 
- Joined the worker node 1 to the control plane trough Token and IP
- Joined the worker node 2 to the control plane trough Token and IP
- Verified that `sudo kubectl get nodes` and `sudo kubectl get pods -A` works 


