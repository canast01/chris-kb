# Commvault — Components

## Core Components

| Component | Role | Notes |
|---|---|---|
| CommServe | Management, scheduling, SQL DB | HA pair (passive standby) for critical environments |
| MediaAgent | Data movement, deduplication (DDB) | Multiple; one DDB per storage pool |
| Client | Backup agent (Windows, Linux, VSA) | VSA agent for VMware vSphere |
| Command Center | Web UI for administration | Replaces legacy Java GUI in FR32+ |
| Storage Policy | Job-to-storage mapping | Primary copy + secondary (offsite) copy |

## CommServe

The CommServe is the single most critical component — it holds the configuration database (SQL Server) that maps every backup job, client, and storage policy. CommServe failure means no new jobs run.

High availability options:
- **Passive standby**: Second CommServe instance with SQL log shipping; manual failover
- **CommServe Failover (active/passive HA)**: Automated failover via CommServe HA option

CommServe SQL backup should run every 4 hours:
```powershell
# Verify CommServe DB backup job status
qlist job -j CommServeDB_Backup -detail
```

## MediaAgent and Deduplication

### Deduplication Data Path

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

MediaAgents perform data movement and host the Deduplication Database (DDB):

```
MediaAgent placement best practices:
  - Deploy one MediaAgent per site for local backups
  - Place DDB on SSD-backed storage — IOPS are critical for large dedup pools
  - DDB free space: maintain ≥ 20% free at all times
  - Single DDB should not manage more than 60TB of deduped data
```

Monitor DDB health via Command Center: Storage → Disk Libraries → DDB Status

## Storage Library Types

| Type | Use Case | Notes |
|---|---|---|
| Disk Library (Dedup) | Primary backup target | SSD recommended for DDB |
| Cloud Library (S3) | Long-term retention | AWS S3, Azure Blob, GCP |
| Tape Library | Offsite/archival | Via SAN-attached or NDMP |
| Hyperscale X | Integrated scale-out | CommVault managed hardware |
