---
tags:
  - dell
  - operations
---
# Data Domain — Procedures

<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Filesystem Cleaning.

*Applies to: Data Domain DD OS 7.x*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Change Readiness

Verify these items before performing any change on the Data Domain — DDOS upgrades, MTree reconfigurations, replication changes, or hardware expansions.

- [ ] `replication show` — all contexts in `Normal` state; do not proceed with a DDOS upgrade while any context is in `Error` or actively lagging
- [ ] No active backup sessions at the time of the change — confirm with backup software that no jobs are running or scheduled during the window
- [ ] `filesys cleaning` is not running: run `filesys clean status` — a cleaning run during a backup window or major change can cause I/O contention
- [ ] `alerts show current` returns no active alerts that indicate pre-existing hardware faults
- [ ] `filesys show space` confirms at least 15% raw capacity free — sufficient headroom for the cleaner to operate post-change
- [ ] Confirm a valid backup of the DD configuration: `system show` — note the current DDOS version; export the configuration backup via System Manager
- [ ] Inform backup application teams of the maintenance window; confirm they will not schedule test restores or new backup jobs during the change
- [ ] Verify ESRS / Smart Connect support connectivity before starting, so Dell support can be reached if needed

| Item | Status | Notes |
|---|---|---|
| Replication contexts in Normal state | | |
| No active backup sessions | | |
| filesys cleaning not running | | |
| No active hardware alerts | | |
| ≥15% raw capacity free | | |
| DD config backup exported | | |

## Maintenance Window

```d2
direction: right

A: "Start Maintenance" {shape: rectangle}
B: "Confirm window does not\noverlap backup schedule" {shape: rectangle}
C: "replication show\nNote context states" {shape: rectangle}
D: "Any context\nin Error?" {shape: rectangle}
E: "Resolve replication issue\nbefore proceeding" {shape: rectangle}
F: "Confirm no active backup sessions\nin backup software" {shape: rectangle}
G: "DDOS upgrade?" {shape: rectangle}
H: "filesys clean start\nWait for completion" {shape: rectangle}
I: "Export config backup\nvia System Manager" {shape: rectangle}
J: "Perform change\nper approved runbook" {shape: rectangle}
K: "filesys status\nreplication show\nalerts show current" {shape: rectangle}
L: "All healthy?" {shape: rectangle}
M: "Investigate and resolve" {shape: rectangle}
N: "Run test DDBoost backup\nConfirm job success" {shape: rectangle}
O: "Close Window" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> D
D -> F
F -> G
G -> H
G -> I
H -> I
I -> J
J -> K
K -> L
L -> M
M -> K
L -> N
N -> O
```

### Replication State

![Replication State](../../../../assets/data-domain-proc-replication-state.svg)

```bash
# Check which MTrees are replicating and their state
replication show all | grep <mtree_name>

# Show replication lag for a specific MTree
replication show stats | grep <mtree_name>
```


```text title="Expected output"
mtree_prod_data01 replication ACTIVE source=10.45.22.18 dest=10.45.22.19 lag=2.3GB
mtree_prod_data01 replication IDLE source=10.45.22.18 dest=10.45.22.20 lag=0B
mtree_prod_data01 replication ERROR source=10.45.22.18 dest=10.45.22.21 lag=45.7GB
mtree_prod_data02 replication ACTIVE source=10.45.22.18 dest=10.45.22.19 lag=1.1GB

mtree_prod_data01 replication_stats bytes_replicated=2.8TB replication_rate=125MB/s lag_time=18s last_sync=2024-01-15T14:32:11Z
mtree_prod_data01 replication_stats bytes_pending=2.3GB estimated_completion=45m
```

!!! warning "Common errors"
    **`mtree_name: command not found`** — Replace `<mtree_name>` with the actual MTree name (e.g., `mtree_prod_data01`).
    **`replication: command not found`** — Ensure you are logged into the Data Domain CLI or run commands via SSH to the management interface.
    **`grep: (standard input) is empty`** — The specified MTree does not exist or has no active replication; verify the MTree name with `replication show all` first.
