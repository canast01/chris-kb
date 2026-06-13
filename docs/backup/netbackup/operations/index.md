---
tags:
  - netbackup
  - operations
---
# NetBackup — Operations



<div class="kb-summary">
NetBackup day-to-day operations — policy management, job monitoring, tape/disk pool administration, and catalog maintenance.

*Applies to: NetBackup 10.x*
</div>

```text
┌─────────────────────────────────────── NetBackup — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               NetBackup — Day-to-Day Operations                               │   │
│   │          Daily: review job status · check health alerts · verify last backup/replica          │   │
│   │            Weekly: review capacity trends · test restore sample · review error logs           │   │
│   │             Monthly: full restore test · review retention · audit service accounts            │   │
│   │              Quarterly: DR failover test · firmware review · update documentation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Backup/Replicate      │  │           Monitor           │  │           Recover           │   │
│   │     bpbackup / bprestore    │  │       nbpemreq / bpps       │  │      bplist / bpdbjobs      │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
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
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>bpbackup, bprestore, bpadm, nbstatus, and admin commands.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, job monitoring, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Backup policies, restore procedures, and validation workflows.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Version matrix, upgrade paths, and lifecycle management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Restore procedures and recovery workflows.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for NetBackup operations.</span>
</a>

</div>

