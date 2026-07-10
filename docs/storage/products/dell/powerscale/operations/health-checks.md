---
tags:
  - dell
  - operations
---
# PowerScale — Health Checks

<div class="kb-summary">
Health Checks reference covering Daily Checks, Health Check, Cluster Health Commands, Health Check Summary.

*Applies to: PowerScale (Isilon) 9.x*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Cluster health:** `isi status` — all nodes should show status Healthy
2. **Quota status:** `isi quota quotas list --format=table` — check near-threshold quotas
3. **SyncIQ replication:** `isi sync reports list` — check last sync success/failure
4. **SmartPools:** `isi storagepool nodepools list` — verify tier assignments
5. **Disk status:** `isi devices drive list` — all drives Healthy
6. **Network interfaces:** `isi network interfaces list` — all Up
7. **Active alerts:** `isi events list --is_alertable=true --resolved=false`

## Daily Checks

![Daily Checks](../../../../../assets/storage-dell-powerscale-hc-daily-checks.svg)

![Daily Checks](../../../../../assets/storage-dell-powerscale-hc-daily-checks.svg)

```d2
direction: right

A: "Daily Health Check" {shape: rectangle}
B: "isi status\nAll nodes ONLINE?" {shape: rectangle}
C: "SMARTFAIL\nor DOWN node?" {shape: rectangle}
D: "Do NOT remove manually\nMonitor Restripe job\nOpen Dell support case" {shape: rectangle}
E: "isi storagepool list\nCapacity < 80%?" {shape: rectangle}
F: "Pool > 80%?" {shape: rectangle}
G: "Identify top consumers\nisi quota quotas list\nPlan expansion or cleanup" {shape: rectangle}
H: "isi sync policies list\nSyncIQ all SUCCESS?" {shape: rectangle}
I: "Policy FAILED\nor OVERDUE?" {shape: rectangle}
J: "isi sync reports list\nInvestigate error\nRestart if needed" {shape: rectangle}
K: "isi event list --limit 20\nCRITICAL events?" {shape: rectangle}
L: "Unack" {shape: rectangle}
M: "Triage event code\nEscalate if hardware" {shape: rectangle}
N: "Checks passed" {shape: rectangle}

A -> B
B -> C
C -> D
C -> E
E -> F
F -> G
F -> H
H -> I
I -> J
I -> K
K -> L
L -> M
L -> N
D -> G
G -> J
J -> M
M -> N
```

| Check | Command | Notes |
|---|---|---|
| [ ] Run `isi status` | `isi status` | confirm all nodes show `ONLINE` and no node is in `SMARTFAIL` or `DOWN` state; note any drive alerts |
| [ ] Run `isi job list` | `isi job list` | confirm no active cluster jobs are in `ERROR` or `PAUSED` state; note unusually long-running Restripe or MultiScan jobs |
| [ ] Check SyncIQ policies | `isi sync policies list` | confirm each policy shows `Last Success` with a timestamp within the expected RPO window |
| [ ] Review recent events | `isi event list --limit 20` | triage any CRITICAL or ERROR severity events |
| [ ] Check storage pool capacity | `isi storagepool list` | alert if any pool or tier exceeds 80% used |
| [ ] Check SmartQuota violations | `isi quota quotas list` | look for directories that have exceeded soft or hard thresholds |
| [ ] Review InsightIQ or CloudIQ for performance anomalies |  | flag any node with sustained CPU utilisation above 85% or latency spikes |
| [ ] Confirm SyncIQ RPO compliance by checking `isi sync reports list` | `isi sync reports list --limit 5` |  |

## Health Check

![Health Check](../../../../../assets/storage-dell-powerscale-hc-health-check.svg)

![Health Check](../../../../../assets/storage-dell-powerscale-hc-health-check.svg)

Run these checks before any maintenance or change, or as first steps when investigating a reported issue.

- [ ] `isi status` — cluster health summary, node states, and drive health are all clean (no SMARTFAIL, no DOWN, no drive faults)
- [ ] `isi storagepool list` — all pools and tiers are below 80% used; confirm SmartPool tiering policies are active
- [ ] `isi job list` — no jobs in ERROR or unexpectedly PAUSED; note any job running longer than its typical duration
- [ ] `isi sync reports list --limit 5` — most recent SyncIQ reports for all policies show SUCCESS; check for policies with repeated failures
- [ ] `isi event list` — no unacknowledged CRITICAL events in the last 24 hours
- [ ] `isi license list` — all required licenses (SmartQuotas, SyncIQ, SmartPools, SnapshotIQ) are valid and not near expiry
- [ ] `isi network subnets list` — SmartConnect zones are configured correctly and DNS delegation is in place
- [ ] `isi statistics query current --keys CPU` — no individual nodes showing sustained CPU saturation

