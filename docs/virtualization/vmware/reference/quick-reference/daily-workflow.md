---
tags:
  - reference
description: "A repeatable morning workflow to confirm the environment is healthy before the business day begins."
---
# Daily VMware Operations Workflow

<div class="kb-summary">
A repeatable morning workflow to confirm the environment is healthy before the business day begins.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

step_1_vcenter_alarm_triage_5_min: "Step 1 — vCenter Alarm Triage (5 min)" {shape: rectangle}
step_2_host_health_3_min: "Step 2 — Host Health (3 min)" {shape: rectangle}
step_3_cluster_ha_and_drs_status_2_m: "Step 3 — Cluster HA and DRS Status (2 min)" {shape: rectangle}
step_4_datastore_capacity_3_min: "Step 4 — Datastore Capacity (3 min)" {shape: rectangle}
step_5_vsan_health_2_min_if_applicab: "Step 5 — vSAN Health (2 min, if applicable)" {shape: rectangle}
step_6_review_failed_tasks_2_min: "Step 6 — Review Failed Tasks (2 min)" {shape: rectangle}

step_1_vcenter_alarm_triage_5_min -> step_2_host_health_3_min: uses
step_2_host_health_3_min -> step_3_cluster_ha_and_drs_status_2_m: uses
step_3_cluster_ha_and_drs_status_2_m -> step_4_datastore_capacity_3_min: uses
step_4_datastore_capacity_3_min -> step_5_vsan_health_2_min_if_applicab: uses
step_5_vsan_health_2_min_if_applicab -> step_6_review_failed_tasks_2_min: uses
```

## Step 1 — vCenter Alarm Triage (5 min)

```powershell
# Connect and get all triggered alarms
Connect-VIServer -Server vcenter.example.local
Get-AlarmDefinition | Where-Object {$_.Enabled} | ForEach-Object {
    Get-Alarm -Entity (Get-Datacenter) | Where-Object {$_.Status -ne "Green"}
} | Select-Object Entity, AlarmDefinition, Status | Format-Table -AutoSize
```

- **Red/critical**: investigate immediately before proceeding
- **Yellow/warning**: log for follow-up; assign owner if persistent

## Step 2 — Host Health (3 min)

```powershell
# Any hosts not fully connected?
Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"} | Select-Object Name, ConnectionState

# Any hosts in maintenance mode unexpectedly?
Get-VMHost -State Maintenance | Select-Object Name, State
```

## Step 3 — Cluster HA and DRS Status (2 min)

```powershell
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, @{
    N="DrsMode"; E={$_.DrsAutomationLevel}
} | Format-Table -AutoSize
```

Confirm: HA Enabled = True, DRS Enabled = True, DrsMode = FullyAutomated (or as per standard).

## Step 4 — Datastore Capacity (3 min)

```powershell
Get-Datastore | Select-Object Name, FreeSpaceGB, CapacityGB, @{
    N="Used%"; E={[math]::Round((1-($_.FreeSpaceGB/$_.CapacityGB))*100,1)}
} | Where-Object {"Used%" -gt 75} | Sort-Object "Used%" -Descending
```

Any datastore > 75% full: investigate and action.

## Step 5 — vSAN Health (2 min, if applicable)

```bash
# SSH to any cluster host, or use vCenter:
# Cluster → Monitor → vSAN → Skyline Health
esxcli vsan health cluster list | grep -v "Green"   # Should return nothing
esxcli vsan debug resync summary                     # Confirm no unexpected resync in progress
```


```text title="Expected output"
(no output — command completes silently)

Cluster Resync Summary
======================
Cluster UUID: 52d4a8f1-7c2e-4d9a-b1e3-9f8c2a5d6e7f
Resync Operations: 0
Resync Bytes: 0 B
Estimated Time Remaining: 0 seconds
Last Updated: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`vsan health cluster list: Unknown command or namespace`** — Ensure you are running the command on an ESXi host with vSAN enabled; if vSAN is not licensed, install the vSAN license first.
    **`Error: Unable to connect to the vSAN cluster`** — Verify the host is part of an active vSAN cluster by checking vCenter under Cluster → Configure → vSAN → General.
## Step 6 — Review Failed Tasks (2 min)

vCenter UI → Recent Tasks → filter by Status: Error → review last 24 hours.

Key tasks to watch:
- Snapshot creation failures (backup dependency)
- VM migrate failures (DRS manual recommendations stuck)
- Storage profile compliance failures

## Step 7 — Backup Status (3 min)

Check backup tool dashboard for jobs that ran overnight:
- **Veeam**: Home → Last 24 Hours — any failures → investigate
- **CommVault**: Command Center → Jobs → Failed Jobs
- **NetBackup**: OpsCenter → Monitor → Jobs → Status: Failed

## Step 8 — Monitoring Dashboard (2 min)

Log in to Aria Operations:
- Environment overview: all objects should show green or yellow (not red)
- Confirm collection is running: `Collection State: OK` for all adapters
- Review any new Immediate or Critical alert categories generated overnight

## Step 9 — Follow-Up on Repeat Alerts

Review alerts older than 24 hours that have not been acknowledged:
- Assign each to an owner
- Create a change or task for any alert that has appeared > 3 consecutive days

Total estimated time: **~20 minutes**
