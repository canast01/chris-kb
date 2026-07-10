---
tags:
  - vsphere
  - architecture
  - interaction-map
  - vmware
  - netapp
  - dell
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

## Full Stack Interaction Map

The diagram below covers all major platform categories — VMware, storage arrays, SAN fabric, backup/DR, automation, security, identity, and cloud — and the integration paths between them.

```d2
direction: right

vCenter: "vCenter Server" {shape: rectangle}
ESXi: "ESXi Hosts" {shape: rectangle}
vSAN: "vSAN" {shape: rectangle}
NSX: "NSX-T Manager" {shape: rectangle}
ONTAP: "NetApp ONTAP" {shape: rectangle}
PowerStore: "Dell PowerStore" {shape: rectangle}
FlashArray: "Pure FlashArray" {shape: rectangle}
MDS: "Cisco MDS (FC" {shape: rectangle}
Brocade: "Brocade FOS (FC" {shape: rectangle}
vDS: "vSphere vDS" {shape: rectangle}
Veeam: "Veeam B&R" {shape: rectangle}
CommVault: "CommVault" {shape: rectangle}
NetBackup: "Veritas NetBackup" {shape: rectangle}
SRM: "VMware SRM" {shape: rectangle}
SnapMirror: "SnapMirror" {shape: rectangle}
RecoverPoint: "RecoverPoint" {shape: rectangle}
Ansible: "Ansible" {shape: rectangle}
Terraform: "Terraform" {shape: rectangle}
PowerCLI: "PowerCLI" {shape: rectangle}
AriaAuto: "Aria Automation" {shape: rectangle}
VCF: "VCF / SDDC Mgr" {shape: rectangle}
AriaOps: "Aria Operations" {shape: rectangle}
AD: "Active Directory" {shape: rectangle}
CyberArk: "CyberArk PAM" {shape: rectangle}
Venafi: "Venafi TLS" {shape: rectangle}
AWS: "AWS" {shape: rectangle}
Azure: "Azure" {shape: rectangle}

vCenter -> ESXi
ESXi -> vSAN
NSX -> ESXi
ESXi -> ONTAP
ESXi -> PowerStore
ESXi -> FlashArray
vCenter -> vSAN
ESXi -> MDS
ESXi -> Brocade
vCenter -> vDS
ONTAP -> Veeam
PowerStore -> CommVault
FlashArray -> NetBackup
vSAN -> Veeam
SRM -> Veeam
ONTAP -> SnapMirror
PowerStore -> RecoverPoint
SRM -> vCenter
Ansible -> vCenter
Terraform -> vCenter
PowerCLI -> vCenter
AriaAuto -> vCenter
VCF -> vCenter
VCF -> NSX
VCF -> vSAN
AriaOps -> ESXi
AriaOps -> ONTAP
AriaOps -> NSX
AD -> vCenter
AD -> AriaOps
AD -> Veeam
CyberArk -> ESXi
CyberArk -> ONTAP
Venafi -> NSX
Venafi -> vCenter
AWS -> vCenter
Azure -> vCenter
SnapMirror -> AWS
```

## Integration Points by Layer

| Layer | Products | Connects To |
|-------|----------|-------------|
| **Compute** | ESXi, vCenter, NSX-T | Storage (NFS/iSCSI/NVMe-oF/vSAN), SAN (FC HBA), Management (vSphere API), Automation (REST/SDK), Identity (SAML/LDAP) |
| **Storage** | vSAN, NetApp ONTAP, Dell PowerStore, Pure FlashArray | Compute (VASA/SPBM/VMFS), SAN (FC/iSCSI), Backup (NDMP/snapshot API), DR (async replication), Management (VASA provider) |
| **SAN / Network** | Cisco MDS, Brocade FOS, vSphere vDS | Compute (FC zoning/HBA), Storage (FC fabric), Management (DCNM/REST API) |
| **Backup / DR** | Veeam, CommVault, NetBackup, SRM, SnapMirror, RecoverPoint | Compute (vSphere API, CBT), Storage (snapshot offload/NDMP), Cloud (offsite target), Identity (AD auth) |
| **Automation** | Ansible, Terraform, PowerCLI, Aria Automation | Compute (vSphere/REST API), Storage (array REST API), Network (NSX REST API), Management (SDDC Manager API) |
| **Management** | VCF, Aria Operations, Aria Automation | Compute, Storage, Network (full lifecycle and metrics across all layers) |
| **Security / Identity** | Active Directory, CyberArk PAM, Venafi | Compute (privileged access / cert push), Storage (array admin auth), Network (NSX cert management), Backup (AD auth) |
| **Cloud** | AWS, Azure | On-prem vCenter (VMware Cloud on AWS / AVS), Storage (SnapMirror Cloud), DR (cloud failover target) |

## See also

- [Cheat Sheets](../cheat-sheets/) — top-10 CLI commands per product
- [VCF Architecture](../../virtualization/vmware/products/vmware-cloud-foundation/architecture/)
- [NSX Architecture](../../virtualization/vmware/products/nsx/architecture/)
- [vSAN Architecture](../../virtualization/vmware/products/vsan/architecture/)
