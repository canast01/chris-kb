# Commvault — How It Works

## Overview

Commvault provides enterprise backup, recovery, replication, archive, and data protection management. The CommServe is the single command-and-control server — it holds the configuration database (SQL Server) mapping every backup job, client, and storage policy. MediaAgents perform data movement and host the Deduplication Database (DDB). Clients are the protected hosts (VMs, databases, filesystems).

## Component Topology

```mermaid
graph TB
  CS["CommServe\n(command & control)"] --> WEBCON["Web Console\n& Command Center"]
  MA1["Media Agent 1\n(data mover)"] & MA2["Media Agent 2"] --> CS
  SRC(["Source — VMs / DBs / Files"]) --> MA1 & MA2
  MA1 & MA2 --> DISK[("Disk Library\nDDB dedup")]
  DISK -->|"aux copy"| TAPE[("Tape / Object\nlong-term retention")]
  ADMIN(["Backup Admin"]) --> WEBCON
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class CS,MA1,MA2 ctrl
  class DISK,TAPE store
  class SRC,ADMIN host
  class WEBCON mgmt
```

## Components

| Component | Role | Notes |
|---|---|---|
| CommServe | Management, scheduling, SQL DB | HA pair (passive standby) for critical environments |
| MediaAgent | Data movement, deduplication (DDB) | Multiple; one DDB per storage pool |
| Client | Backup agent (Windows, Linux, VSA) | VSA agent for VMware vSphere |
| Command Center | Web UI for administration | Replaces legacy Java GUI in FR32+ |
| Storage Policy | Job-to-storage mapping | Primary copy + secondary (offsite) copy |

## CommServe High Availability

- **Passive standby**: Second CommServe instance with SQL log shipping; manual failover
- **CommServe Failover (active/passive HA)**: Automated failover via CommServe HA option

```powershell
# Verify CommServe DB backup job status
qlist job -j CommServeDB_Backup -detail
```

## MediaAgent and Deduplication

```mermaid
flowchart LR
    client(["Client Agent\n(VM / DB / File)"])
    client -->|"raw data stream\nTCP 8403"| ma["MediaAgent"]

    subgraph maBlock [MediaAgent Processing]
        direction TB
        chunk["Chunk data into\nvariable blocks"]
        hash["Hash each block\n(SHA-256)"]
        ddb[("DDB\nDeduplication DB\nSSD-backed")]
        chunk --> hash
        hash -->|"block seen before?"| ddb
    end

    ma --> maBlock

    ddb -->|"New block\nwrite to library"| diskLib[("Disk Library\nPrimary copy")]
    ddb -->|"Duplicate block\nskip write"| dedupSave["Dedup saving\n(reference only)"]

    diskLib -->|"Aux copy"| secondary[("Secondary copy\nOffsite / Cloud / Tape")]

    classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef host fill:#15803d,stroke:#166534,color:#fff
    class ma,chunk,hash ctrl
    class ddb,diskLib,secondary store
    class client host
```

MediaAgent best practices:
- Deploy one MediaAgent per site for local backups
- Place DDB on SSD-backed storage — IOPS are critical for large dedup pools
- DDB free space: maintain ≥ 20% free at all times
- Single DDB should not manage more than 60 TB of deduped data

## Storage Library Types

| Type | Use Case | Notes |
|---|---|---|
| Disk Library (Dedup) | Primary backup target | SSD recommended for DDB |
| Cloud Library (S3) | Long-term retention | AWS S3, Azure Blob, GCP |
| Tape Library | Offsite/archival | Via SAN-attached or NDMP |
| Hyperscale X | Integrated scale-out | CommVault managed hardware; minimum 3-node cluster |

## Port Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Clients | CommServe | 8400 | Job requests |
| Clients | MediaAgent | 8403 | Data movement |
| CommServe | MediaAgent | 8400 | Job orchestration |
| Browser (admin) | Command Center | 443 | Web UI |

## Multi-Site Topology

```mermaid
flowchart TD
    subgraph primarySite [Primary Site]
        cs["CommServe\n(command & control)"]
        ma1["MediaAgent\ndc1-ma-01"]
        diskLib1[("Disk Library\nDDB — Primary")]
        clients1(["VMs / DBs / Files\nSite A"])
        clients1 --> ma1
        ma1 --> diskLib1
        ma1 --> cs
    end

    subgraph drSite [DR / Secondary Site]
        ma2["MediaAgent\ndc2-ma-01"]
        diskLib2[("Disk Library\nDDB — DR copy")]
        clients2(["VMs / DBs / Files\nSite B"])
        clients2 --> ma2
        ma2 --> diskLib2
        ma2 --> cs
    end

    subgraph cloudTier [Cloud / Tape Tier]
        cloud[("Cloud Library\nS3 / Azure Blob\nlong-term retention")]
        tape[("Tape Library\narchival / compliance")]
    end

    diskLib1 -->|"aux copy\n(scheduled)"| diskLib2
    diskLib2 -->|"aux copy\n(scheduled)"| cloud
    diskLib1 -->|"aux copy"| tape
    cs --> webUI["Command Center\nWeb UI — port 443"]

    classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef host fill:#15803d,stroke:#166534,color:#fff
    classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
    class cs,ma1,ma2 ctrl
    class diskLib1,diskLib2,tape store
    class clients1,clients2 host
    class cloud,webUI cloud
```