```bash
# Overall cluster node and drive health summary
isi status

# List all storage pool tiers and their capacity usage
isi storagepool list

# List active and recent cluster background jobs
isi job list

# List SyncIQ policies and their last run status
isi sync policies list

# Show the 5 most recent SyncIQ replication reports
isi sync reports list --limit 5

# List all cluster events (triage CRITICAL severity first)
isi event list --limit 20

# List all SmartQuota entries including directories near threshold
isi quota quotas list

# Query current per-node CPU utilisation
isi statistics query current --keys CPU

# Show installed OneFS version and license status
isi license list
```


```text title="Expected output"
Cluster Information
  Cluster Name: powerscale-prod-01
  Nodes: 6
  Node Status: All nodes online
  Drive Status: All drives healthy
  Cluster Health: Good

Storage Pool: Tier_SSD_NVMe
  Capacity: 50.2 TB
  Used: 38.7 TB (77%)
  Available: 11.5 TB

Storage Pool: Tier_SAS_7.2K
  Capacity: 200.8 TB
  Used: 156.3 TB (78%)
  Available: 44.5 TB

Job ID: job-2024-01-15-0847
  Type: Rebalance
  Status: Running
  Progress: 62%

Job ID: job-2024-01-14-2301
  Type: Backup
  Status: Completed
  Duration: 4h 23m

Policy Name: sync-to-dr-site
  Last Run: 2024-01-15 06:30:00
  Status: Success
  Next Run: 2024-01-15 18:30:00

Report ID: sync-report-20240115-0630
  Policy: sync-to-dr-site
  Duration: 18m 42s
  Files Synced: 1,247,893
  Status: Completed

Event ID: evt-20240115-1402
  Severity: CRITICAL
  Message: Node-4 disk /dev/sda1 temperature warning
  Timestamp: 2024-01-15 14:02:33

Event ID: evt-20240115-1245
  Severity: WARNING
  Message: Cluster rebalance in progress
  Timestamp: 2024-01-15 12:45:18

Quota Name: /ifs/data/projects
  Hard Limit: 100 GB
  Used: 87.3 GB (87%)
  Status: Warning

Quota Name: /ifs/data/archive
  Hard Limit: 500 GB
  Used: 412.1 GB (82%)
  Status: OK

Node-1 CPU: 34%
Node-2 CPU: 28%
Node-3 CPU: 41%
Node-4 CPU: 52%
Node-5 CPU: 31%
Node-6 CPU: 27%

OneFS Version: 9.7.0.0
License Status: Valid
License Expiration: 2025-06-30
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the Isilon OneFS CLI tools are installed and the PATH includes the OneFS bin directory (typically `/usr/local/bin` or part of the OneFS SDK).
    **`Connection refused on 127.0.0.1:8080`** — Verify the OneFS management API service is running and accessible; check network connectivity to the cluster management IP and confirm firewall rules allow access.
    **`Authentication failed: Invalid credentials`** — Verify your OneFS admin credentials are correct and that your user account has sufficient privileges; re-authenticate using `isi auth login` if needed.
## Cluster Health Commands

![Cluster Health Commands](../../../../../assets/storage-dell-powerscale-hc-cluster-health-commands.svg)

![Cluster Health Commands](../../../../../assets/storage-dell-powerscale-hc-cluster-health-commands.svg)

```bash
# Cluster identity, version, and status
isi version
isi status
isi cluster identity view

# Node count and status summary
isi node list
isi status -n all   # Per-node health summary
```


```text title="Expected output"
OneFS 9.4.0.0 (Build 9.4.0.0_1_20230815_084532)
Cluster is in good health.
Cluster Name: prod-isilon-01
Cluster UUID: 550e8400-e29b-41d4-a716-446655440000
Nodes: 6
Protection Policy: +2d:1n
Encoding: Reed-Solomon 6+2

