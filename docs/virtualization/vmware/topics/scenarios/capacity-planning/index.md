# Capacity Planning

<div class="kb-summary">
Capacity planning is deciding when to add compute or storage resources before performance degrades
or space runs out — not after. Aria Operations is the primary tool: it provides time-remaining
projections, reclaimable waste identification, and what-if modelling. This scenario walks through
the full capacity review workflow, from checking raw headroom to making a justified hardware
procurement decision.
</div>

```text
┌──────────────────────────────── Capacity Planning — Review Workflow ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Scheduled capacity review, or approaching threshold alert from Aria Operations                   ││
│   └─────────────────────────────────────┬────────────────────────────────────────────────────────────────────┘│
│                                         │                                                             │
│                    ┌────────────────────┼────────────────────┐                                        │
│                    ▼                    ▼                    ▼                                        │
│   ┌────────────────────────┐  ┌──────────────────────┐  ┌────────────────────────┐                    │
│   │  vSAN storage headroom │  │  Compute headroom    │  │  Aria Ops time-        │                    │
│   │  — check used vs total │  │  — CPU and RAM after │  │  remaining projections │                    │
│   │  — 70% warning         │  │    HA reservation    │  │  — 90-day trend        │                    │
│   └───────────┬────────────┘  └──────────┬───────────┘  └───────────┬────────────┘                    │
│               └─────────────────────────┬┘──────────────────────────┘                                 │
│                                         ▼                                                             │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Check reclaimable waste first — powered-off VMs, oversized VMs, orphaned VMDKs                         ││
│   └─────────────────────────────────────┬────────────────────────────────────────────────────────────────────┘│
│                                         │                                                             │
│                    ┌────────────────────┼──────────────────────┐                                      │
│                    ▼                                           ▼                                      │
│   ┌────────────────────────────────────┐        ┌─────────────────────────────────────┐               │
│   │  Waste reclaimed — headroom        │        │  Waste already optimised — headroom │               │
│   │  restored, no hardware needed yet  │        │  still insufficient: order node     │               │
│   └────────────────────────────────────┘        └─────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| Aria Operations | Primary capacity analytics: time remaining, reclaimable waste, what-if analysis, trending |
| vCenter Server | Cluster CPU and RAM inventory; HA admission control effective capacity |
| vSAN | Storage capacity used vs total; slack space; capacity trending on the vSAN datastore |
| VxRail Manager | Node expansion wizard for HCI clusters — do not add nodes outside VxRail Manager |

---

## 1. Check vSAN Storage Headroom

The hard rule for vSAN production clusters: **never exceed 70% used capacity**. At 80%, vSAN stops
accepting new writes. At 100%, the datastore is read-only and VMs freeze.

```powershell
# Get vSAN datastore capacity via PowerCLI
Get-Datastore | Where-Object {$_.Type -eq "vsan"} | Select Name,
  @{N="CapacityGB";E={[math]::Round($_.CapacityGB,1)}},
  @{N="FreeSpaceGB";E={[math]::Round($_.FreeSpaceGB,1)}},
  @{N="UsedPct";E={[math]::Round((($_.CapacityGB - $_.FreeSpaceGB) / $_.CapacityGB) * 100, 1)}}
```

From the vCenter UI: **Cluster → Monitor → vSAN → Capacity**. Review:

- **Used**: current capacity consumed including mirror/parity overhead
- **Total**: raw usable capacity after FTT policy deduplication/compression
- **Slack**: free space available for writes and resync

| Usage level | Status | Action |
|---|---|---|
| < 70% | Healthy | No action required |
| 70–80% | Warning | Order expansion hardware now |
| > 80% | Critical — stop new VMs | Emergency: reclaim or expand immediately |

---

## 2. Check Compute Headroom (CPU and RAM)

HA admission control reserves a portion of cluster CPU and RAM for failover. The effective capacity
reported by vCenter already accounts for this reservation — compare effective capacity against
actual usage to find real headroom.

```powershell
# Cluster effective CPU and memory after HA reservation
Get-Cluster "cluster-name" | Select Name,
  @{N="EffectiveCPUMHz";E={($_ | Get-View).Summary.EffectiveCpu}},
  @{N="EffectiveMemMB";E={($_ | Get-View).Summary.EffectiveMemory}}

# Current actual usage across all hosts in the cluster
Get-Cluster "cluster-name" | Get-VMHost |
  Measure-Object -Property CpuUsageMhz, MemoryUsageMB -Sum |
  Select Property, Sum
