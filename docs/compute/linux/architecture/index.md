---
tags:
  - architecture
  - linux
---
# Linux — Architecture

<div class="kb-summary">
Linux server infrastructure running RHEL and Ubuntu — systemd service management, LVM2 storage with dm-multipath, LACP bonded networking, SELinux/AppArmor security enforcement, and Ansible-driven automation.

*Applies to: RHEL 8.x / 9.x · Ubuntu 22.04 / 24.04*
</div>

```text
┌──────────────────────────────── Linux Platform Architecture Overview ─────────────────────────────────┐
│                                                                                                       │
│  Linux underpins most infrastructure; RHEL/CentOS for enterprise, Ubuntu for cloud;                   │
│  kernel + systemd + package manager form the core; network via NetworkManager or nmcli.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Distributions                 │  │               Core Components               │   │
│   │         RHEL: enterprise production          │  │         Kernel: hardware abstraction        │   │
│   │         CentOS Stream: upstream test         │  │           systemd: service manager          │   │
│   │            Ubuntu: cloud + DevOps            │  │          glibc: C standard library          │   │
│   │            Debian: stable/minimal            │  │               PAM: auth stack               │   │
│   │          SLES: SAP + HPC workloads           │  │          NetworkManager: networking         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Choose distro based on vendor support matrix; RHEL for VMware, vSAN, SAP, Oracle.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Package Management              │  │             Storage and Security            │   │
│   │          RPM/DNF: RHEL/CentOS/SLES           │  │             LVM: logical volumes            │   │
│   │           APT/dpkg: Debian/Ubuntu            │  │            ext4/XFS: filesystems            │   │
│   │          Subscription: RHEL + SLES           │  │            SELinux/AppArmor: MAC            │   │
│   │          Repos: local mirror or CDN          │  │            firewalld/nftables: FW           │   │
│   │         Errata: security + bug fixes         │  │           SSH: remote access (22)           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 or ARM64 bare metal or VM; NIC (1/10/25GbE); local disk or SAN/NAS;                           │
│  IPMI/iDRAC/iLO for OOB management; firmware and BIOS managed separately.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RHEL           = Red Hat Enterprise Linux; subscription required; 10-year support                    │
│  systemd        = Linux init system and service manager; PID 1; unit files                            │
│  DNF            = package manager for RHEL 8+; replaces yum                                           │
│  LVM            = Logical Volume Manager; flexible disk partitioning                                  │
│  SELinux        = Security-Enhanced Linux; Mandatory Access Control by policy                         │
│  PAM            = Pluggable Authentication Modules; Linux auth stack                                  │
│  glibc          = GNU C Library; fundamental library all Linux programs use                           │
│  NetworkManager = service that manages network interfaces and connections                             │
│  firewalld      = RHEL firewall daemon; zones and rules; wraps nftables/iptables                      │
│  XFS            = default filesystem for RHEL 7+; high performance, no shrink                         │
│  Subscription   = RHEL/SLES entitlement; required for security patches                                │
│  Errata         = security advisory with associated package updates                                   │
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