Node  LNN  Status  Contact  Uptime
1     1    Up      Yes      45d 3h 22m
2     2    Up      Yes      45d 3h 21m
3     3    Up      Yes      45d 3h 20m
4     4    Up      Yes      44d 18h 15m
5     5    Up      Yes      44d 18h 14m
6     6    Up      Yes      44d 18h 13m

Node  Status  CPU   Memory  Disk
1     Up      18%   62%     71%
2     Up      22%   58%     71%
3     Up      19%   61%     70%
4     Up      25%   65%     72%
5     Up      21%   63%     71%
6     Up      20%   64%     71%
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the PATH includes `/usr/bin` or `/opt/isilon/bin`.
    **`Error: Unable to connect to cluster`** — Verify network connectivity to the cluster management IP and that SSH/HTTPS access is permitted on port 22 or 8080.
### Node Health

![Node Health](../../../../../assets/storage-dell-powerscale-hc-node-health.svg)

```bash
# List all nodes with status
isi node list

# Detailed view of a specific node
isi node view <node_id>

# Node hardware sensors (temperature, fans, power)
isi node sensors view <node_id>

# Node drives — check for failed or degraded drives
isi node drives list <node_id>
isi node drives list <node_id> | grep -iE "failed|degraded|missing"
```


```text title="Expected output"
isi node list
ID  Name              Status  Lnn  Roles
1   isilon-node-001   Online  1    Coordinator
2   isilon-node-002   Online  2    Node
3   isilon-node-003   Online  3    Node
4   isilon-node-004   Offline 4    Node

isi node view 1
Node ID:                1
Node Name:              isilon-node-001
Status:                 Online
Logical Node Number:    1
Hardware Platform:      NL400
Serial Number:          AKSD8F7G9H2J1K3L
Uptime:                 45 days 12 hours
Firmware Version:       9.4.0.0

isi node sensors view 1
Node 1 - isilon-node-001
Temperature Sensors:
  CPU0 Temp:           62°C (Normal)
  CPU1 Temp:           58°C (Normal)
  System Inlet:        28°C (Normal)
Fan Sensors:
  Fan Module 1:        4200 RPM (Normal)
  Fan Module 2:        4150 RPM (Normal)
Power Supplies:
  PSU 1:               OK
  PSU 2:               OK

isi node drives list 1
Node 1 - isilon-node-001
Bay  Serial          Model              Status    Capacity
1    SN8F4K2L9X1M    SEAGATE IronWolf   Online    12.0 TB
2    SN7G3J1K8W2N    SEAGATE IronWolf   Online    12.0 TB
3    SN6H2I0J7V3O    SEAGATE IronWolf   Online    12.0 TB
4    SN5D1H9I6U4P    SEAGATE IronWolf   Degraded  12.0 TB
5    SN4C0G8H5T5Q    SEAGATE IronWolf   Online    12.0 TB

isi node drives list 1 | grep -iE "failed|degraded|missing"
4    SN5D1H9I6U4P    SEAGATE IronWolf   Degraded  12.0 TB
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the isilon package is in your PATH, or run commands from the cluster management interface.
    **`Error: Invalid node ID '<node_id>'`** — Replace `<node_id>` with an actual numeric node ID from the output of `isi node list`.
    **`Error: Node <node_id> is unreachable or offline`** — Verify network connectivity to the node and check cluster status with `isi status` before querying individual nodes.
### Active Events and Alerts

![Active Events and Alerts](../../../../../assets/storage-dell-powerscale-hc-active-events-and-alerts.svg)

```bash
# All unresolved critical events
isi event events list --severity critical

# All unresolved events (all severities)
isi event events list

# Events from the last 24 hours
isi event events list --start-time $(date -d 'yesterday' '+%Y-%m-%d')

# Alert channels configured
isi event channels list
```


```text title="Expected output"
ID                                   Severity  Event Type              Node      Time                    Message
12a4b5c6-7d8e-9f0a-1b2c-3d4e5f6a7b8c CRITICAL  Node_Down               node-3    2024-01-15T14:32:18Z    Node 3 is offline
23b5c6d7-8e9f-0a1b-2c3d-4e5f-6a7b8c9 CRITICAL  Disk_Failure            node-1    2024-01-15T13:45:22Z    Disk /dev/sdb failed on node-1
34c6d7e8-9f0a-1b2c-3d4e-5f6a7b8c9d0e CRITICAL  Replication_Lag         node-2    2024-01-15T12:18:05Z    Replication lag exceeded threshold
...

