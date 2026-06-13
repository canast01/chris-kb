---
tags:
  - operations
  - veeam
---
# Veeam — Operations



<div class="kb-summary">
Veeam day-to-day operations — backup job management, restore procedures, scale-out repository, and immutability settings.
</div>

```text
┌───────────────────────────────────────── Veeam — Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Veeam — Day-to-Day Operations                                 │   │
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
│   │  Add-VBRJob / Start-VBRJob  │  │  Start-VBRInstantVMRecovery │  │     Get-VBRRestorePoint     │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
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
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>qcommand, qlist, qoperation, REST API, and job management.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, job review, MediaAgent health, and DDB monitoring.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Change readiness, maintenance windows, and operational procedures.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Version matrix, upgrade workflow, and lifecycle management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Backup policies, restore procedures, and recovery validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for health checks and operations.</span>
</a>

</div>
