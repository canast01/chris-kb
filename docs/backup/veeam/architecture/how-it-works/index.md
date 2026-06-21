---
tags:
  - architecture
  - veeam
---
# Veeam — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Architecture, Supported Platforms, Retention Schedule, Sizing Guidelines and 1 more sections.

*Applies to: Veeam Backup & Replication 12.x*
</div>
![Veeam — How It Works](../../../../assets/backup-veeam-architecture-how-it-works-index.svg)



## Overview

Veeam Backup & Replication provides backup, replication, recovery, and disaster recovery for virtual, physical, and cloud workloads. The Backup Server manages scheduling and configuration. Backup Proxies perform data movement via VMware VADP or agent-based reads. The Scale-Out Backup Repository (SOBR) provides tiered storage — fast disk for short-term, object storage for long-term.

## Architecture

```mermaid
graph LR
    VMs["VMs / Workloads<br/>vSphere · Hyper-V<br/>Physical · Cloud"]
    Proxy["Backup Proxy<br/>transport: SAN / HotAdd / NBD<br/>CBT · compression · dedup"]
    Repo["Backup Repository<br/>local disk · NAS · S3<br/>tape · SOBR tiers"]
    VeeamONE["Veeam ONE<br/>monitoring · reporting<br/>dashboards · capacity"]
    Console["Veeam BR Console<br/>admin · REST API<br/>job engine · catalog"]

    VMs -->|"backup job"| Proxy
    Proxy -->|"writes backup chains"| Repo
    VeeamONE -->|"monitors"| Repo
    Console -->|"orchestrates"| VMs
    Console -->|"orchestrates"| Proxy
    Console -->|"orchestrates"| Repo
    Console -->|"orchestrates"| VeeamONE

    style VMs fill:#2563eb,stroke:#1d4ed8,color:#fff
    style Proxy fill:#2563eb,stroke:#1d4ed8,color:#fff
    style Repo fill:#15803d,stroke:#166534,color:#fff
    style VeeamONE fill:#b45309,stroke:#92400e,color:#fff
    style Console fill:#7c3aed,stroke:#6d28d9,color:#fff
```

## Supported Platforms

| Platform | Method |
|---|---|
| VMware vSphere | VADP, agentless |
| Microsoft Hyper-V | HV provider, agentless |
| Physical Windows | Veeam Agent for Windows (VAW) |
| Physical Linux | Veeam Agent for Linux (VAL) |
| AWS EC2 | Veeam Backup for AWS (separate appliance) |
| Azure VMs | Veeam Backup for Azure (separate appliance) |

## Retention Schedule

| Level | Restore Points | Schedule | Repository |
|---|---|---|---|
| Daily | 14 | Incremental (synthetic full weekly) | Performance tier (fast disk) |
| Weekly | 8 | Synthetic full | Performance tier |
| Monthly | 12 | Active full (monthly) | SOBR capacity tier offload |
| Yearly | 7 | Active full (yearly) | Object storage archive |

## Sizing Guidelines

| Scale | Backup Server | Proxies per Site |
|---|---|---|
| < 100 VMs | 4 vCPU, 8 GB RAM | 1–2 |
| 100–500 VMs | 8 vCPU, 16 GB RAM | 2–4 |
| 500–2,000 VMs | 16 vCPU, 32 GB RAM (+ full SQL) | 4–8 |

## Instant VM Recovery RTO Targets

| Application Tier | Target RTO |
|---|---|
| Tier 1 (critical DB, ERP) | < 15 minutes via Instant VM Recovery |
| Tier 2 (business apps) | < 1 hour |
| Tier 3 (dev/test) | < 4 hours |

---

## See also

- [Veeam — Design Standards](../design-standards/)
- [Veeam — Integrations](../integrations/)
- [Veeam — Deploy](../../deploy/)
