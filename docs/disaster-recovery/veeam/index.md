# Veeam

<div class="kb-summary">
Veeam Backup & Replication — Backup Server scheduling, Proxy data movement via VADP or agent, and Scale-Out Backup Repository with immutable object storage offload.
</div>

```powershell
┌────────────────────────────────────────── Veeam — Overview ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                             Veeam                                             │   │
│   │    VM backup and DR — agentless VMware/Hyper-V backup with instant recovery and replication   │   │
│   │           Veeam Backup Server — scheduler, job engine, catalog, REST API (port 9419)          │   │
│   │       Backup Proxy        — data mover; VMware VADP for CBT snapshots; SAN/NAS/LAN modes      │   │
│   │        Backup Repository   — target storage: SOBR, CIFS/NFS, S3 object, dedup appliance       │   │
│   │  Management: 9419 (Veeam REST API) · Auth: Windows/AD auth for Veeam console; service account │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture: components work together to deliver Veeam capabilities                               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Operations                 │   │
│   │ Veeam Backup Server — scheduler, job engine  │  │          Add-VBRJob / Start-VBRJob          │   │
│   │ Backup Proxy        — data mover; VMware VA  │  │             Get-VBRRestorePoint             │   │
│   │ Backup Repository   — target storage: SOBR,  │  │          Start-VBRInstantVMRecovery         │   │
│   │ Mount Server        — used for instant VM r  │  │               Get-VBRJob | fl               │   │
│   │ Veeam ONE           — optional monitoring:   │  │            Invoke-VBRHealthCheck            │   │
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

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
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