### Retention Lock Review

![Retention Lock Review](../../../../assets/data-domain-proc-retention-lock-review.svg)

```bash
# Check if retention lock is enabled on an MTree
mtree retention-lock status /data/col1/<mtree_name>

# List MTrees with retention lock enabled
mtree list --verbose | grep -E "mtree|retention"
```


```text title="Expected output"
Retention Lock Status for /data/col1/archive_prod:
  Enabled: Yes
  Lock Type: Compliance
  Locked Since: 2024-01-15 09:23:47 UTC
  Retention Period: 2555 days (7 years)

Name                          Type        Retention Lock    Status
archive_prod                  Standard    Enabled           Active
backup_2024                   Standard    Enabled           Active
compliance_vault              Standard    Enabled           Active
temp_staging                  Standard    Disabled          Active
media_archive                 Standard    Enabled           Active
...
```

!!! warning "Common errors"
    **`mtree: command not found`** — Ensure you are logged into the Data Domain CLI (via SSH or console) and not a standard Linux shell; use `sysadmin` or `admin` account.
    **`Permission denied: /data/col1/<mtree_name>`** — Verify the MTree name is correct and your user account has administrative privileges; use `user show` to check current role.
    **`Retention Lock Status: Not Available`** — Confirm the MTree exists and is fully initialized; newly created MTrees may take several minutes before retention lock status is queryable.
### Creating MTrees for New Backup Applications

![Creating MTrees for New Backup Applications](../../../../assets/data-domain-proc-creating-mtrees-for-new-backup-applications.svg)

```bash
# Step 1 — create the MTree
mtree create /data/col1/<application>_backup

# Step 2 — set a quota (prevent runaway growth)
mtree quota set hard-limit 5 TiB /data/col1/<application>_backup
mtree quota set soft-limit 4 TiB /data/col1/<application>_backup

# Step 3 — create an NFS export or DDBoost storage unit
nfs add export /data/col1/<application>_backup clients <backup_server_ip>
# OR
ddboost storage-unit create <application>_backup

# Step 4 — verify
mtree show /data/col1/<application>_backup
mtree quota show
```


```text title="Expected output"
MTree /data/col1/oracle_backup created successfully
Hard limit set to 5.0 TiB for /data/col1/oracle_backup
Soft limit set to 4.0 TiB for /data/col1/oracle_backup
NFS export added: /data/col1/oracle_backup (192.168.10.45)
MTree Information
  Name: /data/col1/oracle_backup
  Capacity: 5.0 TiB
  Used: 0 B
  Available: 5.0 TiB
  Status: Active
Quota Summary
  MTree: /data/col1/oracle_backup
  Hard Limit: 5.0 TiB
  Soft Limit: 4.0 TiB
  Current Usage: 0 B
  % Used: 0%
```

!!! warning "Common errors"
    **`Error: MTree /data/col1/<application>_backup already exists`** — Use `mtree show /data/col1/<application>_backup` to verify the MTree exists, or choose a different name.
    **`Error: NFS export failed - client IP 192.168.x.x is unreachable`** — Verify the backup server IP is correct and reachable from the Data Domain appliance before adding the export.
    **`Error: Quota hard-limit must be greater than soft-limit`** — Ensure the hard-limit value is larger than the soft-limit value (e.g., hard 5 TiB, soft 4 TiB).
### Decommissioning an MTree

![Decommissioning an MTree](../../../../assets/data-domain-proc-decommissioning-an-mtree.svg)

```bash
# Step 1 — confirm backup data has been expired in the backup application
# Step 2 — remove the NFS export or DDBoost storage unit
nfs del export /data/col1/<mtree_name>
# OR
ddboost storage-unit delete <storage_unit_name>

# Step 3 — delete the MTree
mtree delete /data/col1/<mtree_name>

# Step 4 — run cleaning to reclaim space
filesys clean start
filesys clean status
```


