---
tags:
  - vmware
description: "Understanding what normal recovery looks like prevents unnecessary intervention during incidents."
---
# Recovery Behavior Expectations

<div class="kb-summary">
Understanding what normal recovery looks like prevents unnecessary intervention during incidents.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

after_host_failure: "After Host Failure" {shape: rectangle}
after_storage_failure: "After Storage Failure" {shape: rectangle}
after_network_failure: "After Network Failure" {shape: rectangle}
after_vsan_component_failure: "After vSAN Component Failure" {shape: rectangle}
recovery_performance_impact: "Recovery Performance Impact" {shape: rectangle}
when_to_escalate: "When to Escalate" {shape: rectangle}

after_host_failure -> after_storage_failure: uses
after_storage_failure -> after_network_failure: uses
after_network_failure -> after_vsan_component_failure: uses
after_vsan_component_failure -> recovery_performance_impact: uses
recovery_performance_impact -> when_to_escalate: uses
```

## After Host Failure

| Phase | Expected Behavior | Timeframe |
|---|---|---|
| HA detection | vCenter marks host as unreachable | 0–30 seconds |
| HA restart | FDM restarts VMs on remaining hosts | 1–5 minutes |
| VM boot | Guest OS boots normally | 1–3 minutes |
| vSAN resync | If vSAN — rebuild begins for affected components | Minutes to hours (data-dependent) |
| DRS rebalance | DRS may initiate vMotions to rebalance | Within 5–15 minutes |

```powershell
# Monitor HA restart events
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -match "VmRestartedByHA" } |
    Select-Object CreatedTime, @{N="VM";E={$_.Vm.Name}}, FullFormattedMessage

# Check current host state
Get-VMHost | Select-Object Name, ConnectionState, PowerState
```

## After Storage Failure

| Phase | Expected Behavior |
|---|---|
| Path marked dead | `esxcli storage core path list` shows `State: dead` |
| APD declared | After 140 seconds of all paths down (APD) |
| PDL declared | If array signals permanent loss via SCSI sense code |
| VMs paused | APD/PDL triggers HA response (if configured) |
| Object rebuild (vSAN) | New replica created on remaining disk capacity |

```bash
# Check path states on ESXi host
esxcli storage core path list | grep -E "State:|Device:"

# APD/PDL events in vmkernel log
grep -i "APD\|PDL\|lost path" /var/log/vmkernel.log | tail -20
```


```text title="Expected output"
State: active
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
State: active
Device: naa.60001405m2n3o4p5q6r7s8t9u0v1w2x3
State: standby
Device: naa.60001405y1z2a3b4c5d6e7f8g9h0i1j2k
State: disabled
Device: naa.60001405l3m4n5o6p7q8r9s0t1u2v3w4

2024-10-15T14:23:45.123Z cpu2:2048)WARNING: ScsiPath: 2897: Lost path to device naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
2024-10-15T14:24:12.456Z cpu5:4096)WARNING: PDL detected on device naa.60001405m2n3o4p5q6r7s8t9u0v1w2x3
2024-10-15T14:25:33.789Z cpu1:1024)WARNING: APD condition detected: device naa.60001405y1z2a3b4c5d6e7f8g9h0i1j2k
2024-10-15T14:26:01.234Z cpu3:2560)WARNING: ScsiPath: 2897: Lost path to device naa.60001405l3m4n5o6p7q8r9s0t1u2v3w4
2024-10-15T14:27:15.567Z cpu7:5120)WARNING: APD timeout: device naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2 entering PDL state
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/vmkernel.log: No such file or directory` | SSH directly to the ESXi host instead of running commands through vCenter; the vmkernel.log path is only accessible on the ESXi host itself. |
    | `esxcli: command not found` | Ensure you are logged into an ESXi host with SSH access; esxcli is not available on vCenter Server or Windows hosts. |
**Do not rescan storage unnecessarily during a recovery** — it can delay path re-establishment.

## After Network Failure

| Phase | Expected Behavior |
|---|---|
| Link down detected | vmkernel.log logs "Link down" immediately |
| HA heartbeat breaks | After 10 seconds without heartbeat, HA considers host isolated |
| Isolation response | Host executes configured isolation response (leave/power off/shutdown) |
| Alarms | Alarm storm for disconnected VMs and host |
| Recovery | Once link restored, host reconnects to vCenter within 60–120 seconds |

```powershell
# Check for recent network isolation events
Get-VIEvent -MaxSamples 1000 | Where-Object { $_.GetType().Name -match "DasHostIsolated" } |
    Select-Object CreatedTime, FullFormattedMessage
```

## After vSAN Component Failure

```bash
# Resync activity (normal after component failure)
esxcli vsan debug resync list

# Object health — degraded objects mean rebuild in progress
esxcli vsan debug object list | grep -v healthy

# Do NOT remove a second disk until resync completes
esxcli vsan debug resync list | grep "Total Bytes"
```


```text title="Expected output"
UUID                                  Bytes to Sync  Bytes Synced  Est. Time Remaining
52a4c8f1-2b3e-4a9c-b1d2-8e9f3c5a7b2d  847.3 GB      234.5 GB      ~45 minutes
7f1e9d3c-5b2a-4e8f-9c1d-2a5b8e3f7c4d  512.0 GB      512.0 GB      ~0 minutes
Total Resync Objects: 2

UUID                                  Object Health  Bytes  Component Count
a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d  degraded       2.1 GB  3/3
f7e6d5c4-b3a2-9f8e-7d6c-5b4a-3f2e1d0c  degraded       1.8 GB  2/3
c9d8e7f6-a5b4-3c2d-1e0f-9a8b7c6d5e4f  healthy        4.2 GB  3/3

Total Bytes to Sync: 1.36 TB
Bytes Already Synced: 746.5 GB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Resync operations are not running` | Verify the failed disk has been replaced and the host has rejoined the cluster with `esxcli vsan cluster get`. |
    | `grep: (standard input): No such input` | Ensure VSAN is enabled on the cluster and the host has valid VSAN membership with `esxcli vsan cluster info`. |
## Recovery Performance Impact

| Event | Performance Impact | Duration |
|---|---|---|
| HA restart | Affected VMs fully stopped during restart | Minutes |
| vSAN resync | Up to 30% IOPS reduction during rebuild | Hours |
| NIC failover (teaming) | Brief (<1s) packet loss during failover | Sub-second |
| vMotion | 10–15% overhead on source host during transfer | Minutes per VM |

## When to Escalate

- HA restarts still in progress after 15 minutes
- vSAN resync has not started 10 minutes after host failure
- APD not resolved after storage path recovery
- VM fails to power on with "insufficient resources" after HA restart
