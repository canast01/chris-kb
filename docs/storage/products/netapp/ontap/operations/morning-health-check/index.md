---
tags:
  - netapp
  - ontap
  - health-checks
  - operations
search:
  boost: 2
---
# ONTAP Morning Health-Check Runbook

<div class="kb-summary">
Daily ONTAP cluster health-check sequence — takes ~10 minutes. Run this every morning before starting any operational work.
</div>

```d2
direction: down

run_this_routine: "Run This Routine" {shape: rectangle}
health_thresholds: "Health Thresholds" {shape: rectangle}

run_this_routine -> health_thresholds: uses
```

## Before you begin

**Prerequisites:**

- ONTAP CLI access — SSH to the cluster management LIF or use `system node run`
- Credentials with at least `readonly` cluster role (admin role for full access)
- Know your cluster name and node names (`cluster show` confirms both)
- No active non-disruptive upgrade (NDU) or takeover in progress — check with `storage failover show` first

**Timing:** Safe to run during business hours. None of these commands are disruptive. Capture output to your change log.

---

## Run This Routine

Work through steps 1–11 in order. Each command takes seconds. Flag any output that does not match the expected result before moving to the next step.

**Step 1 — Verify all nodes are healthy**

```bash
cluster show
```


```text title="Expected output"
Cluster                     Health  Eligibility
-----------                 ------  -----------
cluster-prod-01             true    true
cluster-dr-02               true    true
cluster-test-03             true    false
3 entries were displayed.
```

!!! warning "Common errors"
    **`Error: command not found: cluster`** — Ensure you are connected to the ONTAP cluster via SSH or the ONTAP CLI, not your local shell.
    **`Error: Access denied for command "cluster show"`** — Verify your ONTAP user account has the appropriate RBAC role assigned (e.g., admin or read-only).
Expected output: every node shows `true` in the Health column and `false` in the Epsilon column (one node may hold Epsilon — that is normal). Any node showing `false` for Health blocks the rest of the routine.

---

**Step 2 — Overall health subsystem status**

```bash
system health status show
```


```text title="Expected output"
Status
------
ok

Component Details:
  System State: normal
  System Health: normal
  Subsystem Health:
    storage: normal
    cpu: normal
    memory: normal
    nvram: normal
    fan: normal
    power-supply: normal
    temperature: normal
    disk: normal
    network: normal
```

!!! warning "Common errors"
    **`Error: command not found`** — Ensure you are logged into the ONTAP cluster CLI (via SSH or console) and not a Linux shell.
    **`Error: Access denied for command: system health status show`** — Verify your user role has sufficient privileges; request admin or operator role access from your cluster administrator.
Expected output: `Status: ok`. Any other status (`degraded`, `warning`) means a subsystem has an active alert — proceed to step 3 immediately.

---

**Step 3 — Active health alerts**

```bash
system health alert show
```


```text title="Expected output"
Alert ID: 1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p
  Severity:       critical
  Probable Cause: Disk shelf temperature sensor failure on shelf 1.2
  Description:    Temperature sensor on disk shelf 1.2 has failed
  Corrective Action: Replace the temperature sensor module
  Triggered On:   2024-01-15 14:32:18 +00:00

Alert ID: 2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q
  Severity:       warning
  Probable Cause: Aggregate aggr_ssd_01 is 89% full
  Description:    Aggregate capacity utilization is above threshold
  Corrective Action: Add capacity or delete unused snapshots
  Triggered On:   2024-01-15 10:15:42 +00:00

Alert ID: 3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r
  Severity:       informational
  Probable Cause: Scheduled backup completed successfully
  Description:    Backup job backup_daily_01 finished
  Corrective Action: No action required
  Triggered On:   2024-01-15 02:00:05 +00:00
```

!!! warning "Common errors"
    **`Error: This command is not available in the current cluster setup`** — Verify the cluster is running ONTAP 9.1 or later and that the health monitoring subsystem is enabled with `system health status show`.
    **`Error: Access denied for user 'admin' on this command`** — Ensure your user account has the 'admin' or 'readonly' role assigned via `security login show`.
Expected output: no rows. Any alert row must be acknowledged or resolved. Note the `Probable Cause` and `Corrective Action` columns — these are actionable.

---

**Step 4 — Aggregate health and usage**

```bash
storage aggregate show -fields state,used-percent
```


```text title="Expected output"
Aggregate                 State    Used%
aggr0                     online   65
aggr1                     online   78
svm_root                  online   42
data_aggregate            online   89
backup_aggregate          online   51
5 entries were displayed.
```