```text title="Expected output"
# Step 1 — confirm backup data has been expired in the backup application
(no output — command completes silently)

# Step 2 — remove the NFS export or DDBoost storage unit
nfs del export /data/col1/prod_backup_mtree
Export /data/col1/prod_backup_mtree deleted successfully.

# Step 3 — delete the MTree
mtree delete /data/col1/prod_backup_mtree
MTree /data/col1/prod_backup_mtree deleted successfully.
Reclaiming space from deleted MTree...

# Step 4 — run cleaning to reclaim space
filesys clean start
Cleaning job started. Job ID: 847293
Estimated completion time: 2 hours 15 minutes

filesys clean status
Job ID: 847293
Status: Running
Progress: 34%
Space reclaimed so far: 2.3 TB
Estimated total reclaim: 6.8 TB
```

!!! warning "Common errors"
    **`Error: MTree /data/col1/prod_backup_mtree is still mounted`** — Unmount the MTree with `nfs unmount /data/col1/prod_backup_mtree` before deletion.
    **`Error: NFS export /data/col1/prod_backup_mtree in use by 3 clients`** — Disconnect all client connections or force-unmount with `nfs del export /data/col1/prod_backup_mtree -force`.
    **`Error: filesys clean already in progress (Job ID: 847291)`** — Wait for the current cleaning job to complete or cancel it with `filesys clean stop 847291` before starting a new one.
### MTree Health Summary

![MTree Health Summary](../../../../assets/data-domain-proc-mtree-health-summary.svg)

| Metric | Target | Check |
|---|---|---|
| MTree quota used | < 85% | `mtree quota show` |
| Replication lag | < 4 hours | `replication show stats` |
| Retention lock as expected | Per policy | `mtree retention-lock status` |
| DDBoost storage unit exists | Configured | `ddboost storage-unit list` |

## Filesystem Cleaning

Cleaning (garbage collection) reclaims disk space after backup data is expired or deleted by the backup application. Without regular cleaning, space is not returned to the usable pool even after backups are removed.

### How Cleaning Works

![How Cleaning Works](../../../../assets/data-domain-proc-how-cleaning-works.svg)

1. Backup application marks expired data for deletion.
2. Data Domain marks the associated dedup segments as unreferenced.
3. Cleaning scans all segments, identifies unreferenced ones, and reclaims their space.
4. Post-clean, `filesys show space` shows reduced post-comp usage.

### Running Cleaning

![Running Cleaning](../../../../assets/data-domain-proc-running-cleaning.svg)

```bash
# Start an immediate cleaning cycle
filesys clean start

# Check cleaning status
filesys clean status

# Stop cleaning in progress
filesys clean stop
```


```text title="Expected output"
Starting immediate cleaning cycle...
Cleaning cycle initiated. Cycle ID: CC-2024-01-15-0847
Estimated duration: 2 hours 15 minutes

Cleaning Status Report
======================
Cycle ID: CC-2024-01-15-0847
Status: In Progress
Start Time: 2024-01-15 08:47:23 UTC
Elapsed Time: 12 minutes 34 seconds
Progress: 23%
Filesystems being cleaned: /data/vol1, /data/vol2, /data/vol3
Estimated completion: 2024-01-15 11:02:57 UTC

Stopping cleaning cycle CC-2024-01-15-0847...
Cleaning cycle stopped successfully.
Final progress: 23% complete
Data integrity check: PASSED
```

!!! warning "Common errors"
    **`filesys clean start: ERROR - Another cleaning cycle is already in progress (Cycle ID: CC-2024-01-15-0701)`** — Wait for the current cycle to complete or use `filesys clean stop` to terminate it first.
    **`filesys clean status: ERROR - No active cleaning cycle found`** — Start a cleaning cycle with `filesys clean start` before checking status.
    **`filesys clean stop: ERROR - Insufficient privileges to stop cleaning cycle`** — Run the command with appropriate administrative credentials or use the Data Domain management console.
