# SnapCenter — Health Checks

> Part of the [SnapCenter Operations](../) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Review backup jobs from the last 24 hours | `Get-SmJob -StartTime (Get-Date).AddHours(-24) \| Select JobId,JobType,Status,StartDateTime,EndDateTime` | |
| [ ] Flag any failed or stuck jobs (Status = `Failed` or `Running` for > expected duration) | `Failed` | |
| [ ] Check plugin host connectivity | `Get-SmHost \| Select HostName,HostType,PlugInStatus` | all hosts should show `Running` |
| [ ] Verify secondary (SnapVault/SnapMirror) copies exist for critical resources | `Get-SmBackup -ResourceName <resource>` | |
| [ ] Check SnapCenter Server disk usage | | review log partition growth (default logs under `C:\Program Files\NetApp\SnapCenter\SMCore\logs\`) |
| [ ] Confirm all resources are within their backup SLA window | | no resource should be missing a backup beyond the defined retention interval |
| [ ] Check certificate expiry on the SnapCenter Server | | |

## Health Check

- [ ] All backup jobs in the last 24 hours completed with `Completed` status
- [ ] No jobs are currently stuck in `Running` or `Queued` state
- [ ] All plugin hosts show `PlugInStatus: Running`
- [ ] SnapVault/SnapMirror relationships on secondary storage are healthy (verify from ONTAP: `snapmirror show -fields healthy`)
- [ ] SnapCenter Server has sufficient disk space on the log and repository partitions
- [ ] No unprotected resources flagged in the SnapCenter Dashboard
- [ ] Server TLS certificate is valid and not expiring within 30 days

~~~bash
# Connect to SnapCenter (run from a host with SnapCenter PowerShell toolkit installed)
Open-SmConnection -SMSbaseurl https://<snapcenter-server>:8146

# List all backup jobs from the last 24 hours with status
Get-SmJob -StartTime (Get-Date).AddHours(-24) | Select JobId, JobType, Status, StartDateTime, EndDateTime

# List all jobs currently in Running or Queued state
Get-SmJob | Where-Object { $_.Status -in @("Running","Queued") } | Select JobId, JobType, Status, StartDateTime

# Check plugin host connectivity and status
Get-SmHost | Select HostName, HostType, PlugInStatus, OverallStatus

# List all resource groups and their protection status
Get-SmResourceGroup | Select ResourceGroupName, PluginCode, Status

# List available backups for a specific resource
Get-SmBackup -ResourceName <resource_name> | Select BackupName, BackupTime, Status

# Check all policies
Get-SmPolicy | Select PolicyName, PluginType, BackupType
~~~
