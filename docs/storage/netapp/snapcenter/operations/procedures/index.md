# SnapCenter — Procedures

> Part of the [SnapCenter Operations](../index.md) reference.

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

1. Navigate to **Resources** → select the resource group or resource
2. Click **Back Up Now**
3. Select the policy to apply
4. Confirm and monitor via **Monitor → Jobs**

---

## Policies

Policies define how SnapCenter performs backups — schedule, retention, SnapMirror/SnapVault replication, and consistency settings.

### Key Policy Attributes

- **Backup type** — Snapshot-based, log backup, full/differential
- **Schedule frequency** — Hourly, daily, weekly, monthly
- **Retention** — Number of snapshots to retain on primary
- **Replication** — Update SnapMirror / SnapVault after backup
- **Consistency** — Crash-consistent vs. application-consistent

### Create a Policy

1. Navigate to **Settings → Policies → New**
2. Select the plug-in type (SQL Server, Oracle, Windows, etc.)
3. Configure backup type, schedule, retention count, and SnapMirror update setting
4. Save the policy

### Assign a Policy to a Resource Group

1. Navigate to **Resources → Resource Groups**
2. Select the resource group → **Modify**
3. In the **Policies** step, attach the required policy
4. Set the schedule (if not already in the policy)