```

If current usage exceeds 80% of effective capacity on either CPU or memory, the cluster is at risk
of resource contention during a host failure (HA failover reduces available capacity further).

---

## 3. Aria Operations Capacity View

Aria Operations provides the most actionable capacity view because it combines current usage,
growth trending, and reclaimable waste in one place.

Navigate to: **Aria Operations → Capacity → Clusters → select cluster → Capacity Remaining**.

Key metrics to review:

- **Time Remaining**: days until the cluster runs out of CPU, RAM, or storage at the current growth
  rate. Below 90 days is a trigger to start hardware procurement.
- **Reclaimable Waste**: capacity that can be recovered without purchasing hardware — oversized VMs,
  idle VMs, reclaimed snapshots.
- **What-If Analysis**: models the impact of adding a workload (how many days does adding 10 new
  VMs reduce time remaining?) or a node (how much headroom does a new host add?).

---

## 4. Trending — 90-Day Growth Analysis

A single point-in-time reading is not enough. Look at the slope of growth over 90 days.

Aria Operations → **Capacity** → select the vSAN datastore → **Historical** → set time range to
90 days. Compare the growth slope:

- **Linear growth**: predictable — use the slope to project when 70% will be hit.
- **Accelerating growth**: new workloads being added faster than expected — revise the order
  timeline forward.
- **Flat**: no growth. Check whether new VMs are being deployed on this cluster at all.

---

## 5. Check Reclaimable Resources Before Ordering Hardware

Before submitting a hardware request, check Aria Operations for waste. Reclaimable capacity is
free — it does not require procurement or a change window.

```powershell
# Find powered-off VMs still consuming VMDK space
Get-VM | Where-Object {$_.PowerState -eq "PoweredOff"} |
  Select Name, ProvisionedSpaceGB,
  @{N="DaysSincePoweredOff";E={(Get-Date) - $_.ExtensionData.Runtime.PowerOffTime | Select -Expand Days}}

# Find VMs with snapshots (snapshots consume storage continuously)
Get-VM | Get-Snapshot | Select VM, Name, SizeGB, Created
```

Common sources of reclaimable waste:

| Waste type | How to find | Action |
|---|---|---|
| Powered-off VMs | PowerCLI above / Aria Ops → Waste | Confirm with owner, delete if stale |
| Oversized vCPU or RAM | Aria Ops → Rightsizing recommendations | Reduce reservation to match actual usage |
| Orphaned VMDKs | vCenter → Datastore → Files → search for .vmdk with no associated VM | Delete after confirming no VM ownership |
| Old snapshots | Get-Snapshot / Aria Ops waste | Consolidate or delete snapshots > 7 days old |

---

## 6. Node Expansion Decision

Use these trigger points to decide when a node expansion is justified:

| Metric | Warning threshold | Action required threshold |
|---|---|---|
| vSAN capacity used | > 70% | > 80% — emergency |
| Cluster CPU (effective) | > 75% sustained | > 85% |
| Cluster RAM (effective) | > 80% sustained | > 90% |
| CPU ready (cluster avg) | > 3% | > 5% |
| Memory ballooning | Intermittent on 1–2 hosts | Active on multiple hosts |
| Time remaining (Aria Ops) | < 90 days | < 45 days |

Document the specific metrics that triggered the decision. Procurement teams require justification
and capacity data, not just "the cluster is getting full."

---

## 7. VxRail Node Expansion

For VxRail HCI clusters, all node additions must go through **VxRail Manager**:

VxRail Manager → **Cluster** → **Expand Cluster** → follow the node expansion wizard.

VxRail Manager validates that the new node matches the cluster's VxRail bundle (ESXi version,
firmware, driver stack), adds the node to vSAN with the correct disk claim policy, and verifies
the post-expansion vSAN health. **Do not add a node to a VxRail cluster via vCenter directly.**
Doing so skips firmware validation, may apply an incorrect VxRail personality, and breaks
the supportability of the cluster.

---

## Post-Task Validation

After adding capacity (hardware or reclamation), verify the following:

| Check | Location | Expected Result |
|---|---|---|
| vSAN used % dropped | vCenter → vSAN → Capacity | Below 70% |
| Aria Ops time remaining updated | Aria Ops → Capacity → Clusters | Value increased |
| vSAN health green | vCenter → vSAN → Skyline Health | All green |
| New node visible in cluster | vCenter inventory | Host Connected, in cluster |
| DRS rebalanced after node add | vCenter → DRS → Recommendations | No pending recommendations |

---

## Common Mistakes

- **Reacting at 80% instead of 70%.** vSAN stops writes at 80%. By the time the alert fires at 80%,
  there is no buffer remaining. Monitor at 70% and act before reaching 80%.
- **Ordering hardware before checking waste.** Aria Ops reclaimable waste recommendations frequently
  recover 10–20% of cluster capacity at zero cost. Always check waste first.
- **Adding a VxRail node via vCenter.** VxRail nodes added outside VxRail Manager miss firmware
  alignment, break the validated bundle, and may cause vSAN instability.
- **Using point-in-time capacity readings.** A cluster at 65% today with accelerating growth hits
  80% in weeks. Always review the 90-day trend, not just the current percentage.

---

## Related Scenarios

- Host Maintenance and Patching
- VxRail LCM Upgrade Failure
- Provision a New Workload