### Automatic Cleaning Schedule

![Automatic Cleaning Schedule](../../../../assets/data-domain-proc-automatic-cleaning-schedule.svg)

```bash
# View scheduled cleaning windows
filesys clean schedule show

# Set a cleaning schedule (run Tuesdays at 02:00)
filesys clean schedule set day tue start-time 02:00

# Enable automatic cleaning
filesys clean schedule enable

# Disable automatic cleaning (manual-only mode)
filesys clean schedule disable
```


```text title="Expected output"
Cleaning Schedule Configuration
================================
Current Schedule Status: ENABLED
Day of Week: Tuesday
Start Time: 02:00 (UTC)
Duration: 4 hours
Last Run: 2024-01-16 02:00:15
Next Run: 2024-01-23 02:00:00
Cleaning Mode: Automatic

Schedule updated successfully.
Day set to: Tuesday
Start time set to: 02:00

Automatic cleaning enabled.
Next scheduled run: Tuesday 02:00 UTC

Automatic cleaning disabled.
System is now in manual cleaning mode only.
```

!!! warning "Common errors"
    **`filesys clean schedule: command not found`** — Verify you are logged into the Data Domain CLI (use `ssh admin@<dd-ip>`) and not a standard Linux shell.
    **`Error: Schedule day must be 3-letter abbreviation (mon, tue, wed, etc.)`** — Use lowercase three-letter day abbreviations (e.g., `tue` instead of `Tuesday` or `TUE`).
    **`Error: Start time must be in HH:MM format (00:00-23:59)`** — Correct the time format to 24-hour notation, e.g., `02:00` instead of `2:00 AM`.
### Monitoring Cleaning Progress

![Monitoring Cleaning Progress](../../../../assets/data-domain-proc-monitoring-cleaning-progress.svg)

```bash
# Active cleaning progress
filesys clean status

# Space before and after (run filesys show space before and after)
filesys show space

# Cleaning history
filesys clean show history
```


```text title="Expected output"
Active cleaning progress
Cleaning is not running.

Filesystem Space Usage
Filesystem                Size      Used      Avail     Use%
/data                    50.0TB    42.3TB    7.7TB     84.6%
/var                     2.0TB     1.2TB     0.8TB     60.0%
/home                    5.0TB     3.1TB     1.9TB     62.0%

Cleaning History
Date                Time      Status    Space Freed   Duration
2024-01-15          14:32:10  Success   2.3TB         45m 22s
2024-01-14          02:15:45  Success   1.8TB         38m 10s
2024-01-13          14:20:33  Success   2.1TB         42m 55s
2024-01-12          02:10:22  Success   1.9TB         40m 18s
2024-01-11          14:05:11  Success   2.2TB         44m 33s
```

!!! warning "Common errors"
    **`filesys: command not found`** — Verify you are logged into the Data Domain management interface or SSH session with proper CLI access.
    **`Permission denied`** — Ensure your user account has administrative privileges; use `sysadmin` or equivalent privileged account.
### Space Reclaim Expectations

![Space Reclaim Expectations](../../../../assets/data-domain-proc-space-reclaim-expectations.svg)

| Dataset Size | Estimated Cleaning Duration |
|---|---|
| < 10 TB | 1–2 hours |
| 10–50 TB | 4–12 hours |
| > 50 TB | 12–24+ hours |

Cleaning can run concurrently with backup operations but will impact throughput. Schedule during off-peak windows when possible.

### When to Trigger Cleaning

![When to Trigger Cleaning](../../../../assets/data-domain-proc-when-to-trigger-cleaning.svg)

- After expiring a large backup policy
- After deleting old data manually
- When capacity is above 75% and not recovering naturally
- Before a capacity upgrade (to accurately assess current usage)

