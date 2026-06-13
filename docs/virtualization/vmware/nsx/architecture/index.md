# NSX — Architecture

<div class="kb-summary">
NSX virtualises the network layer and enforces distributed security at the hypervisor. The 3-node NSX Manager cluster manages control and policy; Transport Nodes run the data plane; Edge Nodes handle north-south routing, NAT, and VPN.
</div>

![NSX Architecture Planes](../../../../assets/nsx-architecture-overview.svg)

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

