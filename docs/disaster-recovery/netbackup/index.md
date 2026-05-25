# NetBackup

<div class="kb-summary">
Veritas NetBackup enterprise backup — three-tier architecture with Primary Server catalog, Media Servers for data movement, and MSDP deduplication with AIR image replication.
</div>

```
┌──────────────────────────────────────── NetBackup — Overview ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                           NetBackup                                           │   │
│   │      Enterprise backup and recovery — master/media/client architecture with deduplication     │   │
│   │             Master Server     — scheduler, catalog, policy engine, job controller             │   │
│   │             Media Server      — data mover, dedup engine, storage unit management             │   │
│   │          Client Agent      — installed on protected host; sends data to media server          │   │
│   │      Management: 443 (Web UI) · Auth: NBU CA host-ID certificates; AD/LDAP for web UI lo      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture: components work together to deliver NetBackup capabilities                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Operations                 │   │
│   │ Master Server     — scheduler, catalog, pol  │  │             bpbackup / bprestore            │   │
│   │ Media Server      — data mover, dedup engin  │  │              bplist / bpdbjobs              │   │
│   │ Client Agent      — installed on protected   │  │               nbpemreq / bpps               │   │
│   │ NetBackup Web UI  — browser admin portal on  │  │             tpconfig / nbstlutil            │   │
│   │ Catalog           — PostgreSQL DB tracking   │  │           bpexpdate / bpimmediate           │   │
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
```text
┌──────────────────────────────────────────────────────────────────────┐
│                    NetBackup Architecture                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │              Master / Primary Server                         │    │
│  │   Policy catalog · job scheduling · device management        │    │
│  └──────────────────────────────┬───────────────────────────────┘    │
│                                 │ job dispatch                       │
│  ┌──────────────────────────────▼───────────────────────────────┐    │
│  │              Media Server(s)                                 │    │
│  │   Data mover · MSDP deduplication · multiplexing             │    │
│  └─────────┬─────────────────────────────────┬──────────────────┘    │
│            │ agent backup                    │ data write            │
│  ┌─────────▼──────────────────┐   ┌──────────▼───────────────────┐   │
│  │  Client Agents             │   │  Storage Units               │   │
│  │  Linux · Windows · Oracle  │   │  Disk (MSDP pool)            │   │
│  │  SQL · VMware proxy        │   │  Tape (robot library)        │   │
│  └────────────────────────────┘   │  Cloud (S3 / Blob)           │   │
│                                   └──────────────────────────────┘   │
│                                                                      │
│  AIR (Auto Image Replication): MSDP ──► remote MSDP (DR site)        │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Three-tier topology, Primary Server catalog, Media Servers, MSDP dedup, and key processes.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
