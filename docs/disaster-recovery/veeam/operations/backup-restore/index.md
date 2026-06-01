# Veeam — Backup & Restore


<div class="kb-summary">
Veeam Backup & Replication provides comprehensive recovery options ranging from full VM restore to granular application-item recovery. Choosing the right restore type minimises RTO and avoids unnecessary data movement.
</div>

---

## Restore Type Decision Tree

```mermaid
flowchart TD
    A([Recovery Required]) --> B{What is lost?}
    B --> |Entire VM| C{Production available?}
    B --> |Files/Folders| G[File-Level Recovery]
    B --> |Application data\nExchange/SQL/AD| H[Application-Item Recovery]
    B --> |VM config only| I[VM Config Restore]

    C --> |Yes — RTO flexible| D[Full VM Restore\nto original/new location]
    C --> |No — RTO critical| E[Instant VM Recovery\nrun from backup]

    E --> F[Storage vMotion\nto production after stabilised]
    D --> J([Validation & sign-off])
    F --> J
    G --> J
    H --> J
    I --> J
```
```
┌────────────────────────────────────── Veeam — Backup & Restore ───────────────────────────────────────┐
│                                                                                                       │
│    Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Backup (Protection)              │  │              Restore (Recovery)             │   │
│   │          Add-VBRJob / Start-VBRJob           │  │             Get-VBRRestorePoint             │   │
│   │              Quiesce source I/O              │  │            Select recovery point            │   │
│   │             Take snapshot / CBT              │  │           Mount or copy to target           │   │
│   │           Transfer changed blocks            │  │              Validate integrity             │   │
│   │             Commit to repository             │  │             Restart application             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Key Veeam Commands                                      │   │
│   │                           Backup trigger  : Add-VBRJob / Start-VBRJob                         │   │
│   │                              List points     : Get-VBRRestorePoint                            │   │
│   │                           Health status   : Start-VBRInstantVMRecovery                        │   │
│   │                             Retention mgmt  : Invoke-VBRHealthCheck                           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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
```sql

This performs a Storage vMotion in the background. The VM remains live throughout.

---

## Full VM Restore

Full VM Restore copies the backup to a production datastore. Use for planned recoveries or when instant recovery is not required.

```text
Veeam Console → Home → Restore → VMware vSphere VMs →
  Entire VM Restore → select backup → select restore point →
  Original location or New location → select ESXi host and datastore →
  Power on VM after restoring → Finish
```

```powershell
$vm     = Find-VBRViEntity -Name "PRODVM01"
$backup = Get-VBRBackup -Name "PRODVM01 - Backup"
$rp     = Get-VBRRestorePoint -Backup $backup | Sort-Object CreationTime | Select-Object -Last 1

$options = New-VBRViRecoveryOptions -PowerVM $true

Start-VBRRestoreVM -RestorePoint $rp -ToOriginalLocation -RecoveryOptions $options
```

---

## File-Level Recovery

Restore individual files from any Windows or Linux guest backup without mounting the full VM.

```text
Veeam Console → Home → Restore → Guest Files → Windows / Linux →
  select backup → select restore point → browse guest file system →
  right-click file → Restore to original location / Keep / Overwrite
```

```powershell
# Mount backup for browse/copy
$rp     = Get-VBRRestorePoint -Backup (Get-VBRBackup -Name "FILESERVER01") |
          Sort-Object CreationTime -Descending | Select-Object -First 1

$session = Start-VBRWindowsFileRestore -RestorePoint $rp
# Session opens Windows Explorer-like browser in console
```

---

## Application-Item Recovery

### Exchange Mailbox Recovery

```text
Veeam Console → Home → Restore → Microsoft Exchange Items →
  select Exchange server backup → browse mailbox → select items →
  Restore to: Original mailbox / PST export / Another mailbox
```

### SQL Database Recovery

```text
Veeam Console → Home → Restore → Microsoft SQL Server Items →
  select SQL server backup → select database → select restore point →
  Restore to original location / Restore to another server
```

```powershell
# SQL restore via PowerShell
$rp = Get-VBRRestorePoint -Backup (Get-VBRBackup -Name "SQLSERVER01") |
      Sort-Object CreationTime -Descending | Select-Object -First 1

Start-VBRSQLDatabaseRestore -RestorePoint $rp `
  -TargetSQLServer "SQLSERVER01" `
  -DatabaseName "ProductionDB" `
  -ToOriginalLocation
```

### Active Directory Object Recovery

```text
Veeam Console → Home → Restore → Microsoft Active Directory Items →
  select Domain Controller backup → browse AD → select object →
  Restore to original location (will re-hydrate in AD)
```

---

## Veeam DataLabs — Restore Testing

DataLabs allows testing restores in an isolated sandbox without touching production.

```text
Veeam Console → Inventory → Virtual Labs → Run Recovery Verification →
  select backup → select VMs to test → select lab → Run verification
```

**Scheduled SureBackup jobs automate this for all production backups:**

```text
Veeam Console → Home → Jobs → SureBackup Job →
  configure virtual lab, application group, and backup job →
  set schedule (weekly recommended)
```

SureBackup boots each VM in the isolated lab and runs application-specific tests (ping, heartbeat, port check, custom script).

---

## Restore Validation Checklist

| # | Check | Method |
|---|---|---|
| 1 | VM powered on and accessible | vCenter console / ping |
| 2 | Guest OS booted successfully | Event log / OS login |
| 3 | Disk count and capacity correct | `lsblk` / Disk Manager |
| 4 | Network connectivity restored | `ping`, `traceroute`, port test |
| 5 | Application services running | Service status / health endpoint |
| 6 | Data integrity verified | Application-level check |
| 7 | DNS and hostname correct | `hostname`, `nslookup` |
| 8 | Backup jobs resumed targeting restored VM | Veeam console → Jobs |
| 9 | Monitoring alerts cleared | Monitoring platform |
| 10 | ITSM incident updated with restore details | Ticket notes + closure |

---

## Common Restore Issues

| Issue | Cause | Fix |
|---|---|---|
| Restore fails: no free space | Target datastore full | Free space or select different datastore |
| Instant recovery VM unresponsive | Network conflict (duplicate IP) | Use isolated network for instant recovery |
| File-level restore: guest OS not detected | VMware Tools missing | Use volume-level or full VM restore |
| SQL restore fails: database in use | Active connections | Disconnect users, set single-user mode |
| Exchange restore: mailbox not found | Old backup predates mailbox creation | Use newer restore point |
| SureBackup: VM fails heartbeat test | Boot time exceeded | Increase boot delay in DataLabs settings |

---

## Related Pages

- [Veeam — Architecture](../../architecture/how-it-works/index.md)
- [Veeam — Health Checks](../health-checks/index.md)
- [Veeam — Troubleshooting](../../troubleshooting/common-issues/index.md)
