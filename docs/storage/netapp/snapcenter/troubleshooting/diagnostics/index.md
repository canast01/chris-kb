# SnapCenter — Diagnostics

> Part of the [SnapCenter Troubleshooting](../index.md) reference.

---

## Diagnostic Commands

```powershell
# Connect to SnapCenter via PowerShell
Open-SmConnection -SMSbaseurl https://<snapcenter-server>:8146

# List all jobs and filter by failed status
Get-SmJob | Where-Object { $_.Status -eq "Failed" } | Select JobId, JobType, StartDateTime, ErrorMessage

# List all resource groups and their current status
Get-SmResourceGroup | Select ResourceGroupName, Status, LastRunTime

# Check all registered hosts and plugin status
Get-SmHost | Select HostName, HostType, PlugInStatus, HostStatus

# List backups for a specific resource
Get-SmBackup -ResourceName <resource_name> | Select BackupName, BackupTime, BackupType, Status

# Get detailed information about a specific job
Get-SmJobSummaryReport -JobId <job_id>

# List all ONTAP storage connections
Get-SmStorageConnection | Select StorageName, Protocol, ClusterVersion
```

```bash
# On a Linux plugin host — check SnapCenter agent service
systemctl status spl
journalctl -u spl -n 100

# On a Windows plugin host (PowerShell)
Get-Service SnapCenter*
Get-EventLog -LogName Application -Source "SnapCenter*" -Newest 50
```

## Log Locations

| Log Source | Location |
|---|---|
| SnapCenter Server web application logs | `C:\Program Files\NetApp\SnapCenter\SnapCenter Web App\log\` |
| SnapCenter Scheduler service logs | `C:\Program Files\NetApp\SnapCenter\SnapCenter Scheduler\log\` |
| SnapCenter SMCore logs (job engine) | `C:\Program Files\NetApp\SnapCenter\SMCore\log\` |
| Windows plugin agent logs | `C:\Program Files\NetApp\SnapCenter\Snapcenter Plug-in Creator\log\` |
| Linux plugin agent logs | `/var/opt/snapcenter/spl/logs/` |
| SnapCenter Plug-in for VMware logs | `/var/log/netapp/snapcenter/` (inside the OVA appliance) |
| MySQL repository logs | `C:\Program Files\NetApp\SnapCenter\MySQL Data\` → `mysql-error.log` |
| IIS access/error logs | `C:\inetpub\logs\LogFiles\` |

For a full support bundle (all logs + config):
1. In SnapCenter GUI: Help → Support → Generate Support Bundle
2. Alternatively, run PowerShell: `Get-SmSupportBundle -Path C:\temp\snapcenter-bundle`
