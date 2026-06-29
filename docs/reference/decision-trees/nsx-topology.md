---
tags:
  - nsx
  - networking
  - architecture
---
# NSX Topology Decision Tree

*Applies to: All products*

<div class="kb-summary">
Design your NSX topology: overlay vs VLAN transport, T0/T1 gateway placement, Edge cluster sizing, HA model, and north-south routing type.
</div>

```d2
direction: right

B: "B" {shape: rectangle}
D: "Single T0 gateway\nMultiple T1s per workload zone" {shape: rectangle}
C: "C" {shape: rectangle}
E: "VRF-Lite on shared T0\nOne routing table per VRF" {shape: rectangle}
F: "Dedicated T0 per tenant\nSeparate Edge cluster per tenant" {shape: rectangle}
G: "G" {shape: rectangle}
H: "Static routes on T0\nNo BGP · manual route config" {shape: rectangle}
I: "eBGP on T0 uplinks\nPeer with ToR switches\nBFD for fast failover" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Edge VM — Small\n2 vCPU · 4 GB RAM" {shape: rectangle}
L: "Edge VM — Large\n8 vCPU · 32 GB RAM" {shape: rectangle}
M: "Bare-metal Edge node\nDPDK · SR-IOV NIC required" {shape: rectangle}
N: "N" {shape: rectangle}
O: "Active/Standby T0\nOne active Edge at a time\nFast failover via BFD" {shape: rectangle}
P: "ECMP Active/Active\n2–8 equal-cost paths\nRequires BGP · stateless DFW" {shape: rectangle}
A: "Start: Design NSX Topology" {shape: rectangle}

B -> D
C -> E
C -> F
E -> G
F -> G
G -> H
G -> I
I -> J
J -> K
J -> L
J -> M
L -> N
M -> N
N -> O
N -> P
```

## Key design decisions

| Decision | Option A | Option B | Tiebreaker |
|---|---|---|---|
| Tenant model | VRF-Lite (shared T0) | Dedicated T0 per tenant | Strict compliance → dedicated |
| Routing | Static routes | eBGP to ToR | Production → always BGP |
| Edge size | VM (Small/Large) | Bare-metal | >25 Gbps → bare-metal |
| T0 HA | Active/Standby | ECMP | Stateful NAT → Active/Standby |

## Important constraints

- **ECMP** requires BGP — you cannot use ECMP with static routes on a T0.
- **Stateful services** (NAT, LB, VPN) **pin to one Edge** even in ECMP — service traffic uses only the active Edge for that service.
- **Bare-metal Edge** requires a dedicated physical server — cannot share with ESXi hypervisor workloads.
- **VRF-Lite** on a T0 requires NSX 3.1+ and separate uplink interfaces per VRF.
- Minimum Edge cluster size for production: **2 nodes** (HA). For ECMP: **2–8 nodes**.

## See also

- [NSX Cheat Sheet](../../cheat-sheets/nsx/)
- [NSX Architecture](../../../virtualization/vmware/nsx/architecture/)
- [NSX Network Interaction Map](../../interaction-map/network/)
- [Back to Decision Trees](index.md)
