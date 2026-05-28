# Veeam — Standards

```
┌────────────────────────────────────── Veeam — Design Standards ───────────────────────────────────────┐
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
│    Ports: 9419 (Veeam REST API) · 6160 (Veeam Agent) · 443 (vCenter)                                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Standard Veeam Design Rules                                  │   │
│   │            RPO target drives snapshot/cycle frequency — document in service design            │   │
│   │            RTO target drives recovery tier: instant, warm standby, or cold restore            │   │
│   │                  Dedicated backup network VLAN — no shared production traffic                 │   │
│   │    Encryption: AES-256 backup (key in Veeam DB); TLS on all management; WORM repo supported   │   │
│   │               Service accounts: minimum privilege; rotate credentials quarterly               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Backup Server = central Veeam component: scheduler, job engine, catalog, REST API                    │
│  Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H       │
│  CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors          │
│  VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup                 │
│  SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage        │
│  Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds                   │
│  SureBackup    = automated backup verification; test-restores VM in isolated virtual lab              │
│  Replication   = creates VM replica at DR site; enables failover without full restore time            │
│  GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points      │
│  Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec       │
│  Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery           │
│  VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required                    │
│  Health Check  = periodic backup integrity scan; verifies restore points are readable                 │
│  Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Job Naming Convention

| Object | Convention | Example |
|---|---|---|
| Backup job | `<env>-<workload>-<type>` | `prod-vm-daily`, `dr-fileserver-weekly` |
| Backup copy job | `<env>-<workload>-copy-<dest>` | `prod-vm-copy-offsite` |
| Replication job | `<env>-<workload>-repl` | `prod-critical-vm-repl` |
| SOBR | `<site>-sobr-<tier>` | `dc1-sobr-primary` |
| Repository | `<site>-repo-<type>-<seq>` | `dc1-repo-ssd-01`, `dc2-repo-linux-01` |

## Retention Schedule

| Level | Restore Points | Schedule | Repository |
|---|---|---|---|
| Daily | 14 | Incremental (synthetic full weekly) | Performance tier (fast disk) |
| Weekly | 8 | Synthetic full | Performance tier |
| Monthly | 12 | Active full (monthly) | SOBR capacity tier offload |
| Yearly | 7 | Active full (yearly) | Object storage archive |

SOBR capacity tier offload: configure automatic offload after 14 days → moves monthly/yearly points to object storage.

### Backup Job Types Comparison



## Backup Job Configuration Standards

- **Backup window**: 22:00–06:00 (default); set hard stop to prevent daytime impact
- **Source-side deduplication**: Enabled on all jobs (reduces WAN for copy jobs)
- **Compression**: Optimal (default) — do not use Extreme unless backup window permits extra CPU time
- **Application-aware processing**: Enabled for all jobs containing SQL Server, Oracle, Exchange, Active Directory VMs
- **Guest OS quiescence**: VSS quiescence for Windows VMs; file system freeze for Linux VMs

## Encryption Standard

Mandatory encryption for:
- All backup copy jobs targeting off-site repositories
- All cloud repository targets (SOBR capacity tier)
- Any job protecting VMs with classified or regulated data (PII, financial, healthcare)

Algorithm: AES-256.

**Key management**:
- Export encryption keys immediately after creation
- Store in CyberArk → dedicated VBR Encryption Keys safe
- Rotate keys annually — plan for re-encryption of existing backup files

## Proxy Standards

| Setting | Standard |
|---|---|
| Minimum proxies per site | 2 (redundancy + parallel capacity) |
| Transport mode preference | Hot-add (SAN) > Direct NFS > NBD |
| Max concurrent tasks per proxy | vCPU count / 2 (default) |
| Proxy OS | Windows Server 2022 or RHEL 8+ (Linux proxy) |

## Repository Standards

| Repository Type | Use Case | Performance Target |
|---|---|---|
| Linux hardened (immutable) | Primary onsite backup | XFS or ReFS; 10 GbE minimum |
| NFS/SMB share | Secondary onsite storage | Dedicated NAS volume; 10 GbE |
| S3-compatible (SOBR capacity) | Long-term / archival | Glacier-class for yearly; Standard for monthly |

## Sizing Guidelines

| Scale | Backup Server | Proxies per Site |
|---|---|---|
| < 100 VMs | 4 vCPU, 8 GB RAM | 1–2 |
| 100–500 VMs | 8 vCPU, 16 GB RAM | 2–4 |
| 500–2,000 VMs | 16 vCPU, 32 GB RAM (+ full SQL) | 4–8 |

## Instant VM Recovery RTO Targets

| Application Tier | Target RTO |
|---|---|
| Tier 1 (critical DB, ERP) | < 15 minutes via Instant VM Recovery |
| Tier 2 (business apps) | < 1 hour |
| Tier 3 (dev/test) | < 4 hours |

Document agreed RTOs in the DR plan; validate quarterly via Instant VM Recovery test.