### Cleaning Troubleshooting

![Cleaning Troubleshooting](../../../../assets/data-domain-proc-cleaning-troubleshooting.svg)

```bash
# Cleaning not reclaiming space — confirm data is actually expired
# Check in backup application: are expired jobs marked as deleted?

# Cleaning status shows errors
log view | grep -i clean

# Cleaning taking too long
system show stats   # check if high I/O is causing slowdown
```


```text title="Expected output"
2024-01-15 14:32:18 UTC [INFO] Cleaning job started for tier-1-pool
2024-01-15 14:35:42 UTC [INFO] Cleaning phase 1: scanning metadata — 2.3TB processed
2024-01-15 14:38:15 UTC [WARN] Cleaning job paused — high I/O detected (read: 85%, write: 92%)
2024-01-15 14:40:22 UTC [ERROR] Cleaning job failed: insufficient free space in journal (required: 512MB, available: 128MB)
2024-01-15 14:42:01 UTC [INFO] Cleaning resumed after journal flush
2024-01-15 14:45:33 UTC [INFO] Cleaning completed — 847GB reclaimed from 12,450 expired objects

System Statistics:
  CPU Usage: 68%
  Memory Usage: 74% (18.2GB / 24GB)
  Disk I/O Read:  89%
  Disk I/O Write: 91%
  Network: 245Mbps ingress, 1.2Gbps egress
  Active Cleaning Jobs: 3
  Pending Cleaning: 2.1TB
```

!!! warning "Common errors"
    **`Cleaning job failed: insufficient free space in journal`** — Increase journal size or reduce concurrent cleaning jobs via `system set cleaning max-concurrent-jobs 1`.
    **`Cleaning phase 1: scanning metadata — timeout after 3600s`** — Extend cleaning timeout with `system set cleaning timeout 7200` or exclude large pools temporarily.
    **`Cleaning paused — high I/O detected`** — Schedule cleaning during off-peak hours using `system set cleaning schedule "02:00-06:00"` or reduce backup window overlap.
---

## Add a Replication Context (DD Boost)

```bash
# Add a DD Boost replication context from source MTree to target Data Domain
replication add source ddboost://<source-dd>/data/col1/<source-mtree> \
  destination ddboost://target-dd.example.com/data/col1/<target-mtree>

# Initialise the context — seeds the initial copy to the DR system
replication initialize ddboost://<source-dd>/data/col1/<source-mtree>

# Monitor initialisation progress
replication status
```


```text title="Expected output"
Adding replication context...
Source: ddboost://source-dd.example.com/data/col1/prod-mtree
Destination: ddboost://target-dd.example.com/data/col1/prod-mtree
Context added successfully. Context ID: ctx-7f2a9e1b

Initializing replication context...
Initialization started at 2024-01-15 14:32:18 UTC
Estimated time to completion: 4h 22m
Initial copy size: 2.3 TB

Replication Status:
Context ID          Source MTree              Status        Progress    Throughput
ctx-7f2a9e1b       prod-mtree                INITIALIZING  34%         185 MB/s
ctx-5d8c3f4a       backup-mtree              REPLICATING   100%        —
```

!!! warning "Common errors"
    **`Error: Invalid source path 'ddboost://<source-dd>/data/col1/<source-mtree>'`** — Replace `<source-dd>`, `<source-mtree>`, and `<target-mtree>` with actual hostnames and MTree names (e.g., `ddboost://dd-prod-01.example.com/data/col1/mtree01`).
    **`Error: Connection refused to target-dd.example.com:3009`** — Verify network connectivity and that DD Boost is enabled on the target Data Domain with `ddboost client show`.
    **`Error: Authentication failed for ddboost context`** — Ensure DD Boost credentials are configured on the source system using `ddboost client config` with valid username and password.
Monitor with `replication show all` until the context reports `Normal` state. Initial seeding time depends on dataset size and WAN bandwidth.

