---
tags:
  - scenarios
  - vmware
---
# VM Performance Degraded

<div class="kb-summary">
A VM is slow or unresponsive. This scenario walks through a layered investigation across Aria Operations,
ESXi host metrics, vSAN storage performance, and NSX Distributed Firewall overhead to pinpoint the root
cause and apply the correct fix — CPU, memory, storage, or network.

*Applies to: vSphere 7.x / 8.x*
</div>

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "VM Performance Degraded \u2014 Thresholds",
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
        "metric": "CPU Ready (%)",
        "zone": "Safe",
        "val": 5
      },
      {
        "metric": "CPU Ready (%)",
        "zone": "Alert",
        "val": 95
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

## Products Involved

| Product | Role in This Scenario |
|---|---|
| Aria Operations | Initial alert triage; CPU ready %, memory balloon, latency, dropped packets |
| ESXi (esxtop) | Host-level CPU, memory, disk, and network metrics; ground truth |
| vSAN | Storage IOPS/throughput/latency per VM; component health |
| NSX (DFW) | East-west firewall overhead; connection timeouts vs packet drops |

---

## 1. Start in Aria Operations — Triage the Alert

Open the affected VM's alert in Aria Operations and note which metric is elevated — it determines where to dig next.

| Metric | Threshold | Meaning |
|---|---|---|
| CPU Ready (%) | > 5% | VM waiting for physical CPU — host overcommitted |
| Memory Balloon (KB) | > 0 sustained | Hypervisor reclaiming guest memory |
| Storage Latency (ms) | > 20 ms (DAVG) | Disk I/O contention at datastore layer |
| Network Dropped Packets | > 0.1% | NIC saturation or DFW overhead |

---

## 2. ESXi Layer — Run esxtop on the Host

SSH to the ESXi host and run esxtop to get real-time ground-truth metrics before acting.

```bash
# Batch mode — 3 samples, 50 lines of output; good for capture
esxtop -b -n 3 | head -50
```


```text title="Expected output"
ESXTOP(1)                                                           ESXTOP(1)

   LEGEND
   %USED    -- CPU used by the hypervisor and VMs
   %RUN     -- CPU ready time
   %WAIT    -- CPU wait time
   %CSTP    -- CPU co-stop time
   MEMSZ    -- Memory size in MB
   GRANT    -- Memory granted to VM
   ACTIVE   -- Active memory
   SHARED   -- Shared memory
   SWAPPED  -- Swapped memory

   GROUP CPU MEMORY DISK NETWORK
   1    12.5 45.2   8.3  2.1
   2    18.7 62.1   15.4 5.8
   3    5.2  28.9   3.1  0.9

   PCPU USED  RUN  WAIT CSTP
   0    14.2  2.1  1.8  0.0
   1    16.8  3.5  2.2  0.1
   2    11.5  1.9  1.5  0.0
   3    13.2  2.8  2.1  0.0

   VMID NAME                 %CPU  %MEM  %DISK %NET
   1    web-prod-01          22.5  48.2  12.1  3.2
   2    db-backup-02         8.3   71.5  28.4  1.1
   3    app-cache-03         15.7  35.9  5.2   8.7
   4    monitoring-04        5.1   22.3  2.1   0.4

   Batch sample 1 of 3 complete
   Batch sample 2 of 3 complete
   Batch sample 3 of 3 complete
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are running this command directly on an ESXi host via SSH or local console, not from a vCenter server or external machine.
    **`Error: Unable to open /proc/uptime: Permission denied`** — Run esxtop with elevated privileges using `sudo esxtop -b -n 3` or log in as root.
    **`Batch mode failed: Invalid sample count`** — Verify the `-n` parameter is a positive integer (e.g., `-n 3` not `-n 0` or `-n abc`).
Key esxtop views and what to look for:

```text
Press key to switch view:
  c  — CPU: look at %RDY (>5% = problem), %USED, %WAIT
  m  — Memory: look at MCTLSZ (balloon), SWPWRT (swap writes active)
  d  — Disk: look at DAVG (>20ms = latency), KAVG, QAVG
  n  — Network: look at %DRPD (dropped packets on vmnic)
```

```bash
# Check CPU ready and memory for a specific VM world
esxtop -b -n 1 | grep -A2 "vmx-vcpu"

# Check which VMs are consuming physical CPUs on the host
esxcli vm process list
```


```text title="Expected output"
PCPU  %USED  %RDY  %SYS  %WAIT %IDLE
  0   45.2  12.5   2.1  15.3  24.9
  1   38.7   8.9   1.8  18.2  32.4
  2   52.1  15.3   2.5  12.1  18.0
  3   41.5  10.2   2.0  16.8  29.5

World ID  Name                           CPU Affinity  %USED  %RDY
 4567     vmx-vcpu:vm-prod-web-01:0      0            45.2   12.5
 4568     vmx-vcpu:vm-prod-web-01:1      1            38.7    8.9

Getting all VMs
UUID                 Display Name              File                                    Memory    CPU  State
564d1234-5678-90ab   vm-prod-db-01            [datastore1] vm-prod-db-01/vm-prod-db-01.vmx  16384   4    running
564d5678-90ab-cdef   vm-prod-web-01           [datastore1] vm-prod-web-01/vm-prod-web-01.vmx  8192    2    running
564d90ab-cdef-1234   vm-dev-test-02           [datastore1] vm-dev-test-02/vm-dev-test-02.vmx  4096    1    running
564dab12-3456-7890   vm-prod-app-03           [datastore1] vm-prod-app-03/vm-prod-app-03.vmx  12288   4    running
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Verify you are running this command directly on an ESXi host (not a vCenter server) with SSH access enabled.
    **`grep: (standard input) is empty`** — Run `esxtop -b -n 1` without piping to check if esxtop is producing output; if blank, the host may be under extreme load or esxtop may need a moment to initialize.
    **`Error: The object has already been deleted or has not been completely created.`** — Wait a few seconds before running `esxcli vm process list` as the VM list may be refreshing; retry the command.
Look for: `%RDY` high across many VMs = host overcommitted; `%RDY` high on one VM only = check resource pool limits.

---

## 3. vSAN Layer — Check Storage Performance

Navigate to **Cluster → Monitor → vSAN → Performance Service** and check per-VM IOPS, throughput, and latency.

```bash
# List all vSAN objects and their health on the host
esxcli vsan debug object list

# List vSAN storage devices and disk group membership
esxcli vsan storage list

# Show per-VM vSAN performance counters (if performance service enabled)
esxcli vsan debug vmdk list
```


```text title="Expected output"
Object UUID                          Health  Owner  Congestion  IsSsd  Capacity
52a1f4c8-7d2e-4a9f-b1c2-9e3d5f6a7b8c  Healthy  host-42  0%  false  102400MB
7f9e8d7c-6b5a-4938-2d1c-0a9b8c7d6e5f  Healthy  host-42  2%  false  51200MB
1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d  Degraded  host-42  15%  true  204800MB
9z8y7x6w-5v4u-3t2s-1r0q-9p8o7n6m5l4k  Healthy  host-43  0%  false  76800MB
...

Storage Device                    Disk Group UUID                       Status
mpx.vmhba0:C0:T0:L0              4c5d6e7f-8a9b-0c1d-2e3f-4a5b6c7d8e9f  Healthy
mpx.vmhba1:C0:T1:L0              4c5d6e7f-8a9b-0c1d-2e3f-4a5b6c7d8e9f  Healthy
mpx.vmhba2:C0:T2:L0              5d6e7f8a-9b0c-1d2e-3f4a-5b6c7d8e9f0a  Healthy
...

VMDK UUID                            VM Name          Read(IOPS)  Write(IOPS)  Latency(ms)
52a1f4c8-7d2e-4a9f-b1c2-9e3d5f6a7b8c  prod-web-01      1245        342         2.3
7f9e8d7c-6b5a-4938-2d1c-0a9b8c7d6e5f  prod-db-02       892         1156        4.7
1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d  dev-app-03       45          23          1.1
```

!!! warning "Common errors"
    **`Unknown command at token esxcli`** — Verify you are running the command on an ESXi host with vSAN enabled, not a vCenter server.
    **`vSAN performance service is not enabled`** — Enable the vSAN performance service in vSAN cluster settings or use `esxcli vsan cluster get` to verify vSAN is operational.
Look for:

```text
vSAN Latency Tiers (DAVG from esxtop):
  < 5 ms   — healthy
  5–20 ms  — monitor closely
  > 20 ms  — investigate disk group / resync
  > 50 ms  — critical; likely degraded component or disk failure
```

In vCenter also check **vSAN → Monitor → Skyline Health** for capacity imbalance, absent/degraded components, and active resync queue (resync adds latency for all VMs on the disk group).

---

## 4. NSX DFW Layer — Rule Overhead on Network Traffic

If network is the bottleneck, run **Path Analysis** in Aria Networks (source VM → destination VM) to identify the blocking DFW rule ID.

```bash
# From NSX Manager REST API — get hit count for a specific rule
curl -sk -u admin:<password> \
  https://<nsx-manager>/api/v1/firewall/stats/rules/<rule-id> \
  | python3 -m json.tool
```


```text title="Expected output"
{
  "rule_id": "1001",
  "rule_name": "Allow-Web-Traffic",
  "hit_count": 15847,
  "byte_count": 2847362,
  "packet_count": 12456,
  "last_hit_timestamp": 1699564823000,
  "enabled": true,
  "direction": "IN_OUT",
  "source": "10.0.0.0/8",
  "destination": "192.168.1.0/24",
  "service": "HTTP,HTTPS",
  "action": "ALLOW",
  "statistics": {
    "total_sessions": 8923,
    "active_sessions": 127,
    "dropped_packets": 0
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification (already present in example, but ensure it's not removed).
    **`curl: (7) Failed to connect to <nsx-manager>: Name or service not known`** — Verify the NSX Manager hostname or IP address is correct and reachable from your network.
    **`jq: parse error: Invalid JSON at line 1`** — Confirm the API endpoint and rule ID are valid; an invalid rule ID may return HTML error pages instead of JSON.
Look for: high hit-count rules on east-west flows. Reduce overhead by consolidating rules with the same action and groups, adding a service exception for high-throughput backup VMs, or disabling packet logging on stateful rules.

---

## 5. PowerCLI — Pull Historical Performance Stats

Pull the past hour of stats without needing Aria Operations access.

```powershell
# CPU ready — high sustained values confirm host-level contention
Get-VM "vm-name" | Get-Stat -Stat cpu.ready.summation `
  -Start (Get-Date).AddHours(-1) -IntervalMins 5 | Format-Table -AutoSize

# Memory balloon — non-zero means hypervisor is reclaiming guest memory
Get-VM "vm-name" | Get-Stat -Stat mem.balloon.average `
  -Start (Get-Date).AddHours(-1) -IntervalMins 5 | Format-Table -AutoSize

# Disk latency — check both read and write
Get-VM "vm-name" | Get-Stat -Stat disk.totalLatency.average `
  -Start (Get-Date).AddHours(-1) -IntervalMins 5 | Format-Table -AutoSize
```

---

## 6. Resolution Reference

| Symptom | Root Cause | Fix |
|---|---|---|
| CPU Ready > 5% | Host overcommitted | DRS migration to less-loaded host; adjust resource pool limits |
| Memory balloon active | Host memory pressure | Increase VM RAM reservation; add RAM to host if persistent |
| vSAN DAVG > 20 ms | Disk group contention or component rebuild | Check resync queue; replace failed disk; rebalance capacity |
| Network dropped packets | NIC saturation or DFW overhead | Check vmnic utilisation; reduce DFW rule count; disable rule logging |
| East-west latency spike | DFW stateful tracking overhead | Profile DFW rules with Aria Networks; add exclusion for high-throughput flows |

---

## Key Terms

| Term | Definition |
|---|---|
| Aria Operations | VMware observability platform; used here to receive the initial performance alert and surface CPU ready %, balloon, and latency metrics per VM |
| esxtop | ESXi CLI tool that shows real-time host-level metrics — CPU, memory, disk, network — at the individual VM and physical device level |
| CPU Ready (%RDY) | Time a VM spends waiting for physical CPU time; measured in esxtop; > 5% indicates the host is overcommitted and the VM is being starved |
| DAVG | Disk average latency (milliseconds) as reported by esxtop at the device driver layer; > 20 ms on vSAN indicates storage contention or a degraded component |
| DRS | Distributed Resource Scheduler; vCenter feature that automatically migrates VMs via vMotion to balance CPU and memory load across cluster hosts |
| vSAN | VMware's hyperconverged storage layer; aggregates local host disks into a shared datastore; performance degrades during component rebuild (resync) |
| DFW | Distributed Firewall; NSX kernel-level firewall enforced per vNIC on every ESXi host; high rule counts or stateful logging add per-packet overhead to east-west traffic |
| PCPU | Physical CPU; a single logical processor core on the ESXi host; %RDY in esxtop reflects how many PCPU cycles a VM is waiting to receive |
| Memory balloon | Hypervisor memory reclamation technique where ESXi inflates a balloon driver inside the guest to reclaim pages; any sustained balloon value means the host is under memory pressure |
| vmnic | Physical NIC on the ESXi host; %DRPD in the esxtop network view shows dropped packets per vmnic; saturation here causes VM network degradation |
| IOPS | Input/output operations per second; the throughput metric for storage; monitored via vSAN Performance Service per VM to distinguish storage bottlenecks from CPU/memory issues |
| vNIC | Virtual NIC presented to the guest VM; DFW rules are enforced at the vNIC kernel layer, so overhead is incurred even for traffic between VMs on the same host |

---

## Common Mistakes

- **Checking vSAN before ESXi host metrics.** Always verify host-level CPU and memory first. vSAN can appear healthy while the host is CPU-starved, masking the real cause.
- **Ignoring CPU ready while focusing on guest CPU.** A guest OS showing 90% CPU usage may actually be waiting for physical CPU time — %RDY in esxtop tells the real story.
- **Overlooking DFW as a latency source.** East-west traffic between VMs on the same host still traverses the DFW kernel module. High rule counts add measurable overhead.
- **Forgetting resource pool limits.** A VM inside a resource pool with a hard CPU limit will show high CPU ready even on an otherwise idle host.

---

## Related Scenarios

- [vMotion Failing](vmotion-failing/index.md) — vMotion failures often surface during performance investigations when DRS tries to rebalance a degraded host.
- [vSAN Disk or Component Failure](vsan-disk-component-failure/index.md) — vSAN latency spikes are frequently caused by active component rebuild after a disk event.
- [NSX Connectivity Broken](nsx-connectivity-broken/index.md) — When dropped packets point to the network layer, a full NSX path trace is the logical next step.
