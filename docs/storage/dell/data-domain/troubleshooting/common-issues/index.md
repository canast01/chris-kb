---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Dell Data Domain Common Issues

```bash
replication disable <context>
replication enable <context>
```
```text
┌─────────────────────────────────── Dell Data Domain Common Issues ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Top issues: filesystem full, replication broken, restore slow, backup job failures      │   │
│   │           Most root-cause to space exhaustion, network issues, or credential expiry           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Space Issues        │  │      Replication Issues     │  │        Backup/Restore       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        FS > 80% full        │  │        Context broken       │  │         Backup fails        │   │
│   │       Cleaning not run      │  │        Lag > 4 hours        │  │         Restore slow        │   │
│   │       MTree quota hit       │  │         Auth failure        │  │       Cannot mount NFS      │   │
│   │       No space for rep      │  │     Network packet drop     │  │       Boost conn fail       │   │
│   │       Cloud tier fail       │  │        WAN bandwidth        │  │        Corrupt backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     Problem      │   First check    │        Fix        │      Verify      │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     FS full      │filesys show space│   Expire backups  │   Space freed    │  No space freed  │   │
│   │    Rep broken    │ replication show │   resync context  │    Lag drops     │ Persistent break │   │
│   │   Backup fail    │ Backup app logs  │   Check DD space  │   Job succeeds   │  Hardware fault  │   │
│   │   Slow restore   │ Disk show state  │    Check disks    │     Speed OK     │   NVRAM fault    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Context broken   = Replication context in error state; typically network or auth failure           │
│    replication resync= Re-establish broken replication context without full reinitialisation          │
│    Expire backups   = Delete old backup images via backup application; cleaning then frees space      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?])
    S --> B1{Deduplication\nratio dropped?}
    S --> B2{CIFS or NFS share\ninaccessible?}
    S --> B3{Replication\nbehind schedule?}
    S --> B4{Cleaning job\nstalled?}
    S --> B5{Disk fault in\nRAID group?}

    B1 -->|Check DRR in GUI| D1{New data type\npre-compressed?}
    D1 -->|Yes| R1[See Space Issues —\nData type incompatible with dedup: review policy]
    D1 -->|Space low| R2[See Space Issues —\nFS above 80%: expire backups then clean]

    B2 -->|Check filesystem and share| D2{Filesystem\nmounted?}
    D2 -->|No| R3[See Space Issues —\nMTree quota hit or FS full]
    D2 -->|Auth failure| R4[See Backup/Restore —\nCIFS/NFS mount auth or credential issue]

    B3 -->|Check replication context| D3{Context in\nerror state?}
    D3 -->|Yes| R5[See Replication Issues —\nContext broken: resync context]
    D3 -->|WAN lag| R6[See Replication Issues —\nLag over 4 hours: check WAN bandwidth]

    B4 -->|Check cleaning status| D4{Cleaning\nrunning?}
    D4 -->|Stalled| R7[See Space Issues —\nCleaning not run: restart cleaning job]
    D4 -->|No space| R8[See Space Issues —\nNo space for replication: expire and clean]

    B5 -->|Check disk state in GUI| D5{RAID group\ndegraded?}
    D5 -->|Drive failed| R9[See Problem Table —\nDisk fault: check disks and open Dell case]
    D5 -->|Slow restore| R10[See Backup/Restore —\nRestore slow: check disk and NVRAM health]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9,R10 section
    class B1,B2,B3,B4,B5,D1,D2,D3,D4,D5 decision
    class S start
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
