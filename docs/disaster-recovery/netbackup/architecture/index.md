# NetBackup — Architecture Overview

## Three-Tier Topology

```mermaid
flowchart TD
    subgraph masterTier [Primary Server]
        master["Primary Server\nCatalog DB · Policy DB\nJob Scheduler · EMM DB"]
    end

    subgraph mediaTier [Media Servers]
        ms1["Media Server 1\nSite A"]
        ms2["Media Server 2\nSite B / DR"]
        ms3["Media Server 3\nCloud Gateway"]
    end

    subgraph storageTier [Storage Units]
        msdp1[("Disk / MSDP\ndedup pool\nSite A")]
        msdp2[("Disk / MSDP\nDR copy\nSite B")]
        cloud[("Cloud — S3\nlong-term archive")]
    end

    subgraph clientTier [Clients]
        vmHost(["VMware backup host\nVADP"])
        dbHost(["Oracle / MSSQL\nagent"])
        nasHost(["NAS — NDMP"])
    end

    master -->|"policy / job control\nTCP 1556"| ms1
    master -->|"policy / job control"| ms2
    master -->|"policy / job control"| ms3

    ms1 --> msdp1
    ms2 --> msdp2
    ms3 --> cloud

    vmHost -->|"TCP 13724 bpcd"| ms1
    dbHost -->|"TCP 13724 bpcd"| ms1
    nasHost -->|"NDMP"| ms1

    msdp1 -->|"AIR image replication"| msdp2

    classDef masterNode fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef mediaNode fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef storageNode fill:#b45309,stroke:#92400e,color:#fff
    classDef clientNode fill:#15803d,stroke:#166534,color:#fff
    class master masterNode
    class ms1,ms2,ms3 mediaNode
    class msdp1,msdp2,cloud storageNode
    class vmHost,dbHost,nasHost clientNode
```

## Data Flow

```
Client (backup agent) → TCP 13782
    │
    ▼
Media Server (reads client data, deduplicates if OST, writes to storage unit)
    │
    ├── AdvancedDisk/BasicDisk (local disk storage units)
    ├── OpenStorage (Data Domain OST)
    └── Cloud Storage Unit (S3, Azure Blob)
    │
Master Server (catalogs image metadata, orchestrates scheduling)
```

## Key Ports

| Port | Protocol | Purpose |
|---|---|---|
| 1556 | TCP | vnetd (BPRD) — main communication |
| 13724 | TCP | bpcd — client daemon |
| 13782 | TCP | bpbrm — backup/restore manager |
| 13785 | TCP | bpdbm — database manager (master) |

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
