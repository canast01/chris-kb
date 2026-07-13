---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
description: "How to escalate Dell Data Domain (PowerProtect DD) issues to Dell Technologies support: what data to collect, how to generate the support bundle..."
---
# Dell Data Domain — Escalation

<div class="kb-summary">
How to escalate Dell Data Domain (PowerProtect DD) issues to Dell Technologies support: what data to collect, how to generate the support bundle, step-by-step case creation on dell.com/support, and the escalation path when progress stalls.

*Applies to: Dell Data Domain / PowerProtect DD running DDOS 7.x*
</div>
![Dell Data Domain — Escalation](../../../../../assets/storage-dell-data-domain-troubleshooting-escalation.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_case_on_dellcomsuppo: "How to Open the Case on dell.com/support" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_case_on_dellcomsuppo: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_case_on_dellcomsuppo -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** SSH to the Data Domain appliance as sysadmin; Dell support account at dell.com/support linked to the DD system serial number
- **AutoSupport configured:** if AutoSupport is enabled (`autosupport show`), Dell can receive the diagnostic bundle automatically. Use `autosupport send <case-number>` once the case is created to push the bundle directly to the case
- **Do NOT restart the filesystem** (`filesys enable`) on an offline filesystem without Dell guidance — the filesystem goes offline for a reason; forcing it back online without diagnosing the root cause can cause data corruption
- **Do NOT pull a disk** from a RAID-protected shelf without Dell identifying the exact failed drive — removing the wrong disk can push the RAID below its protection threshold and cause a second fault

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| DDOS version | `system show version` | Note full version string |
| Serial number | `system show serialno` | Note the DD serial (for case registration) |
| Filesystem status | `filesys status` | Filesystem: enabled, status: running |
| Active alerts | `alerts show current` | No critical alerts |
| Disk state | `disk show state` | No drives in FAILED or ABSENT state |
| Space usage | `filesys show space` | Used capacity below 80% of available |
| Replication state | `replication show` | All contexts in Normal state |
| AutoSupport status | `autosupport show` | Enabled; last send successful |
| Network status | `net show all` | All interfaces Up |

---

## Step-by-Step Data Collection

### 1. Get the system version and serial number

```bash
# SSH to the DD appliance as sysadmin
ssh sysadmin@<dd-ip>

# Full system information (version, model, serial)
system show

# DDOS version only
system show version

# Serial number (required for case registration)
system show serialno
```


```text title="Expected output"
sysadmin@dd-mgmt01.example.com's password: 
Last login: Wed Mar 15 14:22:31 UTC 2024 from 10.45.12.88

Data Domain OS (DDOS) 7.15.1.10
Copyright (c) 2024 Dell Technologies, Inc. All rights reserved.

dd-mgmt01> system show
System Information
  Model: DD9900
  Serial Number: DD-SN-A4F7K2M9X1
  DDOS Version: 7.15.1.10
  System Uptime: 45 days, 3 hours, 22 minutes
  Hostname: dd-mgmt01
  Management IP: 10.45.12.45

dd-mgmt01> system show version
DDOS Version: 7.15.1.10
Build: 7.15.1.10-20240301

dd-mgmt01> system show serialno
Serial Number: DD-SN-A4F7K2M9X1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ssh: connect to host <dd-ip> port 22: Connection timed out` | Verify the DD appliance IP is correct and reachable by pinging it first, then check firewall rules allow SSH on port 22. |
    | `Permission denied (publickey,password)` | Confirm the sysadmin account credentials are correct and that SSH key-based auth is not enforced; try using password authentication explicitly. |
    | `dd-mgmt01> system show: command not found` | Ensure you are in the DD CLI context (not a standard bash shell); type `exit` and reconnect, or verify the DD appliance is fully booted and responsive. |
### 2. Capture filesystem and capacity status

```bash
# Filesystem status (is it enabled and running?)
filesys status

# Capacity and space usage
filesys show space

# Deduplication ratio and compression stats
filesys show compression

# MTree list and per-MTree usage
mtree list
```


```text title="Expected output"
Filesystem Status: ENABLED
Filesystem State: RUNNING
Last Status Check: 2024-01-15 14:32:18 UTC

Filesystem Space Usage:
Total Capacity: 50.0 TB
Used Space: 38.2 TB
Available Space: 11.8 TB
Used Percentage: 76.4%

Compression Statistics:
Global Compression Ratio: 2.34:1
Deduplication Ratio: 3.12:1
Combined Efficiency: 7.28:1
Compressed Data Size: 5.24 TB
Uncompressed Data Size: 38.2 TB

MTree List and Usage:
Name                    Size        Used        Available   Quota
backup-prod             20.0 TB     18.5 TB     1.5 TB      20.0 TB
archive-2023            15.0 TB     12.1 TB     2.9 TB      15.0 TB
replication-staging     10.0 TB     7.6 TB      2.4 TB      10.0 TB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `filesys: command not found` | Verify you are logged into the Data Domain CLI (use `ssh admin@<dd-hostname>`) rather than the host shell. |
    | `Error: Filesystem is DISABLED` | Enable the filesystem with `filesys enable` and verify licensing is active. |
    | `Error: Cannot access MTree list - insufficient permissions` | Confirm your user account has admin or operator role using `user show`. |
### 3. Capture alert and event state

```bash
# All current (active) alerts
alerts show current

# Alert history (last 72 hours)
alerts show history

# System event log
log show syslog | tail -200
```


```text title="Expected output"
All current (active) alerts
================================================================================
Alert ID    Severity  Component        Message                          Timestamp
--------    --------  ---------        -------                          ---------
ALR-2847    WARNING   Replication      Replication lag detected         2024-01-15 14:32:18
ALR-2891    CRITICAL  Disk             Disk capacity threshold exceeded 2024-01-15 13:47:52
ALR-2756    INFO      Network          NTP sync lost on eth1            2024-01-15 12:15:33

Alert history (last 72 hours)
================================================================================
Alert ID    Severity  Component        Message                          Timestamp
--------    --------  ---------        -------                          ---------
ALR-2847    WARNING   Replication      Replication lag detected         2024-01-15 14:32:18
ALR-2891    CRITICAL  Disk             Disk capacity threshold exceeded 2024-01-15 13:47:52
ALR-2756    INFO      Network          NTP sync lost on eth1            2024-01-15 12:15:33
ALR-2701    WARNING   Memory           Memory utilization at 87%        2024-01-14 09:22:41
ALR-2645    INFO      Backup           Incremental backup completed     2024-01-13 23:18:05
...

System event log
Jan 15 14:32:18 dd-system-01 kernel: [replication] lag threshold exceeded: 4521 seconds
Jan 15 13:47:52 dd-system-01 mtree: [disk_monitor] capacity alert: /data1 at 94.2%
Jan 15 12:15:33 dd-system-01 ntpd: NTP synchronization lost on interface eth1
Jan 15 11:44:09 dd-system-01 replication: [sync_engine] checkpoint 847293 completed
Jan 15 10:33:21 dd-system-01 kernel: [memory] page cache reclaim triggered
Jan 15 09:18:47 dd-system-01 backup: [scheduler] daily backup job started (job_id: bkp-2847-dd01)
Jan 15 08:52:15 dd-system-01 network: [eth0] link status changed to UP
Jan 15 07:41:33 dd-system-01 syslog-ng: log rotation completed for /var/log/messages
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: alerts` | Verify you are logged into the Data Domain CLI (SSH to the management IP) and not a standard Linux shell. |
    | `Permission denied` | Ensure your user account has sufficient privileges; use `sysadmin` account or request elevated role access. |
### 4. Capture disk and hardware health

```bash
# Disk states (look for FAILED or ABSENT disks)
disk show state

# Physical disk locations and health
disk show hardware

# RAID reconstruction progress (if rebuilding after a drive failure)
disk show reconstruction
```


```text title="Expected output"
Disk State Summary:
Disk    State      Capacity    Used        Available   Health
disk.0  NORMAL     10.9TB      8.2TB       2.7TB       GOOD
disk.1  NORMAL     10.9TB      7.9TB       3.0TB       GOOD
disk.2  NORMAL     10.9TB      8.5TB       2.4TB       GOOD
disk.3  FAILED     10.9TB      N/A         N/A         BAD
disk.4  NORMAL     10.9TB      8.1TB       2.8TB       GOOD
disk.5  ABSENT     10.9TB      N/A         N/A         OFFLINE
...

Physical Disk Hardware Status:
Disk    Enclosure  Slot  Model              Serial         Temp(C)  Status
disk.0  ENC-1      0     DELL MD1400        6XN7K82        32       OK
disk.1  ENC-1      1     DELL MD1400        6XN7K83        31       OK
disk.2  ENC-1      2     DELL MD1400        6XN7K84        33       OK
disk.3  ENC-1      3     DELL MD1400        6XN7K85        FAILED   FAILED
disk.4  ENC-1      4     DELL MD1400        6XN7K86        32       OK
disk.5  ENC-1      5     DELL MD1400        6XN7K87        N/A      ABSENT
...

RAID Reconstruction Status:
Pool: pool-01
  RAID Group: rg-0
    Status: REBUILDING
    Progress: 45%
    Estimated Time Remaining: 2h 15m
    Failed Disk: disk.3
    Rebuild Rate: 850 MB/s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `disk show: command not found` | Verify you are logged into the Data Domain CLI (via SSH or console) and not a standard Linux shell; use `ssh admin@<dd-ip>` to connect. |
    | `Error: No disks detected` | Check that the storage enclosures are powered on and connected; run `system show hardware` to verify enclosure connectivity. |
    | `RAID reconstruction stalled at 45%` | Check system logs with `log show -filter 'RAID'` to identify I/O errors, and verify no additional disk failures occurred during rebuild. |
### 5. Capture replication status (if replication is involved)

```bash
# All replication contexts and their state
replication show

# Replication statistics (lag, bytes transferred)
replication status

# Per-context detail
replication show context=<context-name>
```


```text title="Expected output"
Replication Contexts:
  Context Name          State      Remote Host          Last Update
  prod-backup-01        ACTIVE     10.50.12.45          2024-01-15 14:32:18
  dr-sync-secondary     ACTIVE     192.168.100.88       2024-01-15 14:31:55
  archive-weekly        IDLE       10.50.12.200         2024-01-14 09:15:42
  test-repl-context    ERROR      10.50.13.5           2024-01-15 12:47:03

Replication Statistics:
  Context Name          Lag (sec)  Bytes Transferred    Status
  prod-backup-01        45         2.3 TB               In Progress
  dr-sync-secondary     12         5.8 TB               Completed
  archive-weekly        0          1.2 TB               Idle
  test-repl-context    N/A        0 B                  Failed

Context: prod-backup-01
  State: ACTIVE
  Remote Host: 10.50.12.45
  Remote Port: 7144
  Bandwidth Limit: 100 Mbps
  Last Successful Sync: 2024-01-15 14:32:18
  Bytes Pending: 512 MB
  Estimated Time to Sync: 41 seconds
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `replication: command not found` | Ensure you are logged into the Data Domain CLI (via SSH or console) and have appropriate admin privileges. |
    | `Error: context '<context-name>' does not exist` | Verify the exact context name using `replication show` and check for typos or spaces in the context name. |
    | `Error: replication service is not running` | Restart the replication service with `replication restart` or contact Dell support if the service fails to start. |
### 6. Generate the support bundle

```bash
# Generate a local support bundle (saved to /ddr/var/support/)
support bundle generate

# Find the bundle
ls -lh /ddr/var/support/

# If AutoSupport is configured and a case number is available:
# Send bundle directly to the Dell case (preferred — no manual upload needed)
autosupport send <case-number>

# Otherwise, SCP the bundle to your workstation for manual upload
# scp sysadmin@<dd-ip>:/ddr/var/support/<bundle-file>.tar /tmp/
```


```text title="Expected output"
Generating support bundle...
Bundle generation completed successfully.
Bundle file: ddve-support-20250114-143022.tar.gz

total 1.2G
-rw-r--r-- 1 root root 1.2G Jan 14 10:30 ddve-support-20250114-143022.tar.gz
-rw-r--r-- 1 root root 892M Jan 13 09:15 ddve-support-20250113-091547.tar.gz
-rw-r--r-- 1 root root 1.1G Jan 12 14:22 ddve-support-20250112-142201.tar.gz

AutoSupport case number not configured or case <case-number> not found.
Proceeding with manual bundle transfer.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `support bundle generate: command not found` | Verify you are logged into the Data Domain CLI (not the Linux shell); use `ssh sysadmin@<dd-ip>` to access the DD OS prompt. |
    | `autosupport send: case number invalid or AutoSupport not configured` | Confirm the case number format and that AutoSupport is enabled via `autosupport show`; if unconfigured, skip to manual SCP transfer. |
    | `scp: Permission denied (publickey,password)` | Ensure SSH key is installed on the Data Domain or add `-u sysadmin` flag and provide the password when prompted. |
### 7. Write the timeline

```text
Data Domain model: DD9400
DDOS version: 7.10.1.0-653009
Serial number: XXXXXXXX
Configuration: DD9400 (source) → DD6400 (replication target, site B)
Backup clients: NetWorker 19.9 (30 hosts), Commvault 11.26 (15 hosts)
Issue first observed: 2026-06-15 09:00 UTC
Last confirmed healthy: 2026-06-15 07:00 UTC
Changes in 24h before the issue:
  - 07:00: DDOS upgrade from 7.10.0 to 7.10.1 completed
  - 09:00: filesys status shows "Filesystem: disabled, status: offline"
  - 09:05: alerts show current: "ALERT-003: Filesystem is offline — disk 3.7 reported unreadable sector"
SupportAssist: enabled; autosupport configured; case not yet created
Steps already taken:
  - Did NOT run filesys enable (awaiting Dell guidance)
  - Did NOT pull disk 3.7 (awaiting Dell identification of correct disk)
  - Replication to site B: context in Initializing (stopped when filesys went offline)
Blast radius: All backup jobs failing; cannot write new backups; DR copy stale since 09:00 UTC
```

---

## How to Open the Case on dell.com/support

1. Go to **dell.com/support** and sign in with your Dell account.

2. Click **My Cases** → **Create New Case**.

3. Under **Product**, enter the Data Domain serial number from Step 1. Select **Dell PowerProtect DD** or **Dell Data Domain** as the product family.

4. Under **Severity**, select:
   - **Severity 1 — Production Down**: Filesystem is offline; no backups can be written or read; replication has stopped; no workaround; backup SLA breach in progress
   - **Severity 2 — Degraded**: Filesystem accessible but approaching capacity; replication lagging > 4 hours; a drive is failed and RAID rebuild has not started; workaround is partial
   - **Severity 3 — Non-Critical**: Single alert; specific protocol issue (NFS/CIFS/DDBoost for one client); replication minor lag; workaround exists
   - **Severity 4 — General**: How-to, upgrade planning, capacity planning, protocol configuration question

5. In the **Summary** field: symptom + scope. Example: `Data Domain DD9400 — filesystem offline since 09:00 UTC after DDOS upgrade, all backup clients failing, disk 3.7 unreadable sector alert`.

6. In the **Description** field, paste:
   - DDOS version and serial number from Step 1
   - `filesys status` and `alerts show current` output
   - Disk state from Step 4
   - The timeline from Step 7

7. Under **Attachments**, upload the support bundle from Step 6 (or use `autosupport send <case-number>` to push it directly to the case).

8. Click **Submit**. You receive a case number immediately.

9. **Severity 1 only:** call Dell support after submission:
    - North America: +1 800 945 3355 (24×7 for production-down)
    - State "Severity 1 — Data Domain filesystem offline, all backup jobs failing, case XXXXXXXX" at the start of the call.

---

## Escalation Path

![Dell Data Domain — Escalation — Diagram](../../../../../assets/storage-dell-data-domain-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Run `filesys enable` on an offline filesystem without Dell guidance | The filesystem goes offline to protect data integrity; forcing it online without knowing the root cause can trigger additional disk errors or corruption | Let Dell review the alert and disk state before any filesystem restart |
| Pull a drive that is showing errors without Dell confirming the correct drive | Removing an incorrectly identified drive in a RAID-6 group can add a second fault and push the array below its protection threshold | Let Dell identify the exact failed drive from the support bundle before any physical removal |
| Disable filesystem cleaning during the investigation | Disabling cleaning allows garbage to accumulate; if capacity fills, the filesystem goes offline | Only disable cleaning if Dell explicitly instructs, and only for a defined time window |
| Restart replication without Dell guidance when the filesystem is offline | Restarting replication on a filesystem that is offline or in an inconsistent state can cause the replication context to enter an Initializing loop | Let Dell restore the filesystem first, then confirm replication restart is safe |
| Upgrade DDOS again immediately after a failed upgrade | A second upgrade on a partially failed state can push the DDOS into an inconsistent version | Let Dell review the upgrade log and the current filesystem state before any retry |
| Delete backup data to free space during a capacity emergency | Deleting backup data may cause the cleaning process to behave unexpectedly and the freed space may not be immediately reclaimed | Engage Dell to assess whether space reclamation can be accelerated safely |

---

## Useful Commands for Case Updates

```bash
# SSH to Data Domain as sysadmin — paste into every case update

# System version and serial
system show

# Filesystem status
filesys status

# Active alerts
alerts show current

# Disk health
disk show state

# Space usage
filesys show space

# Replication state
replication show
```


```text title="Expected output"
System Information
  Model: Dell EMC Data Domain DD3300
  Serial Number: DD3300-001A2B3C4D5E
  System Version: 7.15.1.10
  Uptime: 45 days 12 hours 23 minutes

Filesystem Status
  /data: HEALTHY
  /var: HEALTHY
  /boot: HEALTHY

Current Alerts
  Alert ID: 1847 | Severity: WARNING | Message: Disk 3.4 predictive failure detected
  Alert ID: 1846 | Severity: INFO | Message: Replication lag detected on peer-dd3300-02

Disk State
  Disk 1.1: HEALTHY (1.8TB)
  Disk 1.2: HEALTHY (1.8TB)
  Disk 2.1: HEALTHY (1.8TB)
  Disk 3.4: PREDICTIVE_FAILURE (1.8TB)
  Disk 4.1: HEALTHY (1.8TB)

Filesystem Space Usage
  /data: 78% used (3.5TB of 4.5TB)
  /var: 42% used (210GB of 500GB)
  /boot: 15% used (1.2GB of 8GB)

Replication Status
  Peer: peer-dd3300-02 | Status: LAGGING | Last Sync: 2 hours 47 minutes ago
  Peer: peer-dd3300-03 | Status: IN_SYNC | Last Sync: 3 minutes ago
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Authentication failed` | Verify sysadmin credentials and that SSH key-based auth is configured, or use `ssh -l admin` with password prompt. |
    | `Error: Command not found` | Ensure you are in the Data Domain CLI (not bash shell); exit bash with `exit` and reconnect via SSH. |
    | `Error: Insufficient privileges for this command` | Confirm you are logged in as sysadmin user; use `whoami` to verify and reconnect if needed. |
---

## Support SLA Reference

| Tier | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | Filesystem offline; no backups possible; data at risk | < 2 hours (24×7) |
| ProSupport Plus | P2 — Degraded | Capacity critical; drive failed; replication lagging | < 4 hours (24×7) |
| ProSupport Plus | P3 — Non-Critical | Single protocol issue; minor alert; workaround exists | Next business day |
| ProSupport Plus | P4 — General | How-to, planning, protocol configuration | Next business day |
| ProSupport | P1 | As above | < 4 hours (24×7) |

---

## See also

- [Data Domain — Diagnostics](../diagnostics/)
- [Data Domain — Common Issues](../common-issues/)

---

## Verify resolution

- Run `filesys status` and confirm the filesystem shows `enabled, status: running`
- Run `alerts show current` and confirm no active critical or error alerts
- Run `disk show state` and confirm no drives are in FAILED or ABSENT state
- Run `filesys show space` and confirm capacity is below 80% used
- Run `replication show` and confirm all replication contexts show Normal state and lag is below RPO
- Confirm backup clients can connect and write: run a test backup job from one client and confirm it completes
- Run `autosupport send` to close the diagnostic loop with Dell and attach post-resolution state
- Monitor `alerts show current` for 15 minutes to confirm no new alerts appear