ID                                   Severity  Event Type              Node      Time                    Message
12a4b5c6-7d8e-9f0a-1b2c-3d4e5f6a7b8c CRITICAL  Node_Down               node-3    2024-01-15T14:32:18Z    Node 3 is offline
23b5c6d7-8e9f-0a1b-2c3d-4e5f-6a7b8c9 CRITICAL  Disk_Failure            node-1    2024-01-15T13:45:22Z    Disk /dev/sdb failed on node-1
45d7e8f9-0a1b-2c3d-4e5f-6a7b8c9d0e1f WARNING   High_Memory_Usage       node-4    2024-01-15T11:22:33Z    Memory usage at 87%
56e8f9a0-1b2c-3d4e-5f6a-7b8c9d0e1f2g INFO      Snapshot_Complete       node-2    2024-01-15T10:15:44Z    Snapshot job_20240115_001 completed
...

ID                                   Severity  Event Type              Node      Time                    Message
23b5c6d7-8e9f-0a1b-2c3d-4e5f-6a7b8c9 CRITICAL  Disk_Failure            node-1    2024-01-14T18:45:22Z    Disk /dev/sdb failed on node-1
45d7e8f9-0a1b-2c3d-4e5f-6a7b8c9d0e1f WARNING   High_Memory_Usage       node-4    2024-01-14T16:22:33Z    Memory usage at 87%
56e8f9a0-1b2c-3d4e-5f6a-7b8c9d0e1f2g INFO      Snapshot_Complete       node-2    2024-01-14T09:15:44Z    Snapshot job_20240114_005 completed

Name              Type        Enabled  Address                 Port
email-alerts      SMTP        true     smtp.corp.local         25
```
### Cluster Capacity

![Cluster Capacity](../../../../../assets/storage-dell-powerscale-hc-cluster-capacity.svg)

```bash
# Overall used vs. free capacity
isi statistics system list | grep -E "Cluster Capacity|Used|Free"

# Storage pool capacity breakdown
isi storagepool nodepools list
isi storagepool tiers list

# SmartQuotas — total quota usage
isi quota quotas list --type directory | head -20
```


```text title="Expected output"
Cluster Capacity: 1.2 PB
Used: 847.3 TB
Free: 389.7 TB

ID          Name            Node Count  Status
------      ----            ----------  ------
1           pool-ssd-tier1  4           Online
2           pool-hdd-tier2  8           Online
3           pool-nvme-hot   2           Online

Tier ID     Tier Name       Capacity    Used        Free
-------     ---------       --------    ----        ----
1           SSD             200 TB      156.2 TB    43.8 TB
2           HDD             900 TB      678.1 TB    221.9 TB
3           NVMe            100 TB      13 TB       87 TB

Path                                    Hard Quota  Used        % Used
----                                    ----------  ----        ------
/ifs/projects/analytics               500 GB       487.2 GB    97.4%
/ifs/projects/backup_archive           2 TB        1.8 TB      90.0%
/ifs/data/shared_media                 1.5 TB      1.2 TB      80.0%
/ifs/home/engineering_team             750 GB      612.5 GB    81.7%
/ifs/archive/legacy_data                3 TB        2.1 TB      70.0%
...
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the PATH includes the OneFS bin directory, or run commands directly on the cluster management interface.
    **`Error: Invalid credentials or insufficient permissions`** — Verify your OneFS admin account has appropriate role permissions (typically "Cluster Admin") and re-authenticate if your session has expired.
### Protocol Services

![Protocol Services](../../../../../assets/storage-dell-powerscale-hc-protocol-services.svg)

```bash
# NFS service status
isi services -a | grep nfs

# SMB service status
isi services -a | grep smb

# All running services
isi services -a | grep running
```


```text title="Expected output"
nfs                                    running
smb                                    running
hdfs                                   running
s3                                     running
isi_hw_poll                            running
isi_ibm_config                         running
isi_nfs_d                              running
isi_smb_server                         running
isi_quota_d                            running
isi_eventd                             running
...
```

!!! warning "Common errors"
    **`command not found: isi`** — Ensure you are logged into the PowerScale cluster via SSH or the platform API, as the `isi` command is only available on cluster nodes.
    **`Permission denied`** — Run the command with appropriate cluster admin credentials; standard user accounts may lack permission to query service status.
