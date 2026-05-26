# Linux Server

<div class="kb-summary">
Linux server infrastructure running RHEL and Ubuntu — systemd service management, LVM2 storage, LACP bonded networking, SELinux/AppArmor security, and Ansible-driven automation for enterprise workloads.
</div>

```
┌────────────────────────────────────────── Linux — Overview ───────────────────────────────────────────┐
│                                                                                                       │
│  Linux is the open-source OS kernel underpinning servers, containers, and cloud infrastructure.       │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Core Subsystems       │  │      Key Distributions      │  │          Use Cases          │   │
│   │   Kernel: process + memory  │  │   RHEL/CentOS: enterprise   │  │       Web/app servers       │   │
│   │  Filesystem: VFS + ext4/xfs │  │   Ubuntu: cloud + desktop   │  │       Container hosts       │   │
│   │  Network: TCP/IP + iptables │  │     Debian: stable base     │  │        HPC workloads        │   │
│   │   Systemd: service + boot   │  │    SUSE: SAP + Kubernetes   │  │         Embedded/IoT        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · CPU · RAM · NIC · storage disks/LUNs                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Kernel       = core OS code managing hardware, memory, processes, drivers                            │
│  VFS          = Virtual File System; abstraction layer over real filesystems                          │
│  Systemd      = init system and service manager; PID 1 on most modern distros                         │
│  RHEL         = Red Hat Enterprise Linux; subscription-based enterprise distro                        │
│  CentOS       = RHEL-compatible free rebuild; CentOS Stream is upstream of RHEL                       │
│  iptables     = netfilter firewall rules; nftables is modern replacement                              │
│  ext4         = default Linux filesystem; journalled, supports large files                            │
│  xfs          = high-performance journalled FS; default on RHEL 7+                                    │
│  cgroups      = control groups; limit CPU/memory/IO per process group                                 │
│  namespaces   = isolate PID/net/mount/user views; foundation of containers                            │
│  SELinux      = mandatory access control; labels processes and files                                  │
│  systemctl    = command to start/stop/enable/status systemd services                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
