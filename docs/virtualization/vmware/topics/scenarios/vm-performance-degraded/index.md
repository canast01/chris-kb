# VM Performance Degraded

<div class="kb-summary">
A VM is slow or unresponsive. This scenario walks through a layered investigation across Aria Operations,
ESXi host metrics, vSAN storage performance, and NSX Distributed Firewall overhead to pinpoint the root
cause and apply the correct fix — CPU, memory, storage, or network.
</div>

```text
┌─────────────────────────────── VM Performance Degraded — Investigation Flow ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Alert in Aria Operations — VM latency / CPU ready / dropped packets anomaly detected      ││
│   └──────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                              │                                                        │
│              ┌───────────────────────────────┼───────────────────────────────┐                        │
│              ▼                               ▼                               ▼                        │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │   CPU Ready > 5%?   │        │  Memory Balloon/     │        │ Disk DAVG > 20 ms?  │              │
│   │  Check ESXi PCPU    │        │  Swap Active?        │        │ Check vSAN layer    │              │
│   │  %RDY via esxtop    │        │  Check MEM via       │        │ IOPS / throughput   │              │
│   │                     │        │  esxtop              │        │ / latency per VM    │              │
│   └────────┬────────────┘        └────────┬─────────────┘        └─────────┬───────────┘              │
│            │                              │                                 │                         │
│            ▼                              ▼                                 ▼                         │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ DRS migration or    │        │ Increase RAM         │        │ vSAN component      │              │
│   │ resource pool       │        │ reservation;         │        │ health check;       │              │
│   │ adjustment          │        │ remove balloon       │        │ disk rebuild?       │              │
│   └─────────────────────┘        └─────────────────────┘        └─────────────────────┘               │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Network issue? → NSX DFW: Aria Networks path trace → DFW rule hit count → reduce rule count      ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Open Aria Operations and navigate to the affected VM's alert. Check these four metrics first:

| Metric | Threshold | Meaning |
|---|---|---|
| CPU Ready (%) | > 5% | VM waiting for physical CPU — host overcommitted |
| Memory Balloon (KB) | > 0 sustained | Hypervisor reclaiming guest memory |
| Storage Latency (ms) | > 20 ms (DAVG) | Disk I/O contention at datastore layer |
| Network Dropped Packets | > 0.1% | NIC saturation or DFW overhead |

Note which metric is elevated. That determines where to dig next.

---

## 2. ESXi Layer — Run esxtop on the Host

SSH to the ESXi host where the VM is running and use esxtop for real-time host metrics.

```bash
# Batch mode — 3 samples, 50 lines of output; good for capture
esxtop -b -n 3 | head -50
```

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

If %RDY is high across many VMs on the same host, the host is CPU-overcommitted. If it is only one VM, check resource pool limits and reservations.

---

## 3. vSAN Layer — Check Storage Performance

Navigate in vCenter to **Cluster → Monitor → vSAN → Performance Service** to view per-VM IOPS, throughput, and latency. Then check health.

```bash
# List all vSAN objects and their health on the host
esxcli vsan debug object list

# List vSAN storage devices and disk group membership
esxcli vsan storage list

# Show per-VM vSAN performance counters (if performance service enabled)
esxcli vsan debug vmdk list
```

In vCenter, also check **vSAN → Monitor → Skyline Health**. Look for:

- Disk capacity imbalance (hot disk)
- Component state: "Absent" or "Degraded"
- Resync queue — active resync adds latency for all VMs on the disk group

```text
vSAN Latency Tiers (DAVG from esxtop):
  < 5 ms   — healthy
  5–20 ms  — monitor closely
  > 20 ms  — investigate disk group / resync
  > 50 ms  — critical; likely degraded component or disk failure
```

---

## 4. NSX DFW Layer — Rule Overhead on Network Traffic

If the network path is the bottleneck, use Aria Operations for Networks (Aria Networks) to trace the path.

From Aria Networks, run **Path Analysis** (source VM → destination VM). If a DFW rule ID is flagged:

```bash
# From NSX Manager REST API — get hit count for a specific rule
# GET https://<nsx-manager>/api/v1/firewall/stats/rules/<rule-id>

curl -sk -u admin:<password> \
  https://<nsx-manager>/api/v1/firewall/stats/rules/<rule-id> \
  | python3 -m json.tool
```

High hit-count rules on east-west traffic cause per-packet overhead. Reduce by:

- Consolidating rules with the same action and source/destination groups
- Adding a service exception for high-throughput backup or replication VMs
- Checking if a stateful DFW rule is logging every packet (disable logging if not needed)

---

## 5. PowerCLI — Pull Historical Performance Stats

Use PowerCLI to pull stats for the past hour without needing Aria Operations access.

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

## Common Mistakes

- **Checking vSAN before ESXi host metrics.** Always verify host-level CPU and memory first. vSAN can appear healthy while the host is CPU-starved, masking the real cause.
- **Ignoring CPU ready while focusing on guest CPU.** A guest OS showing 90% CPU usage may actually be waiting for physical CPU time — %RDY in esxtop tells the real story.
- **Overlooking DFW as a latency source.** East-west traffic between VMs on the same host still traverses the DFW kernel module. High rule counts add measurable overhead.
- **Forgetting resource pool limits.** A VM inside a resource pool with a hard CPU limit will show high CPU ready even on an otherwise idle host.

---

## Related Scenarios

- [vMotion Failing](../vmotion-failing/index.md) — vMotion failures often surface during performance investigations when DRS tries to rebalance a degraded host.
- [vSAN Disk or Component Failure](../vsan-disk-component-failure/index.md) — vSAN latency spikes are frequently caused by active component rebuild after a disk event.
- [NSX Connectivity Broken](../nsx-connectivity-broken/index.md) — When dropped packets point to the network layer, a full NSX path trace is the logical next step.
