---
tags:
  - architecture
  - netapp
---
# SnapCenter — Architecture

<div class="kb-summary">
SnapCenter architecture reference — topology, HA options, components, connectivity ports, plugin model, and sizing guidelines.

*Applies to: SnapCenter 5.x*
</div>

![SnapCenter — Architecture — Diagram](../../../../assets/storage-netapp-snapcenter-architecture-diagram.svg)

```d2
direction: right

SCW: "SnapCenter Server\n(Windows / Linux VM" {shape: rectangle}
PL1: "Plug-in for SQL Server" {shape: rectangle}
PL2: "Plug-in for Oracle" {shape: rectangle}
PL3: "Plug-in for VMware" {shape: rectangle}
ONTAP: "NetApp ONTAP\nSnapshot · SnapMirror · SnapVault" {shape: rectangle}
ADMIN: "DBA / Storage Admin" {shape: rectangle}

SCW -> PL1
SCW -> PL2
SCW -> PL3
PL1 -> PL2
PL2 -> PL3
PL3 -> ONTAP
ADMIN -> SCW
```
![SnapCenter Architecture](../../../../assets/snapcenter-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Topology, HA options, components, connectivity ports, plugins, and sizing guidelines.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with ONTAP, VMware, Active Directory, and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
</div>

| Component | Platform | Notes |
|---|---|---|
| SnapCenter Server | Windows Server 2019/2022 VM | Web GUI (8146), REST API, scheduler; 4 vCPU/8GB min |
| Repository Database | MySQL (local or HA cluster) | Stores job history, policies, resource groups, RBAC |
| SnapCenter Agent | Windows or Linux service | Port 8145; installed on each protected host |
| Plug-in for VMware | OVA appliance (per vCenter) | VM and datastore backup without in-guest agents |

