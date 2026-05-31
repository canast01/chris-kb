# NetBackup Standards

```text
┌──────────────────────────────────── NetBackup — Design Standards ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Sizing Guidelines               │  │               HA Requirements               │   │
│   │         Deduplicate where supported          │  │           N+1 component redundancy          │   │
│   │          Bandwidth: 10 GbE minimum           │  │          Heartbeat / health monitor         │   │
│   │          Storage: 130% of raw data           │  │          Separate mgmt / data VLANs         │   │
│   │         Latency: < 10 ms to storage          │  │          Out-of-band access (IPMI)          │   │
│   │           CPU: 8+ vCPU for engine            │  │          Anti-affinity VM placement         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)                                                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Standard NetBackup Design Rules                                │   │
│   │            RPO target drives snapshot/cycle frequency — document in service design            │   │
│   │            RTO target drives recovery tier: instant, warm standby, or cold restore            │   │
│   │                  Dedicated backup network VLAN — no shared production traffic                 │   │
│   │      Encryption: AES-256 backup encryption; KMS key management; TLS 1.2+ on all channels      │   │
│   │               Service accounts: minimum privilege; rotate credentials quarterly               │   │
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
