# NSX — Architecture Overview

NSX is VMware's software-defined networking and security platform. It virtualises the network layer and enforces security at the hypervisor, decoupling networking from physical infrastructure.

| Component | Location | Role |
|---|---|---|
| NSX Manager (3-node cluster) | Management VMs | Management, control, and policy plane |
| Transport Nodes (ESXi hosts) | Every vSphere host | Data plane — overlay networking and DFW |
| Edge Nodes | Dedicated VMs or bare metal | North-south routing, NAT, LB, VPN |
| Tier-0 Gateway | Edge nodes | Physical network peering (BGP / static) |
| Tier-1 Gateway | ESXi hosts (distributed) | Per-tenant routing; no Edge required for L3 |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Manager cluster, transport nodes, Geneve encapsulation, T0/T1 gateways, DFW, segments, and VPN.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter, VCF, physical underlay, BGP, Active Directory, vDS, and SIEM.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, overlay design rules, firewall design, baselines, and version compatibility.</span></a>
</div>

---

## NSX Overlay Architecture

```mermaid
graph TB
  MGR["NSX Manager\n(3-node cluster)"] --> TN["Transport Nodes\n(ESXi hosts + Edge VMs)"]
  TN --> TZ["Transport Zones\n(Overlay + VLAN)"]
  TZ --> SEG["Segments\n(logical switches)"]
  SEG --> T1["Tier-1 Gateway\n(distributed routing per tenant)"]
  T1 --> T0["Tier-0 Gateway\n(north-south on Edge Nodes)"]
  T0 --> PHY["Physical Network\n(underlay — BGP / static)"]

  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff

  class MGR ctrl
  class TN,TZ net
  class SEG,T1,T0 net
  class PHY host
```
