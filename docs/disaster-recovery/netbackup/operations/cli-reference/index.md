# NetBackup CLI Reference


<div class="kb-summary">
NetBackup CLI Reference reference covering Master → Media → Client Topology, Restore Operations, Catalog & Media, Client & Policy Management, Error & Log Analysis.
</div>

## Master → Media → Client Topology

Understanding the three-tier topology is essential before using the CLI — commands execute at the correct tier.

```mermaid
flowchart TD
    subgraph masterTier [Primary / Master Server]
        master["Primary Server\n(catalog, policy DB,\njob scheduler, EMM)"]
        catalog[("NetBackup Catalog\nbpdbm — image metadata")]
        master --> catalog
    end

    subgraph mediaTier [Media Servers]
        ms1["Media Server 1\nSite A — OST/Data Domain"]
        ms2["Media Server 2\nSite B / DR — MSDP pool"]
        ms3["Media Server 3\nCloud gateway — S3"]
    end

    subgraph clientTier [Clients]
        vmHost(["VMware backup host\nVADP proxy"])
        dbHost(["Oracle / MSSQL host\nbpcd agent"])
        nasHost(["NAS — NDMP\ndirect connect"])
    end

    subgraph storageTier [Storage Units]
        dd[("Data Domain\nOST dedup pool")]
        msdp[("MSDP\nMedia Server\nDedup Pool")]
        s3[("AWS S3 / Cloud\nlong-term archive")]
    end

    master -->|"policy / job control\nTCP 1556"| ms1
    master -->|"policy / job control"| ms2
    master -->|"policy / job control"| ms3

    ms1 --> dd
    ms2 --> msdp
    ms3 --> s3

    vmHost -->|"TCP 13724 bpcd"| ms1
    dbHost -->|"TCP 13724 bpcd"| ms1
    nasHost -->|"NDMP port 10000"| ms1

    classDef master fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef media fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef client fill:#15803d,stroke:#166534,color:#fff
    classDef storage fill:#b45309,stroke:#92400e,color:#fff
    class master,catalog master
    class ms1,ms2,ms3 media
    class vmHost,dbHost,nasHost client
    class dd,msdp,s3 storage
```
```
┌────────────────────────────────────── NetBackup — CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 NetBackup — Command Reference                                 │   │
│   │           Use these commands for routine operations, scripting, and troubleshooting           │   │
│   │                                       bpbackup / bprestore                                    │   │
│   │                                        bplist / bpdbjobs                                      │   │
│   │                                         nbpemreq / bpps                                       │   │
│   │                                       tpconfig / nbstlutil                                    │   │
│   │                                     bpexpdate / bpimmediate                                   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)                                                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Command Categories                                      │   │
│   │                  Status / Query  — check current state, list jobs, show config                │   │
│   │                  Operations      — start, stop, failover, restore, sync, expire               │   │
│   │                Configuration   — add/modify policies, schedules, storage targets              │   │
│   │               Diagnostics     — collect logs, run health checks, test connectivity            │   │
│   │                  Scripting       — REST API or CLI for automation and reporting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection             │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Server = central controller: scheduler, catalog, job manager, policy engine                   │
│  Media Server  = data mover between client and storage; can be co-located with master                 │
│  MSDP          = Media Server Deduplication Pool; inline variable-length block dedup                  │
│  Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot                    │
│  Policy        = defines what, when, and where to back up; contains schedules and clients             │
│  Schedule      = full / differential-incremental / cumulative-incremental timing within policy        │
│  Retention     = how long an image is kept; set per schedule, enforced by catalog expiry              │
│  Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config             │
│  NBU CA        = auto-issued certificate authority; signs host IDs for secure comms                   │
│  vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556           │
│  bpdbjobs      = CLI to query job history: status, duration, exit code, errors                        │
│  bplist        = CLI to list available backup images for a client, policy, or date range              │
│  KMS           = Key Management Service for encryption keys used in backup data encryption            │
│  NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

Run restores from the CLI. Always verify client name, backup time, and policy before executing.

```bash
# Restore files for a client
bprestore -C <client> -t <policy_type> -L /tmp/restore.log <file_path>

# List available restore points (backup images)
bpimmedia -U -client <client>

# Browse backups for a client
bplist -C <client> -t <type> -R /

# Initiate instant access restore
bprestore -L /tmp/restore.log -R -C <client> <path>
```

---

## Catalog & Media

Manage media, catalog verification, and storage unit health.

```bash
# List all storage units
bpstulist

# List storage unit detail
bpstulist -label <stu_name>

# List media volumes
vmquery -b -m <media_id>

# List all tape drives
tpconfig -d

# Run catalog backup
bpcatarc

# Verify catalog integrity
bpdbm -consistency_check
```

---

## Client & Policy Management

Inspect and manage client records and policy assignments.

```bash
# List all clients
bpclient -L

# Show detail for a specific client
bpclient -L -client <name>

# Test BPCD connectivity to a client
bptestbpcd -client <host>

# Test client backup connectivity
bptestnetconn -sv -client <host>

# List media servers
nbemmcmd -listhosts -machinetype mediaserver
```

---

## Error & Log Analysis

Decode errors and review logs.

```bash
# Show backup errors from last 24 hours
bperror -backstat -hoursago 24

# Look up an error code
bperror -S <exit_status>

# View unified logs (unilog format)
vxlogview -i 51216 -d 24:00:00

# Tail legacy job logs
tail -f /usr/openv/netbackup/logs/bprd/log.<today>
```
