# Veeam Operations

This page covers the recurring operational tasks for Veeam Backup & Replication: daily and weekly checks, job creation, copy job setup, SOBR management, and pre-upgrade procedures.

---

## Daily Check Routine

The primary review surface is the **Home** view in the VBR console, which shows job counts grouped by status (Running, Success, Warning, Failed). Work through this list top-to-bottom every morning.

### Job Controller Review

Open **Home > Jobs** and sort by **Last Result**. Failed jobs surface at the top. For each failed or warning job:

1. Right-click the job and select **Statistics**.
2. Expand the failed task — the **Reason** column contains the proximate cause.
3. Note the time of failure and whether it was a retry or first attempt.

```powershell
# Quick PowerShell view of last result per job
Get-VBRJob | Select-Object Name, LastResult, LastRun | Sort-Object LastResult
```

Expected output columns: `Name`, `LastResult` (Success / Warning / Failed / None), `LastRun` (timestamp).

### Failed and Warning Jobs

- **Failed** — investigate before the next scheduled run. Do not allow a job to accumulate two consecutive failures without a documented root cause.
- **Warning** — commonly caused by a VM snapshot commit delay, VSS writer timeout, or guest processing credential issue. Document the cause. Repeated warnings on the same job indicate a structural problem.

```powershell
# List jobs with a non-success last result
Get-VBRJob | Where-Object { $_.LastResult -ne "Success" -and $_.LastResult -ne "None" } |
    Select-Object Name, LastResult, LastRun
```

### SOBR Capacity Check

In **Backup Infrastructure > Scale-Out Repositories**, verify that no extent shows **Sealed** or **Unavailable** status. Check the free space on each performance tier extent.

```powershell
# Repository free space — all repos including SOBR extents
Get-VBRRepository | Select-Object Name, @{N="FreeGB";E={[math]::Round($_.FreeSpace/1GB,1)}}, @{N="TotalGB";E={[math]::Round($_.TotalSpace/1GB,1)}}
```

Flag any extent below 10% free space for immediate action (offload trigger or capacity expansion).

### Tape Check (if applicable)

- Confirm the daily tape job completed and media was ejected on schedule.
- Verify the **Tape** node shows no **Error** state for the library or drives.
- Confirm physical tapes are noted for offsite transport per the media rotation policy.

### Daily Checklist Summary

- [ ] Home view — review Success / Warning / Failed job counts
- [ ] Investigate all Failed jobs — document error and remediation
- [ ] Review all Warning jobs — identify root cause, escalate if recurring
- [ ] SOBR extents — confirm no Sealed or Unavailable extent
- [ ] Repository free space — flag any extent below 10% free
- [ ] Active sessions — confirm no job is running more than 2x its normal duration
- [ ] Tape eject — confirm tapes are offsite (if applicable)

---

## Weekly Checks

### SureBackup Verification Job Review

Run or review the scheduled SureBackup job for critical VM groups. In **Home > Last 24 Hours** (adjust filter to last 7 days), locate SureBackup sessions and check the **Verification** column.

A SureBackup failure means the backup is not confirmed restorable — escalate immediately.

```powershell
# List SureBackup sessions from the last 7 days
Get-VBRBackupSession | Where-Object {
    $_.JobType -eq "SureBackup" -and $_.CreationTime -gt (Get-Date).AddDays(-7)
} | Select-Object JobName, Result, CreationTime, EndTime
```

### Repository Capacity Trend

Pull weekly capacity snapshots and compare against the previous week to identify jobs with abnormal data growth.

```powershell
# Capacity across all repositories
Get-VBRBackupRepository | Select-Object Name,
    @{N="FreeGB";E={[math]::Round($_.FreeSpace/1GB,1)}},
    @{N="TotalGB";E={[math]::Round($_.TotalSpace/1GB,1)}},
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpace/$_.TotalSpace)*100,1)}}
```

Flag any repository trending to reach capacity within 30 days at current growth rate.

### Retention Compliance