### SyncIQ Replication

![SyncIQ Replication](../../../../../assets/storage-dell-powerscale-hc-synciq-replication.svg)

```bash
# Policy status
isi sync policies list
isi sync policies view <policy_name>

# Last job result for each policy
isi sync jobs list --state finished | head -10

# Check for failed replication jobs
isi sync jobs list --state failed
isi sync jobs list --state paused
```


```text title="Expected output"
Name                          Enabled  Description
----                          -------  -----------
daily_backup_chicago          True     Daily sync to Chicago DR site
hourly_sync_london            True     Hourly replication to London
weekly_archive_s3             False    Weekly archive to S3 bucket
nightly_compliance_backup     True     Nightly compliance data sync

Policy: daily_backup_chicago
  Enabled: True
  Source: /ifs/data/production
  Target: 10.45.12.8:/ifs/dr
  Schedule: 0 2 * * *
  Last Run: 2024-01-15T02:15:33Z
  Status: Success

ID       Policy Name               State      Start Time              Duration  Files
----     -----------               -----      ----------              --------  -----
4521     daily_backup_chicago      finished   2024-01-15T02:15:33Z   847s      125430
4520     hourly_sync_london        finished   2024-01-15T02:00:12Z   312s      89234
4519     weekly_archive_s3         finished   2024-01-14T23:45:01Z   1205s     234567
4518     nightly_compliance_backup finished   2024-01-15T01:30:44Z   523s      45678
4517     daily_backup_chicago      finished   2024-01-14T02:10:15Z   891s      128945

(no output — no failed jobs currently)

ID       Policy Name               State      Start Time              Duration  Files
----     -----------               -----      ----------              --------  -----
4516     hourly_sync_london        paused     2024-01-15T01:45:22Z   180s      12340
```

!!! warning "Common errors"
    **`Error: Policy '<policy_name>' not found`** — Verify the policy name with `isi sync policies list` and use the exact name from the Name column.
    **`Error: Invalid state value. Valid states are: running, finished, failed, paused, skipped`** — Use only the documented state keywords; check `isi sync jobs list --help` for valid options.
### Jobs (Background Tasks)

![Jobs (Background Tasks)](../../../../../assets/storage-dell-powerscale-hc-jobs-background-tasks.svg)

```bash
# Currently running jobs
isi job status

# Any job in error state
isi job jobs list | grep -i error

# FlexProtect status (data protection rebuild)
isi job jobs list | grep -i "FlexProtect\|Repair"
```


```text title="Expected output"
Job ID                                    Job Type                Status      Progress
1                                         SmartPools              Running     45%
2                                         SnapshotDelete          Completed   100%
3                                         Rebalance               Running     78%
4                                         SyncIQ                  Running     12%
5                                         Dedupe                  Completed   100%

(no output — no jobs in error state)

Job ID                                    Job Type                Status      Progress
7                                         FlexProtect             Running     62%
8                                         Repair                  Completed   100%
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the `isi` binary is in your PATH, or run commands from the cluster management node.
    **`Error: Invalid credentials`** — Verify you have authenticated to the cluster with `isi auth login` or check that your SSH key is properly configured for the admin user.
    **`Error: Connection refused on 127.0.0.1:8080`** — Confirm the cluster is reachable and the OneFS API service is running; try pinging the cluster management IP address.
## Health Check Summary

![Health Check Summary](../../../../../assets/storage-dell-powerscale-hc-health-check-summary.svg)

![Health Check Summary](../../../../../assets/storage-dell-powerscale-hc-health-check-summary.svg)

| Check | Command | Healthy |
|---|---|---|
| All nodes online | `isi node list` | All = online |
| No critical events | `isi event events list --severity critical` | 0 events |
| Capacity < 80% | `isi statistics system list` | Used < 80% |
| NFS/SMB services running | `isi services -a` | Both running |
| SyncIQ policies healthy | `isi sync policies list` | All enabled, last job success |
| No jobs in error | `isi job jobs list` | 0 errors |
| No failed drives | `isi node drives list` | 0 failed/degraded |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerscale — Procedures](../procedures/)
- [Powerscale — CLI Reference](../cli-reference/)
- [Powerscale — Common Issues](../../troubleshooting/common-issues/)
