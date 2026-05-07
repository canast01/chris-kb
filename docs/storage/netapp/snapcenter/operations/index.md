# Operations

> Part of the [NetApp SnapCenter](../) reference.

---
## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Review backup jobs from the last 24 hours | `Get-SmJob -StartTime (Get-Date).AddHours(-24) | Select JobId,JobType,Status,StartDateTime,EndDateTime` |  |
| [ ] Flag any failed or stuck jobs (Status = `Failed`, `Running` for > | `Failed` |  |
| [ ] Check plugin host connectivity | `Get-SmHost | Select HostName,HostType,PlugInStatus` | all hosts should show `Running` |
| [ ] Verify secondary (SnapVault/SnapMirror) copies exist for critical resources | `Get-SmBackup -ResourceName <resource>` |  |
| [ ] Check SnapCenter Server disk usage |  | review log partition growth (default logs under `C:\Program Files\NetApp\SnapCenter\SMCore\logs\`) |
| [ ] Confirm all resources are within their backup SLA window |  | no resource should be missing a backup beyond the defined retention interval |
| [ ] Check certificate expiry on the SnapCenter Server (GUI |  |  |

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

## Change Readiness

- [ ] All backup jobs are succeeding — no failures in the last 24 hours before the change window
- [ ] No jobs are currently stuck in `Running` or `Queued` state
- [ ] Plugin connectivity is healthy for all hosts involved in the change
- [ ] SnapCenter Server has sufficient disk space — logs and repository should be below 80% full
- [ ] Backup schedules for affected resources are paused or accounted for in the change window timing
- [ ] Application teams are notified if their resource group schedules will be disrupted
- [ ] A manual on-demand backup has been taken for critical resources before the change: `Invoke-SmBackup -Resources @{...}`

| Item | Status | Notes |
|---|---|---|
| All backup jobs succeeding (last 24h) | | |
| No stuck Running or Queued jobs | | |
| Plugin hosts all connected | | |
| SnapCenter Server disk space < 80% | | |
| Pre-change backup taken for critical resources | | |

## Incident Triage

- [ ] Navigate to SnapCenter GUI → Monitor → Jobs — identify the failing job and review the error message in the job detail
- [ ] Check the application plugin on the target host: in Settings → Hosts, select the host and click Refresh to test connectivity
- [ ] If plugin unreachable: log onto the target host and verify the SnapCenter agent service is running (Windows: `SnapCenter Plug-in for Windows`; Linux: check `snapcenter_linux_host_plugin` process)
- [ ] Check ONTAP snapshot space on the source volume: `snapshot show -vserver <svm> -volume <vol>` — ensure the volume has space for new snapshots
- [ ] If a SnapVault update is failing: check the secondary relationship from the destination cluster: `snapmirror show -destination-path <svm:vol>` — look for `broken-off` or `lag-time` issues
- [ ] Review the SnapCenter log files on the server for detailed stack traces: `C:\Program Files\NetApp\SnapCenter\SMCore\logs\`
- [ ] If a restore or clone is failing: check igroup membership and LUN mapping on ONTAP — ensure the target igroup matches the host's WWN/IQN

| Question | Answer |
|---|---|
| Which resource group and job failed? | |
| What is the error message in the job detail? | |
| Is the plugin host reachable from SnapCenter? | |
| Is the ONTAP source volume out of snapshot space? | |
| Is the secondary SnapVault relationship healthy? | |

## Maintenance Window

1. Disable or pause backup schedules for resource groups affected by the maintenance: in SnapCenter GUI, navigate to Resource Groups → select group → Modify → disable schedule
2. Notify application teams that backup jobs will not run during the window and confirm they accept the backup gap
3. For SnapCenter Server upgrades: take a full backup of the SnapCenter repository database (MySQL on the SnapCenter server) before beginning
4. Complete the planned change (plugin upgrade, ONTAP change, host maintenance, etc.)
5. After the change, re-enable resource group schedules and confirm all hosts still show plugin status `Running`: `Get-SmHost`
6. Trigger a manual on-demand backup for critical resource groups to confirm end-to-end backup functionality: GUI → Resource Groups → Back Up Now
7. Verify secondary copies replicated successfully by checking SnapVault/SnapMirror transfer on the destination ONTAP cluster

## Post-Change Validation

- [ ] Run `Get-SmHost` — all plugin hosts show `PlugInStatus: Running` with no degraded hosts
- [ ] Trigger on-demand backup for at least one representative resource group and confirm it completes with `Completed` status
- [ ] Verify backup job in the GUI shows successful snapshot creation on ONTAP: `snapshot show -vserver <svm> -volume <vol>`
- [ ] Confirm secondary copies are replicating: check SnapMirror/SnapVault relationship is healthy from the destination cluster
- [ ] Verify resource group schedules are re-enabled and next scheduled run is visible
- [ ] Check SnapCenter Server disk usage — confirm log partition has not grown unexpectedly during the change
- [ ] Perform a test restore from the most recent backup snapshot on at least one non-production resource to validate restore functionality
