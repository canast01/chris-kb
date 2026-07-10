---
tags:
  - netapp
  - operations
---
# SnapCenter — Procedures

<div class="kb-summary">
SnapCenter procedures: adding storage systems, configuring policies and resource groups, scheduling backups, cloning for test/dev, and decommissioning plug-in hosts.

*Applies to: SnapCenter 5.x*
</div>

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

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

---

## Backup Jobs

### Viewing Job History

![Viewing Job History](../../../../../assets/snapcenter-proc-viewing-job-history.svg)

In the SnapCenter UI:
1. Navigate to **Monitor → Jobs**
2. Filter by resource group, policy, or date range
3. Click a job to view detailed logs

Job statuses:
| Status | Meaning |
|---|---|
| Completed | Backup succeeded |
| Completed with warnings | Succeeded with non-critical issues |
| Failed | Backup failed — review job log |
| Running | Job in progress |

### Running a Backup On-Demand

![Running a Backup On-Demand](../../../../../assets/snapcenter-proc-running-a-backup-on-demand.svg)

1. Navigate to **Resources** → select the resource group or resource
2. Click **Back Up Now**
3. Select the policy to apply
4. Confirm and monitor via **Monitor → Jobs**

---

## Policies

Policies define how SnapCenter performs backups — schedule, retention, SnapMirror/SnapVault replication, and consistency settings.

### Key Policy Attributes

![Key Policy Attributes](../../../../../assets/snapcenter-proc-key-policy-attributes.svg)

- **Backup type** — Snapshot-based, log backup, full/differential
- **Schedule frequency** — Hourly, daily, weekly, monthly
- **Retention** — Number of snapshots to retain on primary
- **Replication** — Update SnapMirror / SnapVault after backup
- **Consistency** — Crash-consistent vs. application-consistent

### Create a Policy

![Create a Policy](../../../../../assets/snapcenter-proc-create-a-policy.svg)

1. Navigate to **Settings → Policies → New**
2. Select the plug-in type (SQL Server, Oracle, Windows, etc.)
3. Configure backup type, schedule, retention count, and SnapMirror update setting
4. Save the policy

### Assign a Policy to a Resource Group

![Assign a Policy to a Resource Group](../../../../../assets/snapcenter-proc-assign-a-policy-to-a-resource-group.svg)

1. Navigate to **Resources → Resource Groups**
2. Select the resource group → **Modify**
3. In the **Policies** step, attach the required policy
4. Set the schedule (if not already in the policy)

---

## Add a Host to SnapCenter

1. Navigate to **Hosts** in the SnapCenter UI and click **Add**
2. Enter the fully qualified domain name (FQDN) of the host
3. Select the plug-in packages to install — SQL Server, Oracle, Windows File System, or others as required
4. Click **Submit** — SnapCenter connects to the host and installs the selected plug-ins
5. Monitor the installation progress in the **Jobs** pane
6. Once complete, verify the host appears in the Hosts list with status **Connected** and all plug-ins show **Running**

---

## Create a Backup Policy

1. Navigate to **Settings → Policies** and click **New Policy**
2. Select the resource type the policy will cover (SQL Server, Oracle, Windows File System, etc.)
3. Set the backup schedule — hourly, daily, weekly, or monthly as required
4. Configure retention: set the number of snapshot copies to retain on primary storage and the number of SnapVault copies to retain on the vault destination
5. Enable **Update SnapMirror after backup** or **Update SnapVault after backup** if secondary replication is required
6. Review the policy summary and click **Finish** to save

---

## Clone a Database from Snapshot

1. Navigate to **Resources** and select the database to clone
2. Click **Clone** from the resource actions menu
3. Select the snapshot to use as the clone source — choose a known-good snapshot for the target recovery point
4. Specify the destination clone host and the clone database SID (SQL instance name or Oracle SID)
5. Configure any clone-specific settings (mount path, log directory, etc.) and click **Clone**
6. Monitor the clone job in **Monitor → Jobs**
7. Once complete, verify the clone database is accessible and the application can connect successfully

---

## Restore a Database to a Point in Time

1. Navigate to **Resources** and select the database to restore
2. Click **Restore** from the resource actions menu
3. Choose the recovery type: **Complete** (restore to most recent backup) or **Point-in-time** (restore to a specific timestamp)
4. For point-in-time recovery, specify the target date and time
5. Select the snapshot to use as the restore source — SnapCenter maps the snapshot to the appropriate data and log backups
6. Review the restore scope (full database, tablespace, or file-level) and confirm settings
7. Click **Restore** and monitor the job in **Monitor → Jobs**
8. Once the job completes, verify the database is online and confirm data integrity with the application team

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## Add a Host and Install Plugin