Verify that restore point counts match the configured retention for each job. Orphaned restore points (job deleted but chain retained) consume space and should be cleaned up.

```powershell
# Count restore points per backup job
Get-VBRBackup | ForEach-Object {
    $rp = Get-VBRRestorePoint -Backup $_
    [PSCustomObject]@{
        Job        = $_.JobName
        Points     = $rp.Count
        Oldest     = ($rp | Sort-Object CreationTime | Select-Object -First 1).CreationTime
        Newest     = ($rp | Sort-Object CreationTime -Descending | Select-Object -First 1).CreationTime
    }
}
```

---

## Verifying a Backup is Restorable

### Instant VM Recovery Test

Use Instant VM Recovery (IVR) to start a VM directly from the backup file. This is the fastest way to confirm the restore chain is intact.

1. In the VBR console, go to **Home > Restores > Virtual Machines**.
2. Select **Instant Recovery > VMware vSphere VM**.
3. Choose the backup job and the most recent restore point.
4. Select a target host and datastore that will not conflict with production.
5. Start the VM in **Restore Mode** (isolated/sandbox network recommended).
6. Confirm the VM powers on and the guest OS boots successfully.
7. Run **Undo Instant Recovery** to clean up — do not leave IVR VMs running.

```powershell
# Start Instant VM Recovery via PowerShell (requires Veeam PS module)
$rp = Get-VBRRestorePoint -Name "vm01" | Sort-Object CreationTime -Descending | Select-Object -First 1
Start-VBRInstantRecovery -RestorePoint $rp -Server "esxi-host01" -Datastore "ds-recovery"
```

### File-Level Restore Test

For Windows VMs, mount the backup and browse files to confirm data integrity:

1. In the console, right-click the backup job and select **Restore guest files > Microsoft Windows**.
2. Choose the restore point.
3. Browse to a known file (e.g., a log file with a recent timestamp) and confirm it is accessible.
4. Optionally restore one file to an alternate location to confirm write path.

---

## Backup Job Creation Checklist

Before creating a new backup job, confirm the following are defined:

| Parameter | Decision Required |
|---|---|
| VM scope | Individual VMs, container (folder/tag/cluster), or policy-based |
| Proxy assignment | Automatic or specific proxy (network vs. hot-add vs. direct SAN) |
| Repository | Target SOBR or standalone repo — confirm sufficient capacity |
| Retention | Restore points count or GFS (daily/weekly/monthly/yearly) |
| Schedule | Daily window; allow offset if proxy is shared across jobs |
| Application-aware | Enable for VMs with SQL, Exchange, Oracle — requires guest credentials |
| Guest OS credentials | Pre-add credentials to the Veeam Credentials Manager |
| Exclusions | Exclude swap/temp disks, ISO mount points, VMs in dev/test if appropriate |
| Notifications | Enable email or Veeam ONE alert for job failures |

```powershell
# Create a simple VM backup job via PowerShell
$vm     = Find-VBRViEntity -Name "vm01"
$repo   = Get-VBRBackupRepository -Name "SOBR-Primary"
$cred   = Get-VBRCredentials -Name "svc-veeam-guest"

Add-VBRViBackupJob `
    -Name "vm01-daily" `
    -Entity $vm `
    -BackupRepository $repo `
    -GuestCredentials $cred `
    -ApplicationAwareProcessing $true
```

After creation:
- [ ] Run the job once manually and verify success before relying on the schedule.
- [ ] Confirm the restore point appears under **Home > Backups**.
- [ ] Document the job name, scope, repository, and retention in the CMDB or runbook.

---

## Backup Copy Job Setup (Offsite / Cloud Target)

Backup copy jobs pull from a source backup job and write a secondary chain to an offsite or cloud repository. This is the primary mechanism for the 3-2-1 rule.

### Steps

1. Go to **Home > Backup Copy > VMware vSphere Backup...** (or Hyper-V equivalent).
2. Select the **source** — a specific backup job or all backups from a repository.
3. Select the **target repository** — object storage (S3-compatible, Azure Blob, Wasabi, etc.) or a remote Linux/Windows repo.
4. Set the **copy interval** (e.g., every 1 day) and configure GFS retention independently of the source job.
5. Enable **encryption** on the target if the repository is offsite or cloud.

```powershell
# List existing backup copy jobs
Get-VBRJob -Type BackupSync | Select-Object Name, LastResult, LastRun

