# Veeam — Diagnostics

```
┌───────────────────────────────────────── Veeam — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Veeam — Diagnostic Commands                                  │   │
│   │                       Collect these before opening a vendor support case                      │   │
│   │                                    Start-VBRInstantVMRecovery                                 │   │
│   │                                         Get-VBRJob | fl                                       │   │
│   │                       Check system logs: /var/log/ or Windows Event Viewer                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │               Live Diagnostics              │   │
│   │            Application log bundle            │  │             Network connectivity            │   │
│   │            OS syslog (journalctl)            │  │              Storage path check             │   │
│   │             Core dump if crashed             │  │              Process list check             │   │
│   │             Config export/backup             │  │              Port reachability              │   │
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
## Log Locations

- VBR service log: `C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log`
- Job session logs: `C:\ProgramData\Veeam\Backup\Job_<JobName>\`
- Proxy logs: `C:\ProgramData\Veeam\Backup\` on each proxy server
- Linux agent logs: `/var/log/veeam/`
- Audit log: `C:\ProgramData\Veeam\Backup\Audit.log`

## Diagnostic Commands

```powershell
# Quick PowerShell view of last result per job
Get-VBRJob | Select-Object Name, LastResult, LastRun | Sort-Object LastResult

# List jobs with a non-success last result
Get-VBRJob | Where-Object { $_.LastResult -ne "Success" -and $_.LastResult -ne "None" } |
    Select-Object Name, LastResult, LastRun

# Check repository free space
Get-VBRBackupRepository | Select Name, FriendlyPath, Path,
  @{N="FreeMB";E={[math]::Round($_.GetContainer().CachedFreeSpace / 1MB)}}

# Check proxy status
Get-VBRViProxy | Select Name, Host, MaxTasksCount, IsDisabled

# Check Veeam service log (last 100 lines)
Get-Content "C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log" -Tail 100
```

## Support Bundle Collection

1. In the VBR console: Main Menu > Help > Support Information
2. Click "Export Logs" — select the job or time range relevant to the issue
3. The wizard packages logs from the Backup Server and relevant proxies into a single ZIP archive
