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
- Adjusted the `.ssh` config:

 ```ssh
 Host linux-laptop
    HostName 192.168.1.116
    User altamiranos
 ```
 ```ssh
 Host control-plane-1
    HostName 192.168.1.221
    User altamiranos
 ```
 ```ssh
 Host worker-node-1
    HostName 192.168.1.113
    User altamiranos
 ```
 ```ssh
 Host worker-node-2
    HostName 192.168.1.42
    User altamiranos
 ```
"
Since the KVM has a "built in" DHCP i decided to leave the IP:s as they are. The ideal would be to assign Static IP:S but since the scope is on a smaller scaler it is doable this way. 

The virtualized environment is using a default network that should be enough. Aliases were also added for faster 

