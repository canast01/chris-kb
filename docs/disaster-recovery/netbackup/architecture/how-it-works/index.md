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

## Key Ports

| Port | Protocol | Purpose |
|---|---|---|
| 1556 | TCP | vnetd (BPRD) — main communication |
| 13724 | TCP | bpcd — client daemon |
| 13782 | TCP | bpbrm — backup/restore manager |
| 13785 | TCP | bpdbm — database manager (master) |

## Components

| Component | Role | Key Processes |
|---|---|---|
| Primary Server | Policy scheduling, catalog management, resource arbitration | `nbpem`, `nbproxy`, `nbwebsvc`, `nbrb` |
| Media Server | Data mover — reads/writes backup streams | `bpbrm`, `bptm`, `bpdm` |
| Client | Source of backup data, hosts the backup agent | `bpcd`, `bpbkar` |
| Catalog | Internal DB of policies, images, and media inventory | `nbdb2`, `nbdbms_start_stop` |
| Storage Unit | Logical pointer to physical/virtual storage | Configured on Media Server |

## Storage Unit Types

| Type | Description |
|---|---|
| BasicDisk | Local or NAS filesystem path |
| AdvancedDisk | NetBackup-managed disk volume |
| MSDP | Media Server Deduplication Pool |
| Cloud | Cloud Catalyst or direct cloud (S3/Azure/GCS) |
| Tape/Robot | Physical tape library managed by Media Server |

## Key Processes

| Process | Server | Function |
|---|---|---|
| `nbpem` | Primary | Policy Execution Manager — evaluates schedules and triggers jobs |
| `nbrb` | Primary | Resource Broker — allocates drives, media, and server slots |
| `nbwebsvc` | Primary | Hosts the REST API and Web UI backend |
| `bpbrm` | Media | Backup/Restore Manager — parent process coordinating a single job |
| `bptm` | Media | Tape Manager — manages tape drive I/O |
| `bpdm` | Media | Disk Manager — manages disk-based storage unit I/O |
| `spoold` | Media | MSDP deduplication storage server daemon |
| `bpcd` | Client | Client Daemon — accepts incoming connections from Primary/Media |
| `bpbkar` | Client | Backup Archiver — traverses filesystem and streams data |

## Catalog Backup

The NetBackup Catalog contains all image metadata. Without a valid catalog backup, media cannot be read.

```bash
# Trigger immediate catalog backup
/usr/openv/netbackup/bin/admincmd/bpbackupdb

# Verify catalog backup job in activity monitor
/usr/openv/netbackup/bin/admincmd/bpdbjobs -report -all_columns | grep -i catalog

# Catalog recovery (on rebuilt Primary Server)
/usr/openv/netbackup/bin/admincmd/bprecover -r -drc <path_to_disaster_recovery_file>
```

Store the DR file off-host (NAS/object storage) and the passphrase in a secure vault — both are required for catalog recovery.

## Domain Sizing Guidelines

| Environment Scale | Primary Server vCPU | RAM | Catalog Disk |
|---|---|---|---|
| Small (<500 clients) | 8 vCPU | 32 GB | 500 GB |
| Medium (500–2000 clients) | 16 vCPU | 64 GB | 2 TB |
| Large (>2000 clients) | 32 vCPU | 128 GB | 5–10 TB |

Catalog disk should be on SSD/NVMe — IOPS under load are significantly higher than sequential throughput figures suggest.