## Configure NFS Export

```bash
# Add an NFS export for the specified MTree, restricting access to a single client IP
nfs add /data/col1/<mtree> clients <client-IP> options ro,sec=sys

# To allow read-write access for a subnet
nfs add /data/col1/<mtree> clients <subnet>/<prefix> options rw,sec=sys

# Enable the NFS service if not already running
nfs enable

# Verify the export is listed
nfs show exports
```


```text title="Expected output"
NFS export added: /data/col1/archive01
NFS export added: /data/col1/archive01
NFS service enabled
NFS Exports:
  Export Path              Clients              Options
  /data/col1/archive01     192.168.10.50        ro,sec=sys
  /data/col1/archive01     10.20.0.0/24         rw,sec=sys
  /data/col1/backup02      10.50.100.0/25       rw,sec=sys
  /data/col1/restore       192.168.5.25         ro,sec=sys
```

!!! warning "Common errors"
    **`Error: MTree /data/col1/<mtree> does not exist`** — Verify the MTree name with `mtree show` and replace `<mtree>` with the actual MTree identifier.
    **`Error: NFS export already exists for /data/col1/<mtree>`** — Remove the existing export with `nfs delete /data/col1/<mtree>` before re-adding it with different options.
    **`Error: Invalid client IP/subnet format`** — Ensure the client IP is in dotted-decimal notation (e.g., 192.168.10.50) and subnet uses CIDR notation (e.g., 10.20.0.0/24).
Test the mount from the client:
```bash
mount -t nfs <dd-ip>:/data/col1/<mtree> /mnt/test
ls /mnt/test
```


```text title="Expected output"
total 48
drwxr-xr-x  12 root root  4096 Mar 15 10:23 .
drwxr-xr-x   3 root root  4096 Mar 15 09:45 ..
drwxr-xr-x   8 4294967294 4294967294 4096 Mar 14 16:52 backups
drwxr-xr-x   5 root root  4096 Mar 15 08:31 databases
-rw-r--r--   1 root root 2147483648 Mar 15 10:15 archive.tar.gz
drwxr-xr-x   3 root root  4096 Mar 13 22:41 logs
drwxr-xr-x   2 root root  4096 Mar 12 14:09 temp
```

!!! warning "Common errors"
    **`mount.nfs: mount to NFS server '<dd-ip>' failed: Connection refused`** — Verify the Data Domain IP is correct, the NFS service is running on the appliance, and network connectivity exists between the client and DD system.
    **`mount.nfs: access denied by server while mounting <dd-ip>:/data/col1/<mtree>`** — Confirm the export policy on the Data Domain allows NFS access from the client IP and that the mtree name is correct.
    **`No such file or directory`** — Ensure the mount point `/mnt/test` exists; create it with `mkdir -p /mnt/test` if needed.
## Configure CIFS Share

```bash
# Create a CIFS share pointing to the MTree
cifs share create <share-name> "<description>" /data/col1/<mtree>

# Enable the share
cifs share enable <share-name>

# Verify the share is listed
cifs share show
```


```text title="Expected output"
CIFS share '<share-name>' created successfully.
(no output — command completes silently)
Share Name                    Description                Status    Path
================================================================================
<share-name>                  <description>              enabled   /data/col1/<mtree>
backup_archive                Weekly backup storage      enabled   /data/col1/backup
reports_share                 Finance reports            enabled   /data/col1/reports
media_vault                    Media library access       enabled   /data/col1/media
```

!!! warning "Common errors"
    **`Error: Share '<share-name>' already exists`** — Use a unique share name or delete the existing share with `cifs share delete <share-name>` first.
    **`Error: Path '/data/col1/<mtree>' does not exist or is invalid`** — Verify the MTree exists with `mtree show` and confirm the path is correct.
    **`Error: CIFS service is not running`** — Start the CIFS service with `cifs service start` before creating shares.