Add a managed host and push the appropriate SnapCenter plugin to it.

1. Navigate to **Hosts → Add**
2. Enter the fully qualified domain name (FQDN) of the host
3. Provide credentials (Windows: domain admin or local admin; Linux: root or sudo account)
4. Select the plugin packages to install — SnapCenter Plugin for VMware vSphere, SQL Server, Oracle, or Windows File Systems as required
5. Click **Submit** — SnapCenter connects to the host via WinRM (Windows) or SSH (Linux) and pushes the plugin
6. Monitor installation progress in the **Jobs** pane
7. Verify the host appears with status **Connected** and all plugins show **Running**

```powershell
# Verify via PowerShell after installation
Get-SCHost
```

---

## Create a Resource Group

A resource group defines which resources are backed up together under a single policy and schedule.

1. Navigate to **Resources → Resource Group → New**
2. Name the resource group and select the resource type
3. Add resources — VMs, databases, file systems, or application instances
4. Assign one or more policies to the group
5. Set the schedule (if not already defined in the policy)
6. Review and click **Finish**

```powershell
# Create a resource group via PowerShell
New-SCResourceGroup -Name "RG-Prod-SQL" -PolicyName "Daily-Policy"
```

Group resources that share the same RPO/RTO requirements — avoid mixing critical and non-critical resources in the same group.

---

## Restore from Backup

Restore a resource to its original location or an alternate target.

1. Navigate to **Resources** and select the resource to restore
2. Click **Restore** from the resource actions menu
3. Choose the backup copy to restore from — sort by date to find the correct recovery point
4. Select the restore type:
   - **Full restore** — overwrites the resource with snapshot data
   - **Granular/item-level** — restore specific files, tables, or mailbox items
5. For SQL Server: specify whether to restore to the original instance or an alternate instance
6. For VMware: restore the VM to the original datastore or an alternate datastore/folder
7. Confirm restore settings and click **Restore**
8. Monitor the job and verify application connectivity after completion

```powershell
# Check restore job status via PowerShell
Get-SCRestoreJob
```

---

## Clone a Resource

Use FlexClone to instantly create a writable, space-efficient clone for dev/test or QA purposes.

1. Navigate to **Resources** and select the resource to clone
2. Click **Clone** from the resource actions menu
3. Select the snapshot to use as the clone source
4. For SQL Server: specify the destination SQL instance and clone database name
5. For VMware: specify the destination host/folder and clone VM name
6. Configure any clone-specific options (mount path, log directory, NFS/iSCSI settings)
7. Click **Clone** and monitor the job

```powershell
# Monitor clone job status
Get-SCCloneJob
```

FlexClone operations complete in seconds regardless of volume size — no data is physically copied until the clone diverges from the parent snapshot.

---

## Monitor Backup Jobs and Alerts

Track job status and configure alerting for backup failures.

1. Navigate to **Monitor → Jobs** for live and historical job status
2. Filter by resource group, status, or date range
3. Click any job to view the detailed log including ONTAP snapshot operations

```powershell
# List failed backup jobs with error details
Get-SCJob -Status Failed | Select-Object StartTime, EndTime, ErrorMessage
```

Configure email alerts for failures:

1. Navigate to **Settings → Global Settings → SMTP**
2. Enter SMTP server, sender address, and recipient list
3. Enable notifications for **Failed** and **Completed with warnings** job states

For monitoring integration, configure SNMP traps under **Settings → Global Settings → SNMP** and add SnapCenter as a trap source in your NMS.

---

## Manage Retention and Purge Old Backups

Retention is enforced automatically by policy — SnapCenter deletes the oldest copies when the configured count is exceeded. To manually remove a specific backup:

1. Navigate to **Resources** and select the resource
2. Click **Manage Copies**
3. Select the backup copy to delete
4. Click **Delete** — this removes the snapshot from ONTAP and the entry from the SnapCenter catalog

```powershell
# Remove a backup via PowerShell
Remove-SCBackup -BackupName <backup_name>

# Clean up the catalog after manual snapshot deletions on ONTAP
Invoke-SCCatalogCleanup
```

Run `Invoke-SCCatalogCleanup` after any out-of-band snapshot deletions on ONTAP to keep the SnapCenter catalog consistent with actual storage state.

---

## See also

- [Snapcenter — Health Checks](../health-checks/)
- [Snapcenter — CLI Reference](../cli-reference/)
- [Snapcenter — Common Issues](../../troubleshooting/common-issues/)
