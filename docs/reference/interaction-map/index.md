---
tags:
  - vsphere
  - architecture
---
# VMware Product Interaction Map

<div class="kb-summary">
How VMware's 15 core products connect — compute, storage, network, management, and automation layers with key integration protocols.
</div>

![VMware Product Interaction Map](../../assets/interaction-map-master.svg)

The five domains stack vertically: **Management** (VCF, Aria Suite Lifecycle) orchestrates everything below it. **Compute** (ESXi, vCenter, PowerCLI) is the execution layer. **Storage** (vSAN, vSphere Replication, VxRail) runs inside ESXi or as managed HCI. **Network** (NSX, vDS) runs as ESXi kernel modules and edge VMs. **Automation** (Aria Suite, Tanzu, Horizon) consumes all layers through APIs.

## Domain interaction maps

<div class="kb-grid">
<a class="kb-card" href="compute/">
<strong>Compute</strong><br>
ESXi, vCenter, and PowerCLI — vSphere API, hostd, and govmomi protocol details.
</a>
<a class="kb-card" href="network/">
<strong>Network</strong><br>
NSX and vDS — GENEVE overlay, BGP/ECMP uplinks, and DFW integration points.
</a>
<a class="kb-card" href="storage/">
<strong>Storage</strong><br>
vSAN, vSphere Replication, and VxRail — kernel modules, SPBM, and replication protocols.
</a>
<a class="kb-card" href="management/">
<strong>Management</strong><br>
VCF, Aria Suite Lifecycle, and vCenter SSO — lifecycle APIs and auth federation.
</a>
<a class="kb-card" href="automation/">
<strong>Automation</strong><br>
Aria Suite, Tanzu, and Horizon — how each product consumes the vSphere and NSX APIs.
</a>
</div>

## Key principles

- **VCF manages all layers**: a single SDDC Manager API call can deploy a full workload domain (vCenter + NSX + vSAN).
- **vSAN and NSX are kernel-native**: no separate appliances — both run as VIBs/modules inside each ESXi host.
- **vCenter SSO federates auth**: NSX Manager, Aria Operations, vRA, and Horizon all authenticate via vCenter SSO SAML tokens.
- **Aria Suite Lifecycle deploys Aria**: vROps, vRLI, vRNI, and vRA are all installed and upgraded through LCM — never manually.
- **Tanzu and Horizon sit at the top**: both provision infrastructure by calling the vSphere and vCenter APIs underneath.

## See also

- [Cheat Sheets](../cheat-sheets/) — top-10 CLI commands per product
- [VCF Architecture](../../virtualization/vmware/vmware-cloud-foundation/architecture/)
- [NSX Architecture](../../virtualization/vmware/nsx/architecture/)
- [vSAN Architecture](../../virtualization/vmware/vsan/architecture/)
