# SnapCenter Troubleshooting
## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Plugin not connecting to host | SnapCenter Agent service stopped or firewall blocking TCP 8145 | Settings → Hosts → Refresh host; check agent service: `Get-Service SnapCenter*` (Windows) or `systemctl status spl` (Linux); verify firewall rules |
| Backup job failing with quiesce error | Application not responding to pre-backup script; VSS writer error (SQL/Exchange) | Check application logs on the host; test script manually; on Windows, check VSS writer state: `vssadmin list writers` |
| Clone operation failing with space error | Insufficient free space on destination aggregate; FlexClone license not present | Check aggregate capacity on ONTAP: `storage aggregate show`; verify FlexClone license: `system license show` |
| SnapVault update failing — source snapshot missing | Source snapshot deleted before XDP transfer completed; retention policy mismatch | On destination cluster: `snapmirror show -destination-path`; run `snapmirror resync` or re-initialize the XDP relationship |
| Restore job failing with LUN mapping error | LUN already mapped to another host; igroup mismatch during restore | Check igroup membership: `lun mapping show` on ONTAP; unmount LUN on conflicting host; remap to correct igroup |
| Resource group stuck in running state | Agent crash or hung pre/post script on target host | Kill job from Jobs → Monitor → Cancel; restart SnapCenter agent on host (`Restart-Service SnapCenter*` or `systemctl restart spl`); investigate script exit codes |
| SnapCenter Server unavailable (GUI 503 error) | IIS app pool crashed; SnapCenter web service stopped | On server: `iisreset`; check Windows services: `SnapCenter_WebApp`, `SchedulerSvc`; review IIS error logs |
| Backup succeeds but no snapshot visible on ONTAP | ONTAP storage connection uses wrong SVM credentials; snapshot naming mismatch | Re-verify ONTAP credentials in Settings → Storage Systems; check `snapshot show -volume <vol>` on ONTAP directly |

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

# Check email notification settings
Get-SmEmailNotification
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

## Before Calling Support

1. Reproduce the issue and capture the Job ID from Jobs → Monitor
2. Collect SnapCenter support bundle: Help → Support → Generate Support Bundle
3. Note the SnapCenter Server version: Help → About
4. Note ONTAP version of all registered storage systems
5. Export the error message from the failed job: `Get-SmJobSummaryReport -JobId <id>`
6. Collect plugin host OS logs (Windows Event Log or Linux syslog) for the timeframe of the failure
7. Open a case at [https://mysupport.netapp.com](https://mysupport.netapp.com) under the SnapCenter product
