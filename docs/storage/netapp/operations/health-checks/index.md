---
tags:
  - netapp
  - operations
---
# NetApp Operations — Health Checks

<div class="kb-summary">
Health Checks reference covering Daily Health Check Workflow, AutoSupport Validation, Pre-Change Checklist, Health Summary Table.

*Applies to: ONTAP 9.x*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
daily_health_check_workflow: "Daily Health Check Workflow" {shape: rectangle}
autosupport_validation: "AutoSupport Validation" {shape: rectangle}
prechange_checklist: "Pre-Change Checklist" {shape: rectangle}
health_summary_table: "Health Summary Table" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> daily_health_check_workflow
daily_health_check_workflow -> autosupport_validation
autosupport_validation -> prechange_checklist
prechange_checklist -> health_summary_table
health_summary_table -> verify
verify -> generate_report
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Active IQ alerts** — log in to NetApp Active IQ → check open risk items by severity
2. **Cluster count and version** — run `cluster show` across all managed clusters
3. **Support case status** — NetApp Support → My Cases — review all open P1/P2 cases
4. **Capacity at risk** — Active IQ → Capacity → flag any clusters above 80% used
5. **Software version compliance** — verify no cluster is running an End-of-Support software version
6. **License compliance** — run `license show` on each cluster — verify all required licences are active

## Daily Health Check Workflow

```bash
# 1. Overall cluster health
cluster show
system health status show

# 2. HA pair status
storage failover show

# 3. Disk health
storage disk show -broken

# 4. Aggregate health
storage aggregate show -state !online
storage aggregate show -fields percent-used | awk '$2 > 80'

# 5. Volume health
volume show -state !online
volume show -fields percent-used | awk '$2 > 85'

# 6. Interface health
network interface show -status-oper down

# 7. EMS critical events (last 24 hours)
event log show -severity critical -time ">24h"
event log show -severity error -time ">24h"

# 8. SnapMirror health
snapmirror show -health false
```


```text title="Expected output"
Cluster UUID: 4a3c8b2f-91e7-4d6c-a2f1-7e9c3b5d2a1f
Cluster Name: prod-cluster-01
Cluster Serial Number: 4082068-50-147852

Health Status
Status: ok

Node            HA-Enabled  HA-Capable  Failover-State
node-01         true        true        Connected
node-02         true        true        Connected

Broken Disks: 0

Aggregate                State    Total Size  Used%
aggr_ssd_01              online   10.2TB      76%
aggr_ssd_02              online   10.2TB      82%
aggr_nl_01               online   50.5TB      91%

Volume                   State    Used%
vol_data_prod            online   78%
vol_logs_archive         online   88%

Interface      Status-Oper  Status-Admin  Address
e0a            down         up            192.168.1.10
e0b            up           up            192.168.1.11
e0c            up           up            192.168.1.12

Severity  Message                                    Time
CRITICAL  Disk shelf 2.1 temperature threshold exceeded  2024-01-15 14:32:18
ERROR     NTP sync lost on node-02                      2024-01-15 13:45:22
ERROR     CIFS connection limit approaching threshold    2024-01-15 12:18:05

Source Destination  Health  Status
cluster-02 cluster-01  false   Idle
cluster-03 cluster-01  false   Transferring
```

!!! warning "Common errors"
    **`Error: command not found: cluster show`** — Ensure you are connected to the NetApp cluster management interface (SSH to the cluster IP, not a node IP).
    **`Error: No entry matched the criteria in "storage disk show -broken"`** — This is expected output when no broken disks exist; it indicates healthy disk status, not an error condition.
    **`Error: "snapmirror show" command not found or SnapMirror not licensed`** — Verify SnapMirror license is installed with `system license show` and enable if needed.
## AutoSupport Validation

```bash
system node autosupport show -fields state,last-successful-destination
```


```text title="Expected output"
Node                                    State      Last Successful Destination
------------------------------------- ---------- -------------------------
cluster1-01                             enabled    mail
cluster1-02                             enabled    mail
cluster1-03                             enabled    http
cluster1-04                             enabled    mail
```

!!! warning "Common errors"
    **`Error: command not found`** — Ensure you are connected to the NetApp cluster via SSH or console; this command runs in ONTAP CLI, not the local shell.
    **`Error: Invalid field name "last-successful-destination"`** — Verify the ONTAP version supports this field; use `system node autosupport show` without field filters to confirm available columns.
Confirm last successful delivery is recent (within 24 hours for daily AutoSupport).

## Pre-Change Checklist

- [ ] Cluster health: `system health status show` → ok
- [ ] HA connected: `storage failover show` → Connected
- [ ] No broken disks: `storage disk show -broken` → no output
- [ ] All aggregates online: `storage aggregate show -state !online` → no output
- [ ] All volumes online: `volume show -state !online` → no output
- [ ] No down LIFs: `network interface show -status-oper down` → no output
- [ ] No critical EMS events in 24h
- [ ] SnapMirror relationships healthy

## Health Summary Table

| Check | Command | Expected |
|---|---|---|
| Cluster nodes | `cluster show` | health: true |
| HA pair | `storage failover show` | Connected |
| Disks | `storage disk show -broken` | No output |
| Aggregates | `storage aggregate show -state !online` | No output |
| Capacity | `storage aggregate show` | < 80% |
| Volumes | `volume show -state !online` | No output |
| LIFs | `network interface show -status-oper down` | No output |
| EMS | `event log show -severity critical` | No output |
| SnapMirror | `snapmirror show -health false` | No output |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [NetApp — Alerts](../alerts/)
- [NetApp — Support Cases](../support-cases/)
- [NetApp — Overview](../../)
