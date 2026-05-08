# NetBackup CLI Reference

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

NetBackup CLI commands run on the Primary Server as root (Linux) or Administrator (Windows). The `bp*` family covers backup and restore operations; `nb*` and `tp*` commands cover EMM, media, and device management. Commands are in `/usr/openv/netbackup/bin/admincmd/` on Linux or `C:\Program Files\Veritas\NetBackup\bin\admincmd\` on Windows.
---

## Job Monitoring

Monitor backup and restore jobs in real time or review recent history.

```bash
# High-level job summary
bpjobs -summary

# List all active jobs
bpjobs

# Query job database — failed jobs in last 24 hours
bpdbjobs -report -failed -hoursago 24

# Query job database — all jobs with verbose output
bpdbjobs -report -all_columns -hoursago 48

# Kill a running job
bpdbjobs -cancel -jobid <id>

# Check NetBackup processes
bpps -a
```

---

## Backup Operations

Initiate manual backups and inspect policy configuration.

```bash
# Initiate manual backup for a policy/schedule/client
bpbackup -p <policy> -s <schedule> -c <client>

# List all policies
bppllist -allpolicies -L

# List file list for a policy
bpplinclude -L -p <policy>

# List schedules for a policy
bpplschedrep <policy>

# List clients assigned to a policy
bpplclients <policy>
```

---

## Restore Operations

### Catalog Restore Sequence

When the catalog is lost, recovery must happen before any other restore is possible.

```mermaid
sequenceDiagram
    participant Admin
    participant Master as Primary Server
    participant Catalog as Catalog Backup (offline copy)
    participant Media as Media Server

    Admin->>Master: Install / reinstall NetBackup\n(matching version)
    Admin->>Master: Run bprecover or\nbpcatarc -r (recover from catalog backup)
    Master->>Catalog: Locate catalog backup\n(separate STU or cold copy)
    Catalog-->>Master: Catalog images transferred
    Master->>Master: Rebuild EMM database\nnbemmcmd -machinealias
    Master->>Media: Reconnect media servers\nbpclntcmd -hn <media> -chk
    Media-->>Master: Media servers re-registered
    Admin->>Master: Run bpdbjobs -summary\nverify catalog integrity
    Admin->>Master: Resume backup policies\nbpbackup -p <policy>
    note over Admin,Media: Catalog recovery enables\nall image restores to resume
```

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
