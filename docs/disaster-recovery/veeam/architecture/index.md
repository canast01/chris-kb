# Veeam — Architecture Overview

Veeam provides backup, replication, recovery, and disaster recovery capabilities for virtual, physical, and cloud workloads.

## Architecture Diagram

```mermaid
graph TB
  VBR["Veeam Backup & Replication Server"] --> PROXY["Backup Proxy\n(data mover)"]
  PROXY --> REPO[("Backup Repository\nSOBR / immutable")]
  VCTR(["VMware vCenter\nsource VMs"]) --> PROXY
  REPO -->|"capacity tier"| OBJ[("Object Storage\nS3 / Azure Blob")]
  REPO -->|"tape offload"| TAPE[("Tape Library")]
  ADMIN(["Backup Admin"]) -->|"console"| VBR
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class VBR,PROXY ctrl
  class REPO,TAPE store
  class VCTR,ADMIN host
  class OBJ cloud
```

## Backup Proxy

The proxy is the workhorse of Veeam — it reads VM data and writes to the repository:

- **Transport modes** (VMware):
  - Hot-add (SAN): proxy VM attached to the production datastore — highest throughput
  - Direct NFS: for NFS datastores — bypasses ESXi, directly reads NFS
  - Network (NBD): fallback when SAN/NFS not available — slowest
- Deploy minimum 2 proxies per site for redundancy and parallel job capacity
- Proxies auto-selected by Veeam based on available throughput — no manual assignment needed for most cases

## Scale-Out Backup Repository (SOBR)

SOBR provides tiered storage without managing individual repository capacity.

```mermaid
flowchart LR
    job(["Backup Job\n(daily run)"])

    subgraph sobr [Scale-Out Backup Repository]
        direction TB
        pe1[("Performance Extent 1\nfast disk — NFS / XFS\n0-14 days")]
        pe2[("Performance Extent 2\nfast disk — second node\n0-14 days")]
        ct[("Capacity Tier\nS3-compatible object storage\n14+ days — immutable")]
        pe1 -->|"auto-offload\nafter threshold"| ct
        pe2 -->|"auto-offload"| ct
    end

    job --> pe1
    job --> pe2

    ct -->|"archive tier\nS3 Glacier"| glacier[("Glacier / Archive\nyearly retention")]

    classDef peNode fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef ctNode fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef archNode fill:#0f766e,stroke:#0d5f58,color:#fff
    classDef src fill:#15803d,stroke:#166534,color:#fff
    class pe1,pe2 peNode
    class ct ctNode
    class glacier archNode
    class job src
```

Configure SOBR offload: Backup Infrastructure → Scale-Out Repositories → right-click → Properties → Capacity Tier.

## NAS Backup (File Share Backup)

Veeam 12+ supports backup of SMB/NFS shares via dedicated File Share backup jobs:

- Creates a dedicated File Backup Proxy and cache repository
- Processes changed files using VSS or NAS snapshot integration
- Restore granularity: individual files, folder-level, or point-in-time snapshot

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