Test access from a Windows client by mapping a drive to `\\<dd-hostname>\<share-name>` using an account with access. Confirm read/write as expected by the share permissions.

## Run Filesystem Cleaner

Run during a low-activity backup window to reclaim space without impacting throughput.

```bash
# Start an immediate cleaning cycle
filesys clean start

# Monitor progress in real time
filesys clean watch

# Check cleaning status at any time
filesys clean status
```


```text title="Expected output"
Starting immediate cleaning cycle...
Cleaning cycle initiated successfully. Cycle ID: CC-2024-01-15-0847
Cleaning started at: 2024-01-15 08:47:23 UTC

Cleaning in progress...
Phase: Metadata scan
Progress: 45%
Estimated time remaining: 12 minutes
Data processed: 2.3 TB
Garbage collected: 156 GB

Phase: Block consolidation
Progress: 78%
Estimated time remaining: 4 minutes
Data processed: 5.1 TB
Garbage collected: 412 GB

Cleaning cycle status:
Status: RUNNING
Cycle ID: CC-2024-01-15-0847
Start time: 2024-01-15 08:47:23 UTC
Current phase: Block consolidation
Progress: 78%
Estimated completion: 2024-01-15 09:01:15 UTC
Data freed so far: 412 GB
```

!!! warning "Common errors"
    **`filesys clean: command not found`** — Verify you are logged into the Data Domain CLI (via SSH or console) and have appropriate administrative privileges.
    **`Error: A cleaning cycle is already in progress. Cycle ID: CC-2024-01-15-0801`** — Wait for the current cycle to complete or use `filesys clean abort` to stop it before starting a new one.
    **`Error: Insufficient free space to start cleaning cycle`** — Ensure at least 5% of total capacity is available before initiating a new cleaning cycle.
Cleaning reclaims space from expired or deleted backup data. Run `filesys show space` before and after to confirm space was recovered. See also the [Filesystem Cleaning](#filesystem-cleaning) section for scheduling and troubleshooting.

## Change Replication Throttle

```bash
# Set a bandwidth limit in bytes per second (e.g. 50 MB/s = 52428800 bps)
replication throttle set 52428800

# View current throttle setting
replication throttle show

# Remove the throttle limit (full bandwidth)
replication throttle del
```


```text title="Expected output"
Throttle limit set to 52428800 bytes per second
Current replication throttle: 52428800 bps (50.00 MB/s)
Throttle limit removed - replication bandwidth unrestricted
```

!!! warning "Common errors"
    **`Error: Invalid throttle value. Must be between 1024 and 10737418240 bytes per second`** — Ensure the bandwidth value is within the valid range; 52428800 bps (50 MB/s) is acceptable, but values below 1 KB/s or above 10 GB/s will be rejected.
    **`Error: Replication in progress. Cannot modify throttle settings during active replication`** — Wait for the current replication job to complete before adjusting throttle settings, or use `replication status` to monitor progress.
Apply a throttle during business hours to protect production I/O from replication traffic. Remove or raise the limit during off-peak windows to reduce replication lag. Verify lag after any change with `replication show stats`.

## Expand Data Domain Capacity (DD Expansion Shelf)

1. Physically install the expansion shelf and connect the SAS cables per the Dell hardware installation guide
2. Power on the expansion shelf and wait for it to initialise
3. On the Data Domain, check that new disks are detected:
   ```bash
   disk show state
   ```
   New disks should appear as `Available`
4. Expand the filesystem to include the new capacity:
   ```bash
   filesys expand
   ```
5. Verify the expanded capacity is reflected in the usable pool:
   ```bash
   filesys show space
   ```
6. Update the CMDB with the new raw and usable capacity figures and close the change record

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Data Domain — Health Checks](../health-checks/)
- [Data Domain — CLI Reference](../cli-reference/)
- [Data Domain — Common Issues](../../troubleshooting/common-issues/)
