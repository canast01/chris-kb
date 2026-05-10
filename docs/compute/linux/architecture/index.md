# Linux — Overview

Architecture overview, design principles, and topology.

## Server Roles

Linux servers fulfill multiple infrastructure roles:

| Role | Typical OS | vCPU | RAM | Notes |
|---|---|---|---|---|
| Application server | RHEL 8/9, Ubuntu 22.04 | 4–16 | 8–64 GB | Primary workload host |
| Automation node (Ansible) | RHEL 9 | 4 | 8 GB | Ansible control plane; no inbound access |
| Monitoring server | Ubuntu 22.04 | 8 | 16 GB | Prometheus, Grafana, exporters |
| NFS/SMB file host | RHEL 9 | 4 | 16 GB | Shared storage; LVM on SAN-backed LUNs |
| Container host | RHEL 9 | 8–32 | 16–128 GB | Podman/Docker workloads |
| Backup proxy (Linux) | RHEL 9 | 8 | 16 GB | Veeam proxy or NetBackup media server |


## Server Role Topology

```mermaid
graph TB
  KERNEL["Linux Kernel\nRHEL / Ubuntu / SLES"]
  KERNEL --> STORAGE["Storage Stack\nlvm2 · dm-multipath · xfs/ext4"]
  KERNEL --> NET["Network Stack\nnm · bonding · firewalld"]
  KERNEL --> SVCS["systemd Services\nsshd · rsyslog · cron"]
  KERNEL --> SEC["Security\nSELinux / AppArmor · auditd · PAM"]
  STORAGE --> DISK[("Block Devices\n/dev/sd* / /dev/mapper/*")]
  NET --> NIC["Physical NICs\neth0 / bond0 / enp*"]
  ADMIN(["Sysadmin"]) -->|"SSH / console"| KERNEL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class KERNEL ctrl
  class STORAGE,SVCS,SEC net
  class DISK store
  class NIC,NET net
  class ADMIN host
```

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
