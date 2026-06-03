# Commvault Backup and Restore — Procedures

```bash
curl -s -X POST "https://commserve.example.com/webconsole/api/Login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' | jq '.token'
```

```text
┌────────────────────────────── Commvault Backup and Restore — Procedures ──────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Backup Job Types               │  │                Restore Types                │   │
│   │      Full: all data in subclient scope       │  │      In-place: restore to original path     │   │
│   │       Incremental: changed since last        │  │     Out-of-place: alternate path/client     │   │
│   │       Differential: changed since Full       │  │     Cross-client: different target host     │   │
│   │     Synthetic Full: built on MA from inc     │  │    Granular: item-level from VM/Exchange    │   │
│   │     Snap backup: array snapshot + backup     │  │     Live Browse: mount backup for reads     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Full backup cycle: Full (weekly) → Incrementals (daily) → Synthetic Full (next week)               │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               On-Demand Backup (Command Center)                               │   │
│   │              1. Navigate: Protect → Virtualization (or File Servers / Databases)              │   │
│   │            2. Select subclient → right-click → Backup Now → choose Full/Incremental           │   │
│   │             3. Monitor job in Job Activity pane; check logs if status ≠ Completed             │   │
│   │                4. Verify protected size and dedup savings in job summary report               │   │
│   │            5. CLI: qoperation execschedule -clientName HOST -subclientName default            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Restore: right-click subclient → Browse and Restore → select files → Restore                       │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Restore Verification                                     │   │
│   │         After restore: verify file checksums, check application startup, validate data        │   │
│   │            VM restore: power on, run OS checks, verify application services running           │   │
│   │            DB restore: validate row counts, run DBCC CHECKDB (SQL) or RMAN validate           │   │
│   │           Scheduled restore tests: monthly verified restore to isolated environment           │   │
│   │           SLA reporting: track %backup success; target ≥ 99% weekly completion rate           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Restore target must have iDA agent; network path from MA to target must be open                      │
│  VM restores: target datastore must have sufficient free space (source VM size + 20%)                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Synthetic Full = Full backup constructed on MA from existing incrementals; no client I/O             │
│  Snap Backup    = IntelliSnap array-level snapshot followed by backup-from-snap to library            │
│  Live Browse    = Mount backup copy as NFS/CIFS share for direct file browsing                        │
│  Granular Recov = Item-level restore (e.g., single email, SQL row, VM disk file)                      │
│  DBCC CHECKDB   = SQL Server command to verify database consistency after restore                     │
│  Browse Window  = Time range visible in CommCell browse based on retention settings                   │
│  Cross-client   = Restore to a different machine than the original backup source                      │
│  Job Activity   = Real-time view of all running, queued, and recently completed jobs                  │
│  Protected Size = Total data covered by backup policy on a given client/subclient                     │
│  qoperation     = CLI to trigger on-demand backup: execschedule or backup subcommand                  │
│  SLA Report     = Commvault report showing backup success rate vs configured targets                  │
│  Retention Copy = Backup copy kept for extended period (monthly/yearly) on tape/cloud                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
Subclient → Restore → In-Place → Overwrite existing data: Yes
```
```text
Subclient → Restore → Out-of-Place → Specify destination client and path
```
```bash
qoperation execscript -sn QS_ValidateCopy -si "StoragePolicyName" -si "CopyName"
```
```mermaid
flowchart TD
    A([Recovery Request]) --> B{What needs recovery?}
    B --> C[Entire VM]
    B --> D[Specific files/folders]
    B --> E[Application data\nExchange / SQL / AD]

    C --> F{Target location?}
    F --> G[Original location\nIn-Place Restore]
    F --> H[Alternate host/DS\nOut-of-Place Restore]

    D --> I{Source accessible?}
    I --> |Yes - live agent| J[File-Level Recovery\nvia live browse]
    I --> |No - offline VM| K[Mount backup as\nvirtual volume\nthen browse]

    E --> L{Application type?}
    L --> M[Exchange → Mailbox\nor Item Restore]
    L --> N[SQL → DB Restore\nor Table-level]
    L --> O[AD → Authoritative\nor Non-authoritative]

    G --> P[Validate services post-restore]
    H --> P
    J --> P
    K --> P
    M --> P
    N --> P
    O --> P

    P --> Q{Validation passed?}
    Q --> |Yes| R([Recovery Complete])
    Q --> |No| S[Escalate /\nRestore alternate point]
```
