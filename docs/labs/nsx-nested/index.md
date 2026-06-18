---
tags:
  - nsx
  - networking
  - vsphere
---
# Lab 3 — NSX-T in Nested ESXi

<div class="kb-summary">
Deploy NSX Manager into the Lab 1 nested environment, prepare ESXi transport nodes, create overlay segments, and configure a basic Distributed Firewall rule. Estimated time: 2–3 hours.
</div>

```text
┌──────────────────────────── NSX-T Nested Lab — Architecture ──────────────────────────────────────────┐
│  NSX Manager VM (16 GB RAM · single node for lab)                                                     │
│  Transport Nodes: ESXi-01 + ESXi-02 (NSX VIBs installed · Geneve TEP vmkernel)                        │
│  Overlay Segment → T1 Gateway (optional) → T0 Gateway → Edge VM (optional)                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

| Requirement | Value |
|---|---|
| Lab 1 | Completed: 2 nested ESXi hosts + vCenter |
| Additional RAM | 16 GB for NSX Manager (single lab node) |
| NSX Manager OVA | Download from VMware Customer Connect (NSX-T 3.x or 4.x) |
| DNS entry | Forward DNS for NSX Manager FQDN required |
| Physical portgroup | Promiscuous Mode + Forged Transmits: Accept (done in Lab 1) |

## What this lab builds

| Component | Purpose |
|---|---|
| NSX Manager (single node) | Control + management plane |
| Transport nodes (ESXi-01, ESXi-02) | Data plane — runs DFW and Geneve overlay |
| Overlay transport zone | Logical network space for Geneve segments |
| Overlay segment | Layer 2 segment for test VMs |
| DFW rule | Basic allow/deny between two VMs |
| Edge VM + T0/T1 (optional) | North-south routing outside the lab subnet |

## Phases

<div class="kb-grid">
<a class="kb-card" href="guide/">
<strong>Full Step-by-Step Guide</strong><br>
Deploy NSX Manager, add vCenter as compute manager, prepare transport nodes, create segments, and write a DFW rule.
</a>
</div>

## See also

- [Lab 1 — Nested ESXi Homelab](../nested-esxi/) — prerequisite
- [NSX Topology Decision Tree](../../reference/decision-trees/nsx-topology/)
- [NSX Cheat Sheet](../../reference/cheat-sheets/nsx/)
- [Network Interaction Map](../../reference/interaction-map/network/)
