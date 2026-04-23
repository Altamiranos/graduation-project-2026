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

The day commenced with starting up all the VMs. I've noticed that i needed to enable SSH on both the worker-nodes. This was a quick fix. Now that i have SSH working for every component i started the preflight check. This is based on the **preflight-checklist.md** found in **~/graduation-project-2026/docs/k3s/**

- Infrastructure
- Networking
- SSH Access
- System Preparation
- System Validation

After the preflight is done, it was time to install k3s. The first step is to create the control-plane and later move on to create the worker-nodes. 

### k3s install

The installation went very smooth, i had no issues getting the cluster up and running. However all the documentation that i decided to make (hardcoded and non-hardcoded) is taking a bit of time, this is still important to have project reproducible, so this is important. The installation process is based on the **k3s-install-checklist.md**  found in **~/graduation-project-2026/docs/k3s/**

- Control plane installed on control-plane-1 
- Joined the worker node 1 to the control plane trough Token and IP
- Joined the worker node 2 to the control plane trough Token and IP
- Verified that `sudo kubectl get nodes` and `sudo kubectl get pods -A` works 


# Draft notes 23/4 2026 

The cluster is alive and well. The first drafts of the progress so far is also written. This will be the standard workflow and process moving forward. There are two options of moving forward with Deployment that is the next step, i can create a basic deplyment with kubectl create or write my own .yaml files for it. Since This project focuses on growth and is a valuable learning experience i decided to go with the second option. I'm also aware of the nginx/demo that is usually used for the "testdeployment" This is not being used for my own deployment tho, because nginx is not used in this project. This was decided from the start of the project and will be followed trough. 

The deployment will instead be:
- FastAPI-service (simplified): `main-py`, `Dockerfile`, `deployment.yaml`, `service.yaml`
- The idea is to use FastAPI because of it's relevance and modernism. This could result in a very valuable learning experience even if it is created on a small scale for the limited infrastructure that this project is based on.
- This will be timeconsuming, however could be very worth it. High risk - High reward!

Since the whole project is based on k3s, FastAPI deployment will be done trough **Podman** as a builder and **containerd** as a runtime, instead of using Docker. These alternatives are even more lightweight and are also completely open-source while docker has been in a grey-zone lately with their licensing.  

**FastAPI app:**
1. Build as a container image trough podman
2. Imports to k3s
3. Standard-runtime by containerd
---

Created a directory: ~/graduation-project-2026/app. This is where the `main.py` and `Dockerfile` will be. 

This is based on **main.py, fastapi-k3s.tar, Dockerfile** found in **~/graduation-project-2026/app/**

- Created an image in **Dockerfile** for FastAPI
- Build an image trough podman for **fastapi.yaml**
- Exported created image as **fastapi-k3s.tar**
- Sent created image to control-plane-1
- Sent **Dockerfile** to control-plane-1
- Sent **fastapi-k3s.tar** to control-plane-1
- Sent **fastapi-k3s.tar** to worker-node-1
- Sent **fastapi-k3s.tar** to worker-node-2

Issues encountered: When deploying the fastapi, i got the status ErrImageNeverPull. This will be troubleshooted tomorrow.

```bash
Events:
  Type     Reason             Age                    From               Message
  ----     ------             ----                   ----               -------
  Normal   Scheduled          3m56s                  default-scheduler  Successfully assigned default/fastapi-app-7dd646d7c5-b9mm2 to worker-node-1
  Warning  Failed             101s (x12 over 3m56s)  kubelet            Error: ErrImageNeverPull
  Warning  ErrImageNeverPull  90s (x13 over 3m56s)   kubelet            Container image "fastapi-k3s:1.0" is not present with pull policy of Never
 ```
 ---
This is based on **fastapi.yaml** found in **~/graduation-project-2026/deployment/**
- Created a deployment manifest and a service manifest
- Comments were added for more transparency
- The deployment and service manifests were put in the same .yaml named **fastapi.yaml**

Plan for tomorrow: Troubleshoot the ErrImageNeverPull to running. Afterwards continue deployment and finish checklists for deployment. One for template and one for you.