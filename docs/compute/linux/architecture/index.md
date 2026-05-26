# Linux — Architecture

<div class="kb-summary">
Linux server infrastructure running RHEL and Ubuntu — systemd service management, LVM2 storage with dm-multipath, LACP bonded networking, SELinux/AppArmor security enforcement, and Ansible-driven automation.
</div>

```
┌───────────────────────────────────────── Linux Architecture ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Linux Kernel (monolithic + loadable modules)                         │   │
│   │     Process scheduler: CFS — Completely Fair Scheduler; time-slices CPU per cgroup weight     │   │
│   │        Memory manager: virtual address spaces, page tables, TLB, OOM killer, hugepages        │   │
│   │       VFS: Virtual File System layer — unified API over ext4, XFS, Btrfs, tmpfs, procfs       │   │
│   │      Syscall interface: glibc wraps int 0x80 / SYSCALL into POSIX functions for userspace     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Kernel subsystems provide isolation, scheduling, and I/O to all userspace processes                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Namespaces & cgroups             │  │                systemd & init               │   │
│   │         pid: process tree isolation          │  │            PID 1: systemd is init           │   │
│   │         net: network stack isolation         │  │          Units: service/timer/mount         │   │
│   │          mnt: mount point isolation          │  │        Targets: multi-user/graphical        │   │
│   │         cgroup v2: CPU/mem/IO limits         │  │         journald: structured logging        │   │
│   │         user: UID mapping isolation          │  │         socket activation: on-demand        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 CPUs · RAM DIMMs · NVMe/SAS disks · NIC · iDRAC/iLO BMC · Power & Cooling                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CFS         = Completely Fair Scheduler; distributes CPU time using a red-black tree                 │
│  VFS         = Virtual File System; kernel abstraction layer over concrete filesystems                │
│  cgroups     = Control Groups; enforce per-process CPU, memory, and I/O resource limits               │
│  namespace   = Kernel isolation primitive; wraps PIDs, network, mounts, UIDs independently            │
│  systemd     = PID 1 init; manages units (services, timers, mounts) and the boot sequence             │
│  journald    = systemd journal daemon; stores structured binary logs with metadata fields             │
│  OOM killer  = Out-of-Memory killer; terminates processes when the kernel exhausts RAM                │
│  hugepages   = 2 MB / 1 GB pages; reduce TLB misses for memory-intensive workloads                    │
│  tmpfs       = RAM-backed filesystem; used for /tmp, /dev/shm, and systemd runtime dirs               │
│  procfs      = /proc virtual filesystem; exposes kernel and process state as readable files           │
│  syscall     = Kernel entry point; userspace requests OS services via a defined ABI                   │
│  loadable module= .ko kernel object loaded/unloaded at runtime via modprobe/rmmod                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Linux Architecture](../../../assets/linux-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">Kernel subsystem architecture, server roles, LVM storage stack, network stack, and key CLI reference.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">SAN/NFS storage connectivity, Ansible automation, monitoring (Prometheus/Grafana), and AD/LDAP auth.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">Disk layout standards, VLAN and bonding design, package repository policy, and hardening baseline.</div>
  </a>
</div>

## Server Roles

| Role | Typical OS | vCPU | RAM | Notes |
|---|---|---|---|---|
| Application server | RHEL 8/9, Ubuntu 22.04 | 4–16 | 8–64 GB | Primary workload host |
| Automation node (Ansible) | RHEL 9 | 4 | 8 GB | Control plane; no inbound access |
| Monitoring server | Ubuntu 22.04 | 8 | 16 GB | Prometheus, Grafana, exporters |
| NFS/SMB file host | RHEL 9 | 4 | 16 GB | Shared storage; LVM on SAN-backed LUNs |
| Container host | RHEL 9 | 8–32 | 16–128 GB | Podman/Docker workloads |
| Backup proxy | RHEL 9 | 8 | 16 GB | Veeam proxy or NetBackup media server |

## Topology


