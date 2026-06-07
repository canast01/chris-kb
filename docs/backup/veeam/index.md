# Veeam

<div class="kb-summary">
Veeam Backup & Replication — Backup Server scheduling, Proxy data movement via VADP or agent, and Scale-Out Backup Repository with immutable object storage offload.
</div>

```text
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


```text
┌───────────────────────── Veeam Backup & Replication — Installation Sequence ──────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Windows Server 2019/2022  ·  8+ vCPU  ·  32 GB RAM  ·  500 GB catalog disk (scale with jobs)         │
│  SQL Server 2019+ local or remote  ·  service accounts with local admin and SQL sysadmin              │
│  TCP 9392 (console)  ·  2500 (transport)  ·  443 (cloud/portal)  ·  6160 (installer service)          │
│  DNS forward + reverse for all VBR, proxy, and repo nodes  ·  NTP sync to domain or PDC               │
│  vCenter read/write service account  ·  vSphere API access confirmed                                  │
│                                                                                                       │
│                                        │  install VBR server                                          │
│                                        ▼                                                              │
│  Step 2 · Backup Server                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Run VBR installer on Windows host  ·  point to SQL instance  ·  accept default services              │
│  Activate licence  ·  connect vCenter via Add VMware vSphere infrastructure wizard                    │
│  VBR Management Service  ·  Mount Service  ·  Backup Service all show Running                         │
│  Configure global settings: email notifications, job parallelism, backup I/O control                  │
│  Install Veeam Backup Enterprise Manager if multi-VBR console is needed                               │
│                                                                                                       │
│                                        │  add proxy servers                                           │
│                                        ▼                                                              │
│  Step 3 · Backup Proxies                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add Windows or Linux proxy via Managed Servers  ·  install Veeam Transport Service                   │
│  Assign transport mode: Network (NBD), HotAdd (VMFS), or Direct SAN per datastore type                │
│  Set max concurrent tasks per proxy  ·  assign proxies to backup jobs explicitly or auto              │
│  For large environments: dedicated proxies per site or per datastore cluster                          │
│                                                                                                       │
│                                        │  configure backup repositories                               │
│                                        ▼                                                              │
│  Step 4 · Backup Repositories                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add repository: Windows/Linux path, SMB share, dedup appliance, or object storage                    │
│  Scale-Out Backup Repository (SOBR): combine extents  ·  set capacity tier to object storage          │
│  Enable immutability on S3/object extents or on Linux XFS + immutable flag repos                      │
│  Set retention policy per repo  ·  enable per-VM backup chains for granular restore                   │
│  Verify repo is reachable from proxies  ·  test write with a small job                                │
│                                                                                                       │
│                                        │  install Veeam ONE                                           │
│                                        ▼                                                              │
│  Step 5 · Veeam ONE                                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Veeam ONE server (separate VM)  ·  connect to VBR server and vCenter                          │
│  Veeam ONE Monitor: real-time job and infrastructure alarms  ·  configure alert thresholds            │
│  Veeam ONE Reporter: capacity, chargeback, and compliance reports on schedule                         │
│  Install Veeam ONE Agent on VBR server for deep job-level telemetry                                   │
│                                                                                                       │
│                                        │  create jobs and policies                                    │
│                                        ▼                                                              │
│  Step 6 · Jobs & Policies                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create backup jobs: select VMs/containers  ·  assign proxy + repo  ·  set retention                  │
│  Add backup copy job to secondary repo or tape  ·  test restore from both tiers                       │
│  Configure SureBackup job for automated restore verification  ·  set test schedule                    │
│  Enable application-aware processing per VM (VSS quiesce)  ·  test SQL/Exchange aware                 │
│  Document RPO/RTO per job  ·  confirm monitoring alerts reach on-call distribution list               │
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
