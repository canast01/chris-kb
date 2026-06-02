# NetBackup — Encryption


<div class="kb-summary">
Encryption reference covering Backup Data Encryption.
</div>

```
┌─────────────────────────────────────── NetBackup — Encryption ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              NetBackup — Encryption Configuration                             │   │
│   │            AES-256 backup encryption; KMS key management; TLS 1.2+ on all channels            │   │
│   │              In-transit: TLS 1.2+ for all management; data channel also encrypted             │   │
│   │              At-rest: AES-256 on repository or vault storage; key managed by KMS              │   │
│   │               Key lifecycle: generate → use → rotate (annual) → retire → destroy              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  In-Transit                  │  │                   At-Rest                   │   │
│   │              TLS 1.2+ (minimum)              │  │              AES-256 encryption             │   │
│   │              443 (Web UI) HTTPS              │  │              KMS key management             │   │
│   │             Mutual TLS internal              │  │               WORM / immutable              │   │
│   │             Cert rotation annual             │  │             Key rotation annual             │   │
│   │             No plain-text admin              │  │               Audit key access              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
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

| Encryption Mode | Location | CPU Impact |
|---|---|---|
| Client-side | Client host | High (on production server) |
| Media server-side | Media server | Low (off client) |
| Storage-level | Array/appliance | None (hardware) |

Mandate client-side or media-server-side encryption for all policies covering PII or regulated data.