!!! warning "Common errors"
    **`Error: command not found: storage`** — Ensure you are connected to the ONTAP cluster via SSH or the ONTAP CLI, not a local shell.
    **`Error: Invalid field "used-percent"`** — Use the correct field name `used-percent` or check available fields with `storage aggregate show -fields ?`.
Expected output: all aggregates in `online` state. Flag any aggregate with `used-percent` exceeding 80%. At 85% or above treat as critical — see threshold table below.

---

**Step 5 — Offline volumes**

```bash
volume show -fields state,percent-used | grep -v online
```


```text title="Expected output"
Vserver   Volume       State      Percent Used
--------- ------------ ---------- ------------
cluster1  vol_backup   offline    45%
cluster1  vol_temp     restricted 78%
cluster2  vol_archive  offline    12%
```

!!! warning "Common errors"
    **`Error: command not found`** — Ensure you are connected to the ONTAP cluster via SSH or the ONTAP CLI, not a standard Linux shell.
    **`Error: No such field "percent-used"`** — Verify your ONTAP version supports the percent-used field; use `volume show -fields ?` to list available fields for your release.
Expected output: no rows (or only the header line). Any volume not in `online` state requires investigation before starting operational work.

---

**Step 6 — Volumes approaching capacity**

```bash
volume show -fields percent-used | awk 'NR==1 || $NF+0 > 80'
```


```text title="Expected output"
Vserver   Volume       Percent Used
--------- ------------ ------------
cluster1  vol_data_01  85
cluster1  vol_backup   92
cluster1  vol_logs     88
svm_prod  vol_archive  81
svm_prod  vol_temp     95
```

!!! warning "Common errors"
    **`Error: command not found: volume`** — Ensure you are connected to the ONTAP cluster via SSH or the ONTAP CLI, not a standard Linux shell.
    **`Error: invalid field name "percent-used"`** — Verify the field name matches your ONTAP version; use `volume show -fields ?` to list available fields.
Expected output: header line only. Any volume above 80% must be noted. Above 90% is critical — expand the volume or move data before proceeding with other work.

---

**Step 7 — SnapMirror replication lag**

```bash
snapmirror show -fields lag-time,health
```


```text title="Expected output"
Source Destination Mirror State Lag Time Health
======== =========== ============ ========== ======
svm1:vol_prod svm2:vol_prod_mirror SnapMirror Snapmirrored 00:15:32 Healthy
svm1:vol_data svm2:vol_data_mirror SnapMirror Snapmirrored 00:08:47 Healthy
svm3:vol_archive svm4:vol_archive_dr SnapMirror Snapmirrored 02:34:15 Healthy
svm2:vol_logs svm3:vol_logs_copy SnapMirror Snapmirrored 00:22:10 Unhealthy
svm1:vol_backup svm2:vol_backup_mirror SnapMirror Idle 23:45:00 Healthy
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are logged into the ONTAP cluster CLI (ssh admin@cluster-mgmt-ip) rather than the local shell.
    **`Error: No SnapMirror relationships found`** — Verify that SnapMirror relationships exist on this cluster using `snapmirror show` without filters first.
    **`Error: Invalid field name "lag-time"`** — Use the correct field name `lag_time` (underscore instead of hyphen) in the -fields parameter.
Expected output: all relationships show `true` for Health. For `lag-time`, compare against each relationship's schedule — lag exceeding 2× the schedule interval indicates a transfer problem. Any `false` Health value requires immediate investigation.

---

**Step 8 — LIF status**

```bash
network interface show -fields status-oper
```


```text title="Expected output"
Vserver         Interface       Address         Netmask         Status Admin Status Oper
-------         ---------       -------         -------         ------ ----- ----------
cluster1        e0a             192.168.1.10    255.255.255.0   up     up    up
cluster1        e0b             192.168.1.11    255.255.255.0   up     up    up
node1           mgmt1           10.0.0.50       255.255.255.0   up     up    up
node2           mgmt1           10.0.0.51       255.255.255.0   up     up    down
node1           data1           172.16.0.100    255.255.255.0   up     up    up
node2           data1           172.16.0.101    255.255.255.0   down   up    down
6 entries were displayed.
```

!!! warning "Common errors"
    **`Error: command not found: network`** — Ensure you are connected to the ONTAP cluster CLI (SSH to the cluster management IP), not the local shell.
    **`Error: invalid field name "status-oper"`** — Use the correct field name `status-admin` or `status-oper` separately, or omit `-fields` to see all interface details.
Expected output: all LIFs show `up` for `status-oper`. Any `down` LIF blocks storage access for the associated protocol — resolve before starting other work.

---

**Step 9 — Broken or failed disks**

```bash
storage disk show -broken
```


```text title="Expected output"
Disk                 Container                     Type    RPM  Usable Size State
----------           ----------                     ----    ---  ----------- --------
1.0.0                FAILED                         SSD     N/A  372.6GB     broken
1.0.1                FAILED                         SSD     N/A  372.6GB     broken
1.0.8                FAILED                         HDD     7200 558.3GB     broken
2.1.5                FAILED                         SSD     N/A  372.6GB     broken
3.0.12               FAILED                         HDD     7200 1.0TB       broken

