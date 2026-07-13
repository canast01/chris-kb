---
tags:
  - internals
  - vmware
description: "DRS evaluates cluster imbalance every 5 minutes using a per-host demand score against fair-share entitlement. Migrations are proposed or executed based on..."
---
# DRS Mechanics

<div class="kb-summary">
DRS evaluates cluster imbalance every 5 minutes using a per-host demand score against fair-share entitlement. Migrations are proposed or executed based on automation level and migration priority band. Predictive DRS extends this with Aria Operations forecasts.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

A: "A" {shape: rectangle}
B: "B" {shape: rectangle}
C: "C" {shape: rectangle}
D: "D" {shape: rectangle}
J: "J" {shape: rectangle}
H: "H" {shape: rectangle}
I: "I" {shape: rectangle}
E: "E" {shape: rectangle}
F: "F" {shape: rectangle}
G: "G" {shape: rectangle}

A -> B
B -> C
C -> D
C -> J
D -> H
H -> I
I -> E
H -> E
E -> F
E -> G
```

## Imbalance Score Calculation

DRS computes a **normalized imbalance score** per host each invocation cycle (every 5 minutes, or triggered by VM power-on, vMotion completion, or host join).

**CPU demand**: actual MHz consumed by all VMs on the host, including CPU ready and co-stop as demand pressure indicators.

**Memory demand**: active memory (working set) + memory overhead (VMX overhead + vMMU overhead). Balloon driver and swap activity increase effective demand.

**Fair share**: total cluster demand ÷ number of hosts, weighted by host capacity (heterogeneous clusters weight by MHz and GB).

**Imbalance score** = deviation of host demand from fair share. DRS aggregates CPU and memory deviations into a composite score using an internal weighting (VMware does not publish the exact formula; behavior is observable via DRS recommendations in "show all recommendations" mode).

**Threshold mapping:**

| DRS Migration Threshold | Aggressiveness | Description |
|--------------------------|---------------|-------------|
| 1 (Conservative) | Only critical imbalances | Migrates only when imbalance is severe |
| 2 | Less aggressive | Migrates for moderate-to-severe imbalance |
| 3 (Default) | Aggressive | Migrates if any imbalance benefit detected |
| 4 | More aggressive | Migrates for marginal gains |
| 5 (Aggressive) | Maximum | Migrates whenever any positive balance score |

## Migration Priority Bands

Each DRS recommendation has a priority band that determines whether it executes automatically under "Partially Automated" mode.

| Priority Band | Label | Auto-execute (Partial)? | Description |
|---------------|-------|------------------------|-------------|
| 1 | Mandatory | Yes | Required to power on VM (no other host available) |
| 2 | High | Yes | High imbalance reduction benefit |
| 3 | Medium | No | Moderate benefit |
| 4 | Low | No | Minor benefit |
| 5 | Very Low | No | Negligible benefit |

Under **Fully Automated**, DRS executes all priority bands without confirmation. Under **Manual**, no band auto-executes — all appear as recommendations in the vSphere Client.

## Reservation vs Entitlement

DRS distinguishes between what a VM is *guaranteed* and what it is *entitled to receive*:

| Concept | Definition | DRS impact |
|---------|-----------|-----------|
| Reservation | Hard lower bound on CPU/memory — always guaranteed | Host must have sufficient unreserved capacity to admit VM |
| Limit | Hard upper bound — VM never exceeds this | Limits effective demand used in imbalance calculation |
| Share | Relative weight for CPU/memory contention | Determines entitlement when resources are contested |
| Entitlement | Computed fair allocation based on shares + reservation | DRS balances actual demand vs entitlement per host |
| Memory overhead | VMkernel overhead per VM (VMX process, vMMU, VMCS) | Counted as consumed memory; included in demand |
| Balloon / swap | Memory reclamation signals | Balloon indicates memory pressure; included in demand signal |

A VM with a large CPU reservation inflates the host's committed capacity even if the VM is idle. DRS counts reservations as consumed for admission control purposes but uses actual demand for balance scoring.

## Initial Placement

When a VM powers on, DRS scores every host in the cluster and selects the optimal target:

1. **Constraint pass**: eliminate hosts violating affinity/anti-affinity rules, DRS-disabled hosts, hosts in maintenance mode, hosts with insufficient reserved capacity.
2. **Feasibility pass**: eliminate hosts that cannot satisfy VM reservations given current committed capacity.
3. **Score pass**: rank remaining hosts by projected imbalance after VM placement; select the host that produces the most balanced cluster state.
4. **Rule enforcement**: VM-to-VM affinity (must run on same host), VM-to-host affinity (must run on host group).

## Predictive DRS

Predictive DRS requires Aria Operations (formerly vRealize Operations) integrated with vCenter.

| Component | Role |
|-----------|------|
| Aria Operations | Builds time-series demand model per VM; forecasts future demand spikes |
| vCenter DRS | Receives forecast data from Aria; pre-migrates VMs before predicted load |
| Integration | Aria pushes recommendations to vCenter via REST API integration (configured in Aria administration) |
| Lead time | Aria forecasts up to 60 min ahead; DRS acts early to avoid reactively chasing spikes |

Predictive DRS does not replace reactive DRS — both run simultaneously. Predictive recommendations appear with "Predictive DRS" label in DRS recommendations panel.

## DRS Behavior by Automation Level

| Level | Initial Placement | Rebalance Migrations | Manual Override |
|-------|-------------------|---------------------|-----------------|
| Disabled | Manual host selection | No DRS migrations | N/A |
| Manual | DRS suggests; user confirms | Recommendations only; user applies | Always required |
| Partially Automated | DRS places automatically | Priority 1–2 auto; 3–5 as recommendations | For lower priority |
| Fully Automated | DRS places automatically | All priorities auto-executed | Not required; user can still migrate |

## DRS and vSAN Stretched Cluster

On a vSAN stretched cluster, DRS enforces **site affinity** automatically:

- Each site has a VM-Host group (`site-a-hosts`, `site-b-hosts`) and a corresponding VM group (`site-a-vms`).
- VM-Host affinity rules (should / must) bind VM groups to host groups.
- DRS will not migrate a VM across sites if a "must" affinity rule binds it to one site's host group.
- During a site failure, HA restarts VMs on the surviving site; DRS does not re-balance back to the recovered site until the admin manually rebalances or removes the affinity constraint.
- Cross-site vMotion is blocked by "must" rules; use "should" rules if you need DRS to make cross-site moves in edge cases.

## Edge Cases and Constraints

**Pinned VMs (DRS disabled per-VM):**
Set `VM → Edit Settings → DRS Automation → Disabled`. DRS ignores the VM for balance calculations but still considers its reserved capacity when scoring other placements.

**Latency-sensitive VMs:**
Latency-sensitive VMs use CPU reservation pinning (SMP scheduler reserves pCPUs). DRS avoids migrating these because vMotion interrupts NUMA locality; if migration is necessary, DRS selects a host with matching NUMA topology.

**EVC clusters:**
EVC (Enhanced vMotion Compatibility) masks CPU features to the lowest common denominator in the cluster. DRS can vMotion VMs to any host in the EVC cluster regardless of CPU generation. EVC mode must be set before adding older hosts; changing EVC requires all VMs powered off.

**vMotion cost:**
DRS assigns a cost to each migration (CPU and network load of vMotion). The benefit of balancing must exceed this cost; DRS will not propose a migration that produces marginal balance improvement at high vMotion cost (e.g., moving a very large memory VM).

---

## See also

- [HA Deep Dive — Internals](../ha-deep-dive/)
- [Cluster Services — Internals](../cluster-services/)
- [Resource Management — Internals](../vsphere-resource-management/)