# Check copy job sessions
Get-VBRBackupSession | Where-Object { $_.JobType -eq "BackupSync" } |
    Sort-Object CreationTime -Descending | Select-Object -First 10 |
    Select-Object JobName, Result, CreationTime, EndTime
```

**Key configuration points:**

- Copy jobs should use a different window than the primary job to avoid proxy contention.
- If targeting cloud object storage (capacity tier), enable **decompress before storing** only if the target does not deduplicate.
- Monitor copy job lag — if the copy job is consistently behind, investigate WAN bandwidth or proxy capacity.

---

## SOBR Capacity Management

### Offload Policy

In **Backup Infrastructure > Scale-Out Repositories**, select the SOBR and open **Properties > Capacity Tier**. Configure:

- **Move backups older than N days** — set based on how long backups should remain on fast storage before offloading to object storage.
- **Copy backups to object storage as soon as they are created** — use this for a continuous offload model (no delay).
- **Encrypt data uploaded to object storage** — always enable for cloud targets.

Trigger an immediate offload manually when an extent is approaching capacity:

```powershell
# Trigger SOBR offload (capacity tier upload)
$sobr = Get-VBRScaleOutBackupRepository -Name "SOBR-Primary"
Invoke-VBRScaleOutBackupRepositoryOffload -ScaleOutBackupRepository $sobr
```

### Archive Tier

If using Glacier, Azure Archive, or similar cold storage as an archive tier, configure the **Archive Tier** tab within the SOBR:

- Set the archive cutoff (e.g., move GFS monthly restore points older than 6 months to archive).
- Note that retrieval from archive tier takes hours — document the expected RTO for archived restores.

### Sealing Extents

When an extent needs to be decommissioned:

1. Right-click the extent and select **Set to Seal** — Veeam will evacuate data to other extents during the next job run.
2. Monitor evacuation progress in **Backup Infrastructure** until the extent shows 0 restore points.
3. Remove the extent only after it is fully evacuated.

---

## Pre-Upgrade Checklist (Veeam B&R Version Upgrades)

Complete this checklist before upgrading VBR to a new major or minor version.

### Before the Upgrade Window

- [ ] Read the Veeam release notes — check for breaking changes, deprecated features, and required component upgrades.
- [ ] Verify OS and SQL Server compatibility for the new version.
- [ ] Export the current VBR configuration backup:
  ```powershell
  Export-VBRConfiguration -Path "C:\vbr-config-backup-$(Get-Date -Format yyyyMMdd).xml"
  ```
- [ ] Take a snapshot of the Veeam Backup Server VM (if virtualised) immediately before the upgrade.
- [ ] Confirm all running jobs are complete and no jobs are scheduled to start during the upgrade window.
- [ ] Upgrade VMware Tools on the Backup Server VM if it is virtualised (unrelated to Veeam but good practice).
- [ ] Notify stakeholders of the maintenance window and expected impact.
- [ ] Download the ISO or installer from Veeam's site and verify the checksum.

### During the Upgrade

- Stop all running jobs before launching the installer.
- The installer will upgrade the VBR server, console, and (optionally) managed components (proxies, repositories).
- Allow the installer to upgrade managed components in the same window — components running mismatched versions will produce warnings.

### After the Upgrade

- [ ] Confirm the VBR service starts and the console connects.
- [ ] Run `Get-VBRJob` to confirm all jobs are visible and their schedules are intact.
- [ ] Manually start a non-critical backup job to confirm end-to-end function.
- [ ] Upgrade the Veeam ONE server and agent if in use (must match VBR version).
- [ ] Delete the pre-upgrade VM snapshot after 48 hours of stable operation.
- [ ] Update this runbook with the new version number and upgrade date.
