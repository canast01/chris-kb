---
tags:
  - netbackup
---
# NetBackup

<div class="kb-summary">
Veritas NetBackup enterprise backup — three-tier architecture with Primary Server catalog, Media Servers for data movement, and MSDP deduplication with AIR image replication.

*Applies to: NetBackup 10.x*
</div>

```text
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
┌────────────────────────────── Veritas NetBackup — Installation Sequence ──────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  RHEL 8/9 or Windows 2019+  ·  Primary: 16 vCPU, 64 GB RAM, 1 TB catalog (SSD)                        │
│  Name resolution: all nodes must resolve each other by FQDN + short name                              │
│  TCP 1556 (BPCD)  ·  13724 (vnetd)  ·  13782 (bprd)  ·  443 (web UI)                                  │
│  Service account with sudo/local admin  ·  NTP synced  ·  no firewall blocking NBU ports              │
│  Licence key or token from Veritas portal  ·  MSDP sizing worksheet completed                         │
│                                                                                                       │
│                                        │  install Primary Server                                      │
│                                        ▼                                                              │
│  Step 2 · Primary Server                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Run NetBackup installer  ·  select Primary Server role  ·  accept default port layout                │
│  Complete web UI setup wizard at https://<primary>:8443/webui  ·  set admin password                  │
│  Activate licence  ·  configure SMTP for job notifications  ·  set master name                        │
│  Verify daemons: nbpem, nbstm, nbsl, nbsd, nbrb, nbemm all running                                    │
│  Configure catalog backup: frequency, destination, retention  ·  test catalog backup                  │
│                                                                                                       │
│                                        │  add Media Servers                                           │
│                                        ▼                                                              │
│  Step 3 · Media Servers                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install NetBackup on each media server  ·  select Media Server role  ·  register to Primary          │
│  Configure storage server for MSDP: set MSDP pool path and size per media server                      │
│  Tune MSDP threads and cache size based on expected ingest rate                                       │
│  Verify media server appears in Host Management → Hosts with Active status                            │
│  Enable NBU SSO between media servers for load-balanced data movement                                 │
│                                                                                                       │
│                                        │  deploy clients                                              │
│                                        ▼                                                              │
│  Step 4 · Clients                                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Push NBU client from Primary: Host Management → Add Hosts → push install                             │
│  For VMs: configure VMware Intelligent Policy (VIP) — no client agent needed                          │
│  Oracle/SQL/Exchange: install DB agent  ·  configure credentials per instance                         │
│  Verify client appears in Workloads and can be browsed for backup selection                           │
│                                                                                                       │
│                                        │  configure storage units                                     │
│                                        ▼                                                              │
│  Step 5 · Storage Units & MSDP                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create disk storage unit pointing to MSDP server  ·  set high water mark 95%                         │
│  Create cloud storage unit (S3) for long-term retention  ·  enable AIR duplication                    │
│  Create storage lifecycle policy (SLP): tier 1 MSDP → tier 2 cloud at 30 days                         │
│  Configure storage unit groups for policy-level load balancing across media servers                   │
│  Verify dedup ratio on MSDP  ·  test duplication job to cloud tier                                    │
│                                                                                                       │
│                                        │  create policies                                             │
│                                        ▼                                                              │
│  Step 6 · Policies & Schedules                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create backup policy per workload type: VMware / Standard / Oracle / MS-SQL                          │
│  Assign clients, schedule (full weekly, incr daily), storage lifecycle policy                         │
│  Set retention: full 6 weeks, incremental 2 weeks  ·  configure multiplexing if needed                │
│  Enable NetBackup Anomaly Detection for AI-driven backup failure prediction                           │
│  Run first full  ·  verify job details  ·  test granular restore from web UI                          │
│  Document runbook: catalog recovery procedure, media server failover, AIR restore                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Three-tier topology, Primary Server catalog, Media Servers, MSDP dedup, and key processes.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
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
