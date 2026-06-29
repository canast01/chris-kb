---
tags:
  - vmware
---
# Resource Contention Modeling

<div class="kb-summary">
Resource Contention Modeling reference covering CPU Contention, Memory Contention, Storage Latency, Network Contention, Contention Response Actions and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Resource Contention Modeling \u2014 Thresholds",
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
        "metric": "Memory usage %",
        "zone": "Safe",
        "val": 90
      },
      {
        "metric": "Memory usage %",
        "zone": "Alert",
        "val": 10
      },
      {
        "metric": "RX/TX utilisation",
        "zone": "Safe",
        "val": 80
      },
      {
        "metric": "RX/TX utilisation",
        "zone": "Alert",
        "val": 20
      },
      {
        "metric": "Packet loss (vmkping)",
        "zone": "Safe",
        "val": 0
      },
      {
        "metric": "Packet loss (vmkping)",
        "zone": "Alert",
        "val": 100
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

## CPU Contention

**CPU Ready** is the primary indicator: time a vCPU waited in the run queue because the physical CPU was busy.

| CPU Ready % | State |
|---|---|
| < 5% | Normal |
| 5–10% | Monitor |
| > 10% | Contention — investigate |
| > 20% | Severe — VM performance severely impacted |

```powershell
# CPU usage across all hosts
Get-VMHost | Select-Object Name,
    @{N="CPUUsageMHz";E={$_.CpuUsageMhz}},
    @{N="CPUTotalMHz";E={$_.CpuTotalMhz}},
    @{N="UsedPct";E={[math]::Round($_.CpuUsageMhz / $_.CpuTotalMhz * 100, 1)}}

# Per-VM CPU ready (use esxtop or performance charts — not directly queryable via PowerCLI)
# In esxtop: press 'c' for CPU view — %RDY column
```

```bash
# esxtop CPU view — look for %RDY > 10
esxtop   # press 'c', then look at %RDY per world
```


```text title="Expected output"
ESXTOP - VMware ESXi top utility
GID  NAME                                   NWLD   %USED   %SYS   %RDY   %WAIT  %IDLE
  1  vmx:VM-WebServer-01                      4   45.23   8.12  12.47  18.93  15.25
  2  vmx:VM-Database-02                       8   72.15   6.89   3.21  14.32   3.43
  3  vmx:VM-AppServer-03                      2   28.45   5.67  18.92  22.11  24.85
  4  vmx:helper-world                         1    2.34   1.23   0.12   0.89  95.42
  5  vmx:VM-Backup-04                         6   61.78   7.45   8.34  16.23   6.20
  6  vmx:VM-Analytics-05                      3   55.89   9.12  14.56  12.34   8.09

Press 'q' to quit, 'c' for CPU, 'm' for memory, 'd' for disk, 'n' for network
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are logged into an ESXi host directly via SSH (not vCenter); esxtop is only available on ESXi.
    **`Error: Unable to initialize display`** — Run esxtop with a terminal that supports interactive mode (avoid non-interactive SSH sessions); use `ssh -t` to force pseudo-terminal allocation.
## Memory Contention

| Indicator | Threshold | Meaning |
|---|---|---|
| Balloon (MB) | > 0 | Host reclaiming memory from VMs |
| Swap rate (MB/s) | > 0 | Severe — swapping to disk, significant performance hit |
| Memory usage % | > 90% | High — ballooning imminent |
| Overhead | N/A | Hypervisor overhead, not controllable |

```powershell
# Memory state per host
Get-VMHost | Select-Object Name,
    @{N="MemUsedGB";E={[math]::Round($_.MemoryUsageGB,1)}},
    @{N="MemTotalGB";E={[math]::Round($_.MemoryTotalGB,1)}},
    @{N="UsedPct";E={[math]::Round($_.MemoryUsageGB / $_.MemoryTotalGB * 100, 1)}}
```

```bash
# esxtop memory view — look for MCTLSZ (balloon) and SWPRD/SWPWT (swap)
esxtop   # press 'm'
```


```text title="Expected output"
│ ESXTOP │ Press 'h' for help
│ World │ GID │ NWLD │ VMID │ NAME │ MCTLSZ │ SWPRD/s │ SWPWT/s │ %SWPFD                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2048 │ 2048 │ 1 │ 4 │ vm-prod-web-01 │ 512 MB │ 0 │ 2.4 │ 8.2%                                        │
│ 2049 │ 2049 │ 1 │ 5 │ vm-prod-db-02 │ 1.2 GB │ 12.8 │ 45.6 │ 34.7%                                    │
│ 2050 │ 2050 │ 1 │ 6 │ vm-dev-test-03 │ 256 MB │ 0 │ 0 │ 0.0%                                          │
│ 2051 │ 2051 │ 1 │ 7 │ vm-prod-app-04 │ 768 MB │ 3.2 │ 18.9 │ 12.1%                                    │
│ 2052 │ 2052 │ 1 │ 8 │ vm-prod-cache-05 │ 2.1 GB │ 28.4 │ 156.2 │ 67.3%                                │
│ 2053 │ 2053 │ 1 │ 9 │ vm-backup-srv-06 │ 0 MB │ 0 │ 0 │ 0.0%                                          │
...
(Press 'q' to quit, 'h' for help)
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are running this command directly on an ESXi host (not a vCenter server) with SSH access enabled.
    **`Cannot open /proc/vmware/sched: Permission denied`** — Run esxtop with root privileges or as a user in the root group.
## Storage Latency

| Latency | State |
|---|---|
| < 10 ms | Normal |
| 10–20 ms | Warning — monitor under load |
| > 20 ms | Problem — investigate |
| > 50 ms | Severe — application timeouts likely |

```powershell
# Datastore latency (requires performance metrics collection enabled)
$stats = Get-Stat -Entity (Get-Datastore "<ds_name>") -Stat "datastore.totalReadLatency.average", "datastore.totalWriteLatency.average" -Realtime -MaxSamples 20
$stats | Select-Object Entity, MetricId, Value, Timestamp
```

## Network Contention

| Indicator | Threshold | Meaning |
|---|---|---|
| Dropped packets | > 0 | NIC ring buffer full or physical issue |
| RX/TX utilisation | > 80% | NIC saturation — add uplinks |
| Packet loss (vmkping) | > 0% | Physical or MTU issue |

```bash
# NIC utilisation
esxcli network nic stats get -n vmnic0 | grep -E "Bytes|Dropped"

# Real-time: esxtop network view
esxtop   # press 'n'
```


```text title="Expected output"
Bytes Received: 4,294,967,296
Bytes Transmitted: 2,147,483,648
Dropped Rx Packets: 0
Dropped Tx Packets: 0

esxtop 5.5.0   Build 1746018   (c) 1998-2013 VMware, Inc. All rights reserved.
PORT-ID UPLINK PKTRX/s PKTTX/s MbRX/s MbTX/s DRPRX DRPTX
vmnic0  yes    12450   8932    847.3  621.5  0     0
vmnic1  yes    11203   9104    798.2  634.1  2     0
vmnic2  no     0       0       0.0    0.0    0     0
vmnic3  no     0       0       0.0    0.0    0     0
```

!!! warning "Common errors"
    **`Could not get network stats for vmnic0: Unknown option`** — Verify the NIC name with `esxcli network nic list` and ensure you're using the correct vmnic identifier.
    **`esxtop: command not found`** — Install or enable esxtop; if using ESXi 7.0+, use `esxcli stats` or vSphere Client instead as esxtop may be deprecated.
## Contention Response Actions

| Resource | Contention | Response |
|---|---|---|
| CPU | %RDY > 10% | vMotion VMs to less loaded host; review DRS settings |
| Memory | Balloon > 0 | vMotion VMs; add RAM; reduce VM memory reservations |
| Memory | Swap > 0 | Emergency — vMotion immediately; swap = disk I/O |
| Storage | Latency > 20ms | Check array load; rebalance VMs across datastores |
| Network | Drops > 0 | Check MTU, cable, uplink saturation |

## DRS Imbalance Score

```powershell
# DRS migration recommendations pending
Get-Cluster "<cluster>" | Select-Object Name,
    @{N="DRSScore";E={$_.ExtensionData.Summary.UsagesSummary.OverallUsage}}

# Review DRS recommendations
(Get-Cluster "<cluster>").ExtensionData.RecommendedAction
```
