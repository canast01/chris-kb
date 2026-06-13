---
tags:
  - netbackup
  - security
---
# NetBackup — Access Control


<div class="kb-summary">
Access Control reference covering NetBackup Access Control (NBAC).
</div>

```text
┌───────────────────────────────────── NetBackup — Access Control ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              NetBackup — RBAC and Access Control                              │   │
│   │            Auth: NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles            │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
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
