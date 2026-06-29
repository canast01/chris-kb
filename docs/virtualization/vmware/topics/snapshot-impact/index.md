---
tags:
  - vmware
---
# Snapshot Performance Impact

<div class="kb-summary">
Snapshots are a write-redirect mechanism — they do not freeze data, they redirect writes to a delta disk. This has measurable performance and operational consequences.

*Applies to: vSphere 7.x / 8.x*
</div>

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Snapshot Performance Impact \u2014 Thresholds",
    "fontSize": 13,
    "fontWeight": "normal"
  },
  "width": 480,
  "height": {
    "step": 26
  },
  "data": {
    "values": [
      {
        "metric": "Delta disk > 50% of base disk",
        "zone": "Safe",
        "val": 50
      },
      {
        "metric": "Delta disk > 50% of base disk",
        "zone": "Alert",
        "val": 50
      }
    ]
  },
  "mark": {
    "type": "bar",
    "cornerRadiusEnd": 3
  },
  "encoding": {
    "y": {
      "field": "metric",
      "type": "nominal",
      "axis": {
        "title": null,
        "labelLimit": 200
      },
      "sort": null
    },
    "x": {
      "field": "val",
      "type": "quantitative",
      "stack": "normalize",
      "axis": {
        "title": "Threshold boundary",
        "format": ".0%"
      }
    },
    "color": {
      "field": "zone",
      "type": "nominal",
      "scale": {
        "domain": [
          "Safe",
          "Alert"
        ],
        "range": [
          "#15803d",
          "#dc2626"
        ]
      },
      "legend": {
        "title": "Zone"
      }
    },
    "order": {
      "field": "zone",
      "sort": [
        "Safe",
        "Alert"
      ]
    },
    "tooltip": [
      {
        "field": "metric",
        "type": "nominal",
        "title": "Metric"
      },
      {
        "field": "zone",
        "type": "nominal",
        "title": "Zone"
      },
      {
        "field": "val",
        "type": "quantitative",
        "title": "Segment %",
        "format": ".0f"
      }
    ]
  }
}
```

## How Snapshots Work

```text
Base VMDK (read-only once snapshot exists)
  └── Delta disk (-000001.vmdk) — all new writes go here
        └── Delta disk (-000002.vmdk) — if a second snapshot is taken
```

Every read must check whether the block exists in the delta chain before falling back to the base disk. Chain depth increases read latency.

## Performance Impact by Chain Depth

| Snapshot Depth | Typical IOPS Impact | Typical Latency Impact |
|---|---|---|
| 1 snapshot | 5–10% overhead | Minimal |
| 2–3 snapshots | 10–25% overhead | Noticeable on I/O-intensive VMs |
| 4+ snapshots | 25–50%+ overhead | Significant; backup tools may create multi-snapshot chains |
| 32 snapshots | VMware-imposed maximum | Near-unusable for write-heavy workloads |

## Detecting Snapshot Issues

```powershell
# List all VMs with snapshots, sorted by snapshot count
Get-VM | Where-Object { $_.ExtensionData.Snapshot -ne $null } |
    Select-Object Name,
        @{N="SnapCount"; E={ ($_ | Get-Snapshot | Measure-Object).Count }},
        @{N="OldestSnap"; E={ ($_ | Get-Snapshot | Sort-Object Created | Select-Object -First 1).Created }} |
    Sort-Object SnapCount -Descending

# Flag snapshots older than 3 days
Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-3) } |
    Select-Object VM, Name, Created, SizeGB
```

## Consolidation Warnings

```powershell
# Find VMs needing consolidation (orphaned delta files present)
Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded -eq $true } |
    Select-Object Name

# Trigger consolidation
Get-VM "vm-name" | Get-View | Invoke-Method -Name ConsolidateVMDisks_Task
```

## esxtop — Identifying Snapshot Latency

```bash
# Connect to host, run esxtop in disk mode
esxtop
# Press 'u' for disk view
# Look for GAVG (guest average latency) > 25ms and DAVG (device latency) > 15ms
# Compare VMs with/without snapshots for correlation
```


```text title="Expected output"
ESXTOP 7.0.3 -- 192.168.1.42 -- 09:34:22
DISK ADAPTER STATISTICS
Adapter    CMDS/s  READS/s  WRITES/s  MBPS    GAVG    DAVG    QAVG    %UTIL
vmhba0     145.2   89.3     55.9      234.5   18.2    8.1     0.3     42%
vmhba1     312.7   156.4    156.3     512.1   34.6    22.4    1.8     78%
vmhba2     98.1    45.2     52.9      156.3   12.1    5.9     0.1     28%

VIRTUAL MACHINE DISK STATISTICS
VM Name              READS/s  WRITES/s  GAVG    DAVG    %RDY
prod-db-01           234.5    89.3      42.1    18.7    8.2%
prod-web-02          45.2     12.1      8.3     3.2     1.1%
prod-db-01-snap      189.7    156.2     67.3    31.4    14.6%
backup-vm-03         12.3     4.5       5.1     2.1     0.3%
...
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are connected to an ESXi host via SSH or use vSphere Client; esxtop only runs on ESXi hosts, not vCenter.
    **`ESXTOP: Unable to open /proc/vmware/sched/pcpu/cpu0/stats`** — Verify the user account has root or equivalent ESXi administrative privileges; standard users cannot access performance metrics.
    **`ESXTOP: No such file or directory`** — Confirm the ESXi host is fully booted and the hostd service is running with `systemctl status hostd`; esxtop requires the management daemon to be active.
## Backup-Induced Snapshots

Backup tools (Veeam, NBU, Commvault) create and delete a snapshot per job run. If the delta disk grows large during backup and consolidation is slow:

- I/O is redirected to the delta for the entire backup window.
- Consolidation after backup can cause a "stun" (VM pause of 1–30 seconds) while delta is merged.

```powershell
# Monitor consolidation task progress
Get-Task | Where-Object { $_.Name -match "ConsolidateVM" } |
    Select-Object ObjectId, State, PercentComplete, StartTime
```

## Storage Impact

```powershell
# Check total snapshot disk consumption per datastore
Get-Datastore | ForEach-Object {
    $ds = $_
    $snaps = Get-VM -Datastore $ds | Get-Snapshot
    [PSCustomObject]@{
        Datastore     = $ds.Name
        FreeSpaceGB   = [math]::Round($ds.FreeSpaceGB, 1)
        SnapshotCount = ($snaps | Measure-Object).Count
        SnapshotSizeGB= [math]::Round(($snaps | Measure-Object SizeGB -Sum).Sum, 1)
    }
}
```

## Policy and Remediation

| Threshold | Action |
|---|---|
| Snapshot > 3 days old | Alert; review with VM owner |
| Snapshot > 7 days old | Escalate; delete unless exception approved |
| Snapshot chain > 3 deep | Immediate remediation |
| Consolidation needed flag | Schedule consolidation in next maintenance window |
| Delta disk > 50% of base disk | Emergency — consolidate immediately |
