# Veeam — Scripts


<div class="kb-summary">
Veeam — Scripts reference.
</div>

```text
┌─────────────────────────────────────────── Veeam — Scripts ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Veeam — Automation Scripts                                  │   │
│   │               Scripts automate routine Veeam operations — run via cron or CI/CD               │   │
│   │               Always store credentials in vault (not in script); log all output               │   │
│   │                 Test scripts in non-production before scheduling in production                │   │
│   │                        Scope scripts to least-privilege service account                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Status / Reporting Scripts          │  │              Automation Scripts             │   │
│   │           Job success rate report            │  │            Auto-expire old points           │   │
│   │              Capacity trending               │  │          Auto-add new VMs to policy         │   │
│   │            SLA compliance report             │  │          Nightly DR test validation         │   │
│   │             RPO / RTO dashboard              │  │             Alert on job failure            │   │
│   │          Start-VBRInstantVMRecovery          │  │               Get-VBRJob | fl               │   │
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
PowerShell scripts for Veeam automation use the Veeam PowerShell snap-in and should be scheduled via Windows Task Scheduler on the Backup Server. Scripts must load the snap-in and connect to VBR at the start of each execution, and disconnect cleanly at the end. Output should be written to a dated log file and emailed or pushed to a monitoring system.

| Script | Language | Purpose |
|---|---|---|
| `veeam_job_summary.ps1` | PowerShell | Queries all job sessions from last 24 hours; emails pass/warn/fail counts |
| `veeam_restore_point_age.ps1` | PowerShell | Reports oldest restore point per protected VM; alerts on stale restore points |
| `veeam_sobr_capacity.ps1` | PowerShell | Iterates SOBR extents; alerts when any extent exceeds 80% usage |
| `veeam_surebackup_trigger.ps1` | PowerShell | Triggers SureBackup job for critical group; parses result and posts to ticketing system |
| `veeam_backup_copy_health.ps1` | PowerShell | Confirms backup copy jobs have run within expected window; alerts on missed runs |

**Script conventions**

```powershell
Add-PSSnapin VeeamPSSnapIn -ErrorAction SilentlyContinue
Connect-VBRServer -Server "localhost"
# ... script logic ...
Disconnect-VBRServer
```

- Store VBR credentials using Windows Credential Manager or retrieve from CyberArk at runtime.
- Use `Try/Catch/Finally` blocks to ensure `Disconnect-VBRServer` is called even on error.
