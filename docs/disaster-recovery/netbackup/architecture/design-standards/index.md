# NetBackup Standards

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Policy | `<app>-<os>-<frequency>` | `oracle-linux-daily`, `mssql-win-weekly` |
| Schedule | `<type>-<retention>` | `full-14d`, `incr-7d`, `weekly-8w` |
| Storage Unit | `<site>-<type>-<tier>` | `dc1-ostdd-primary`, `dc2-cloud-archive` |
| Media Server | `<site>-nbumedia-<seq>` | `dc1-nbumedia-01` |
| Client Group | `<env>-<os>-<tier>` | `prod-linux-db`, `prod-windows-app` |

## Retention Schedule

| Level | Schedule Type | Retention |
|---|---|---|
| Daily | Incremental | 14 days |
| Weekly | Full | 8 weeks |
| Monthly | Full | 12 months |
| Yearly | Full | 7 years |

Compliance requirements may extend yearly retention to 10 years for regulated data.

## Backup Policy to Job Flow

```mermaid
flowchart TD
    policy["Backup Policy\n(application type,\nclient list, schedules)"]
    policy --> schedule["Schedule\n(full-14d, incr-7d, weekly-8w)"]
    schedule --> trigger{Schedule\ntrigger}
    trigger -->|"Window opens"| jm["Job Manager\n(allocate media server + STU)"]
    jm --> clientConn["Connect to client\nbpcd TCP 13724"]
    clientConn --> dataStream["Stream data to media server\nbpbrm TCP 13782"]
    dataStream --> dedup{Storage\ntype?}
    dedup -->|"OST / Data Domain"| ddDedup["DD Boost\ninline dedup on media server"]
    dedup -->|"MSDP"| msdpDedup["MSDP\ndedup on media server"]
    dedup -->|"BasicDisk"| basicDisk["Write directly\nno dedup"]
    ddDedup --> catalog["Catalog image in\nNetBackup DB\nbpdbm"]
    msdpDedup --> catalog
    basicDisk --> catalog
    catalog --> done(["Job complete\nlog in bpdbjobs"])

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    classDef storage fill:#7c3aed,stroke:#6d28d9,color:#fff
    class jm,clientConn,dataStream,ddDedup,msdpDedup,basicDisk,catalog action
    class trigger,dedup decision
    class policy,schedule terminal
    class done terminal
```

## Policy Design Rules

- **Client list**: Always use an explicitly named client list — wildcard client patterns are not permitted in production
- **Granularity**: Separate policies per application type (Oracle, MSSQL, file system) — do not mix policy types
- **Application-aware**: Enable application-consistent backup for Oracle (ORA policy type), MSSQL, and Exchange
- **VMware**: Use tag-based or folder-based selection — never include entire vCenter as a single selection
- **Multiplexing**: Limit to 8 jobs per drive to avoid excessive fragmentation during restores

## Storage Unit Standards

| Parameter | Standard |
|---|---|
| Primary storage (OST/DD) | AdvancedDisk or OST on Data Domain; deduplicated |
| Cloud storage (long-term) | Cloud storage unit with S3-compatible target; Glacier-class after 90 days |
| Tape (archival) | LTO8/9 WORM for compliance workloads; separate tape pool per retention tier |
| Storage unit load balancing | Maximum concurrent jobs per storage unit = media server CPU core count / 2 |

## Catalog Backup Standard

The catalog is the most critical data in a NetBackup domain — protect it rigorously:

- Catalog backup must run every 4–6 hours (not just daily)
- Store catalog backup on a separate storage unit from standard backups
- Keep a cold copy of the most recent catalog backup off-site or on a separate server
- Verify catalog backup is successful before proceeding with any infrastructure change

```bash
# Check catalog backup status
bplist -S <master_server> -t 0 -policy NBU_Catalog -s -1d
```

## Encryption Standard

| Data Classification | Policy | Algorithm |
|---|---|---|
| PII / Regulated | Mandatory | AES-256 |
| Business-sensitive | Required | AES-256 |
| Internal | Optional | N/A |

Key management: store encryption key files in CyberArk or an offline vault. Loss of key = unrecoverable backup data.

## Test Restore Standard

| Restore Type | Frequency |
|---|---|
| File-level restore test (non-critical VM) | Monthly |
| Full VM restore test | Quarterly |
| Database restore test (Oracle/MSSQL) | Quarterly |
| Catalog recovery test | Annually |
