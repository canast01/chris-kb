# Commvault — Standards

```text
┌────────────────────────── Commvault Design Standards — Sizing and Topology ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Design Principles                                       │   │
│   │                 Separate CommServe and MediaAgent roles onto dedicated servers                │   │
│   │         Place MediaAgents close to data sources (same site/rack) to reduce WAN traffic        │   │
│   │         Size DDB on fast local NVMe: 1 GB DDB per 1 TB source data (post-dedup ratio)         │   │
│   │           Minimum 2 MA per site for redundancy; use MA groups for automatic failover          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Component sizing drives performance; under-sized MA is the most common bottleneck                  │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               CommServe Sizing               │  │              MediaAgent Sizing              │   │
│   │          CPU: 8-16 vCPU (SQL-heavy)          │  │        CPU: 16-32 vCPU for throughput       │   │
│   │      RAM: 32-64 GB for large CommCells       │  │          RAM: 16-32 GB + DDB cache          │   │
│   │          SQL: NVMe RAID-10 for CSDB          │  │       DDB: NVMe SSD, separate from OS       │   │
│   │       NIC: 10 GbE for GUI/CLI traffic        │  │         NIC: 25 GbE for data streams        │   │
│   │         OS: Windows Server 2019/2022         │  │         OS: Windows or Linux (RHEL)         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Storage policy design directly impacts restore time and dedup efficiency                           │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Storage Design    │       Retention       │        Network        │        HA / DR        │   │
│   │   Primary: fast disk  │     Daily: 30 days    │      Backup VLAN      │      DR CommServe     │   │
│   │ Secondary: tape/cloud │    Weekly: 12 weeks   │     10/25 GbE NIC     │    SQL log shipping   │   │
│   │  Dedup ratio 5:1-20:1 │   Monthly: 12 months  │     QoS throttling    │    CommCell DR site   │   │
│   │  WORM for compliance  │     Yearly archive    │     Firewall proxy    │      RPO < 1 hour     │   │
│   │  Cloud tier: S3/Blob  │    Legal hold caps    │    Bandwidth limits   │     RTO < 4 hours     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CommServe: physical server preferred; avoid shared VMs for production CommCells                      │
│  DDB drives: enterprise NVMe (Samsung PM9A3 / Intel P4510); avoid SAS/SATA for DDB                    │
│  Backup network: dedicated 10/25 GbE switch; separate from production VLAN                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CommCell DR    = Passive CommServe replica at secondary site for CS failover                         │
│  DDB Resync     = Process to rebuild DDB fingerprint index from library chunks                        │
│  Storage Policy = Container linking subclients to libraries with retention and copy rules             │
│  Dedup Ratio    = Ratio of source data size to post-dedup storage consumed                            │
│  MA Group       = Named pool of MediaAgents for load balancing and failover                           │
│  Primary Copy   = First storage policy copy; used for fast restores                                   │
│  Secondary Copy = Aux-copy destination (tape or cloud) for long-term retention                        │
│  WORM           = Write Once Read Many; immutable storage for compliance locks                        │
│  RPO            = Recovery Point Objective; max acceptable data loss (time since last backup)         │
│  RTO            = Recovery Time Objective; max acceptable time to complete restore                    │
│  Bandwidth Cap  = Throttle on MA data transfer rate to protect production network                     │
│  SQL Log Ship   = SQL Server log shipping replicating CSDB to DR CommServe                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Storage Policy | `<app>-<retention>-<tier>` | `oracle-7yr-primary`, `vm-90d-secondary` |
| Subclient | `<app>-<env>-<host>-<type>` | `oracle-prod-db01-full` |
| Client Group | `<env>-<os>-<tier>` | `prod-linux-db`, `dev-windows-app` |
| Schedule Policy | `<frequency>-<retention>` | `daily-14d`, `weekly-8w` |
| MediaAgent | `<site>-ma-<seq>` | `dc1-ma-01`, `dc2-ma-01` |

## Retention Schedule

| Level | Copy | Retention |
|---|---|---|
| Daily | Primary (disk/dedup) | 14 days |
| Weekly | Primary (disk/dedup) | 8 weeks |
| Monthly | Secondary (offsite or cloud) | 12 months |
| Yearly | Secondary (tape or cloud archive) | 7 years |

Configure via SLA Plans in Command Center (preferred for FR32+) or directly in Storage Policy (legacy).

### Capacity Planning Flow



## VMware vSphere Standards

| Setting | Value |
|---|---|
| Backup proxy type | Hot-add (SAN or VDDK) preferred over NBD |
| Number of proxies | Minimum 2 per site for redundancy |
| VMware concurrent tasks per proxy | Maximum 4 (adjust per MediaAgent CPU) |
| VSA subclient granularity | Per-datastore or per-folder; never entire vCenter in one subclient |
| Application-aware backup | Enabled for SQL Server, Oracle, Exchange VMs |

## Encryption Standard

| Data Classification | Encryption Required | Algorithm |
|---|---|---|
| PII / Regulated | Yes — mandatory | AES-256, MediaAgent-side minimum |
| Business-sensitive | Yes — recommended | AES-256 |
| Internal non-sensitive | Optional | Per policy decision |

- Encryption keys: exported and stored in CyberArk or offline secure vault
- Loss of key = loss of backup data — key management is as critical as backup data itself
