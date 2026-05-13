# NetBackup — Architecture

<div class="kb-summary">
Veritas NetBackup three-tier architecture — Primary Server catalog and scheduling, Media Servers for data movement, and Clients with backup agents.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Three-tier topology, key processes, storage units, catalog backup, and sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware VADP, Oracle RMAN, NDMP, and cloud storage integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Policy naming, retention schedules, MSDP standards, and media server placement.</span></a>
</div>

| Component | Role |
|---|---|
| Primary Server | Central scheduler, catalog DB (PostgreSQL), EMM device database |
| Media Server | Data mover; writes to storage units; runs deduplication (MSDP) |
| Client | Backup agent on protected host; sends data to Media Server via TCP 13724 |
| MSDP | Media Server Deduplication Pool; inline dedup; supports AIR image replication |
| Catalog | Most critical component — tracks all backup images; must be protected separately |

```mermaid
graph TB
  MASTER["Primary Server\nCatalog · Scheduler · EMM DB"] -->|"TCP 1556 policy/job control"| MS1["Media Server 1\nSite A"]
  MASTER --> MS2["Media Server 2\nSite B / DR"]
  MS1 --> MSDP1[("MSDP Pool\nSite A")]
  MS2 --> MSDP2[("MSDP Pool\nSite B")]
  MSDP1 -->|"AIR replication"| MSDP2
  MSDP2 -->|"SLP copy"| CLOUD[("Cloud Storage\nlong-term archive")]
  CLIENT1(["VMware VADP host"]) -->|"TCP 13724 bpcd"| MS1
  CLIENT2(["Oracle / MSSQL agent"]) -->|"TCP 13724 bpcd"| MS1
  classDef master fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef media fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef store fill:#b45309,stroke:#92400e,color:#fff
  classDef client fill:#15803d,stroke:#166534,color:#fff
  class MASTER master
  class MS1,MS2 media
  class MSDP1,MSDP2,CLOUD store
  class CLIENT1,CLIENT2 client
```
