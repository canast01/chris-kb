---
tags:
  - netbackup
  - troubleshooting
search:
  boost: 1.5
---
# NetBackup — Common Issues

```bash
# Check bpcd is running on the client
bpps -a | grep bpcd

# Test connectivity from master to client on NetBackup port
telnet <client-hostname> 13782

# Review bpcd log on client
tail -200 /usr/openv/netbackup/logs/bpcd/log.<yyyymmdd>

# Review bpbrm log on master
tail -200 /usr/openv/netbackup/logs/bpbrm/log.<yyyymmdd>
```
```text
┌────────────────────────────────────── NetBackup — Common Issues ──────────────────────────────────────┐
│                                                                                                       │
│   │     Symptom      │   Likely Cause   │    First Check    │       Fix        │      Verify      │   │
│   │    Status 96     │client not respon │ ping + bpps on cl │ restart nbclient │     bpps -x      │   │
│   │   Status 2106    │  MSDP pool full  │ bpexpdate / nbstl │ expand or expire │  nbstlutil list  │   │
│   │    Status 58     │media write error │ check disk/tape h │ new storage unit │   tpconfig -d    │   │
│   │    Status 84     │media manager dow │ check ltid proces │   restart ltid   │     vmquery      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     General Triage Pattern                                    │   │
│   │          Is the issue new or recurring? New = recent change; Recurring = config problem       │   │
│   │             Is it isolated to one source or all? Isolated = agent; All = server/repo          │   │
│   │                                Check logs first: nbpemreq / bpps                              │   │
│   │                    If unresolved in 2h: open vendor case with full log bundle                 │   │
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
```bash
# Check catalog backup job history
bplist -S <master-server> -policy NBU_Catalog -Listdead -d 01/01/1970 00:00:00

# Force an immediate catalog backup
bpbackup -p NBU_Catalog_Backup

# Check catalog database consistency
bpdbm -consistency -verbose
```
```bash
# Check all STU free space
bpstulist -U

# Check disk pool usage (MSDP / AdvancedDisk)
nbdevquery -listdp -stype PureDisk -U

# Expire old images to reclaim space
bpexpdate -policy <policyname> -d 0 -backupid <backup-id>

# Run image cleanup to actually reclaim the space
bpimage -cleanup
```
```bash
# Check MSDP pool status
cacontrol --dsstat -d <msdp-path>

# Check fingerprint database health
cacontrol --dbstat

# Review dedupe log for anomalies
tail -500 /usr/openv/netbackup/logs/spoold/log.<yyyymmdd>
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A[Status 25 — client connect refused]
    S --> B[Media manager volume busy]
    S --> C[Catalog backup failed]
    S --> D[Policy class mismatch]
    S --> E[Master / media server connectivity loss]
    A --> A1{bpcd running on client?}
    A1 -->|No| A2[Start bpcd and verify port 13782 open — see Before you begin]
    A1 -->|Yes| A3[Check bpbrm and bpcd logs for TLS or host ID error]
    B --> B1{Tape library online?}
    B1 -->|No| B2[Check ltid process and tpconfig -d — see Before you begin]
    B1 -->|Yes| B3[Check for volume in use by another job; wait or cancel conflicting job]
    C --> C1{Storage unit accessible?}
    C1 -->|No| C2[Check MSDP pool and STU free space — see Before you begin]
    C1 -->|Yes| C3[Run bpdbm -consistency and force catalog backup with bpbackup]
    D --> D1{Client OS matches policy type?}
    D1 -->|No| D2[Correct policy type in NetBackup console to match client OS]
    D1 -->|Yes| D3[Check schedule type and retention level for the policy]
    E --> E1{vnetd reachable on port 1556?}
    E1 -->|No| E2[Restart NetBackup services on master and check firewall rules]
    E1 -->|Yes| E3[Check NBU CA host ID certificate validity on media server]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A,B,C,D,E,A2,A3,B2,B3,C2,C3,D2,D3,E2,E3 section
    class A1,B1,C1,D1,E1 decision
    class S start
```

---

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
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

---

## See also

- [Netbackup — Diagnostics](../diagnostics/)
- [Netbackup — Escalation](../escalation/)
- [Netbackup — Health Checks](../../operations/health-checks/)
