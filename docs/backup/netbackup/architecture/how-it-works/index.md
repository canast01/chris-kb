---
tags:
  - architecture
  - netbackup
---
# NetBackup — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Three-Tier Topology, Domain Sizing Guidelines.

*Applies to: NetBackup 10.x*
</div>
![NetBackup — How It Works](../../../../assets/backup-netbackup-architecture-how-it-works-index.svg)



## Overview

NetBackup operates on a three-tier architecture: a centralized Primary Server (formerly Master Server) coordinates all operations via policy scheduling, catalog management, and resource arbitration. Media Servers handle data movement — reading from clients and writing to storage units. The Catalog is the operational heartbeat of the entire deployment, storing all image metadata, policies, and media inventory.

## Three-Tier Topology

```mermaid
graph TB
    Primary["Primary Server<br/>catalog · policy engine<br/>nbpem · scheduler · job control"]
    MediaSrv["Media Servers<br/>proxy I/O · MSDP dedup pools<br/>compression · encryption"]
    Clients["Clients<br/>NBU agent · bpbkar<br/>Windows · Linux · NAS"]
    Storage["Storage Units<br/>AdvancedDisk · MSDP pool<br/>tape robot · cloud LSU"]

    Primary -->|"schedules + orchestrates"| MediaSrv
    Primary -->|"schedules + orchestrates"| Clients
    Clients -->|"data path"| MediaSrv
    Primary -->|"catalog queries"| Storage
    MediaSrv -->|"stores backups"| Storage

    style Primary fill:#2563eb,stroke:#1d4ed8,color:#fff
    style MediaSrv fill:#15803d,stroke:#166534,color:#fff
    style Clients fill:#b45309,stroke:#92400e,color:#fff
    style Storage fill:#7c3aed,stroke:#6d28d9,color:#fff
```

Store the DR file off-host (NAS/object storage) and the passphrase in a secure vault — both are required for catalog recovery.

## Domain Sizing Guidelines

| Environment Scale | Primary Server vCPU | RAM | Catalog Disk |
|---|---|---|---|
| Small (<500 clients) | 8 vCPU | 32 GB | 500 GB |
| Medium (500–2000 clients) | 16 vCPU | 64 GB | 2 TB |
| Large (>2000 clients) | 32 vCPU | 128 GB | 5–10 TB |

Catalog disk should be on SSD/NVMe — IOPS under load are significantly higher than sequential throughput figures suggest.

---

## See also

- [Netbackup — Design Standards](../design-standards/)
- [Netbackup — Integrations](../integrations/)
- [Netbackup — Deploy](../../deploy/)