5 entries were displayed.
```

!!! warning "Common errors"
    **`Error: command not found: storage`** — Ensure you are running this command in the ONTAP CLI (SSH to the cluster management IP), not in the Linux shell.
    **`Error: access denied for command "storage disk show"`** — Verify your user role has the "storage" privilege by running `security login show -user-or-group-name <username>`.
Expected output: no rows. Any broken disk must be replaced immediately. Open a case with NetApp if the disk is under support contract. Do not start any workload migrations until broken disks are replaced.

---

**Step 10 — Recent error events (last hour)**

```bash
event log show -severity error -time-range "1h"
```


```text title="Expected output"
Time                 Severity Event
-------------------- -------- -----------------------------------------------
2024-01-15 14:32:18  ERROR    Aggregate aggr_ssd_01: RAID status degraded
2024-01-15 14:28:45  ERROR    Volume vol_data_prod: Snapshot copy failed
2024-01-15 14:15:22  ERROR    Node cluster-02: Network interface e0a down
2024-01-15 14:02:10  ERROR    LUN lun_db_backup: Space threshold exceeded
2024-01-15 13:58:33  ERROR    SnapMirror job SM_hourly_sync: Transfer aborted
```

!!! warning "Common errors"
    **`Error: invalid time-range format`** — Use ISO 8601 format or relative time like "-1h", "-24h", or specify absolute timestamps with "-start-time" and "-end-time" parameters.
    **`Error: This command requires cluster admin privileges`** — Run the command with an account that has cluster-admin role, or use `security login show` to verify your permissions.
Expected output: no rows, or only informational entries. Review any `error`-severity events. Cross-reference with steps 3–9 to determine if they are already captured by an alert. Events not tied to an existing alert need investigation.

---

**Step 11 — AutoSupport delivery**

```bash
autosupport history show
```


```text title="Expected output"
Node: cluster1-01
Sequence Number: 1847
Subject: AUTOSUPPORT [cluster1-01] 192.168.1.45
Sent Time: 2024-01-15 14:32:18 +00:00
Destination: support.netapp.com
Status: Sent
Size: 8.2 MB

Node: cluster1-02
Sequence Number: 1846
Subject: AUTOSUPPORT [cluster1-02] 192.168.1.46
Sent Time: 2024-01-15 14:31:45 +00:00
Destination: support.netapp.com
Status: Sent
Size: 7.9 MB

Node: cluster1-01
Sequence Number: 1845
Subject: AUTOSUPPORT [cluster1-01] 192.168.1.45
Sent Time: 2024-01-14 02:15:33 +00:00
Destination: support.netapp.com
Status: Sent
Size: 8.1 MB
```

!!! warning "Common errors"
    **`Error: command not found`** — Verify you are connected to the ONTAP cluster CLI and have appropriate admin privileges.
    **`Error: This command is not supported on this release`** — Check your ONTAP version with `version` command; autosupport history show requires ONTAP 9.6 or later.
Expected output: the most recent entry shows `sent-successful` or `ignore`. A `failed` status means AutoSupport is not reaching NetApp — check proxy configuration and network connectivity. This does not block operations but must be resolved today.

---

## Health Thresholds

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Aggregate used | >75% | >85% | Add disks or enable thin-provisioning on hosted volumes |
| Volume used | >80% | >90% | Expand volume size or move data to a less-full aggregate |
| SnapMirror lag | >2x schedule interval | RPO breach | Force a manual `snapmirror update`, check bandwidth and network |
| Broken disks | Any | Any | Replace immediately, open NetApp support case |
| LIF down | Any | Any | Investigate port and failover group; restore before starting work |
| Health alerts | Any warning | Any error | Follow Corrective Action in `system health alert show` |

---

## See Also

- [ONTAP Health Checks](../health-checks.md) — broader health-check reference covering storage, network, and protocol layers
- [ONTAP Procedures](../procedures.md) — step-by-step procedures for common admin tasks
- [ONTAP Troubleshooting](../../troubleshooting/index.md) — common issues and diagnostic steps
- [ONTAP CLI Reference](../cli-reference.md) — full command reference for ONTAP CLI
- [ONTAP Operations](../index.md) — all ONTAP operations pages
