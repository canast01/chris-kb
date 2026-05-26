# NetBackup — How It Works

## Overview

NetBackup operates on a three-tier architecture: a centralized Primary Server (formerly Master Server) coordinates all operations via policy scheduling, catalog management, and resource arbitration. Media Servers handle data movement — reading from clients and writing to storage units. The Catalog is the operational heartbeat of the entire deployment, storing all image metadata, policies, and media inventory.

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

Store the DR file off-host (NAS/object storage) and the passphrase in a secure vault — both are required for catalog recovery.

## Domain Sizing Guidelines

| Environment Scale | Primary Server vCPU | RAM | Catalog Disk |
|---|---|---|---|
| Small (<500 clients) | 8 vCPU | 32 GB | 500 GB |
| Medium (500–2000 clients) | 16 vCPU | 64 GB | 2 TB |
| Large (>2000 clients) | 32 vCPU | 128 GB | 5–10 TB |

Catalog disk should be on SSD/NVMe — IOPS under load are significantly higher than sequential throughput figures suggest.
