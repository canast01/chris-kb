# Veeam — Encryption

```
┌───────────────────────────────────────── Veeam — Encryption ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Veeam — Encryption Configuration                               │   │
│   │  AES-256 backup encryption (key stored in Veeam config DB); TLS on all management; WORM repos │   │
│   │              In-transit: TLS 1.2+ for all management; data channel also encrypted             │   │
│   │              At-rest: AES-256 on repository or vault storage; key managed by KMS              │   │
│   │               Key lifecycle: generate → use → rotate (annual) → retire → destroy              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  In-Transit                  │  │                   At-Rest                   │   │
│   │              TLS 1.2+ (minimum)              │  │              AES-256 encryption             │   │
│   │         9419 (Veeam REST API) HTTPS          │  │              KMS key management             │   │
│   │             Mutual TLS internal              │  │               WORM / immutable              │   │
│   │             Cert rotation annual             │  │             Key rotation annual             │   │
│   │             No plain-text admin              │  │               Audit key access              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
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
## Backup Encryption

Enable AES-256 encryption per backup job:

```powershell
# VBR console: Job Properties → Storage → Enable backup file encryption
# Enter encryption password — stored in VBR config DB
# Export encryption keys after creation: Main Menu → Manage Passwords → Export
```

### S3 Object Lock (SOBR Capacity Tier)

Configure Object Lock in `Compliance` mode:
- VBR console → SOBR → Capacity Tier → Enable immutability
- Set immutability period = retention period + 10 days buffer
- Compliance mode: even bucket owner cannot delete during immutability period
