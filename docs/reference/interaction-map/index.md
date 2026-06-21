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

```mermaid
graph LR
    %% ── Compute ─────────────────────────────────────────────
    ESXi["ESXi Hosts"]
    vCenter["vCenter Server"]
    NSX["NSX-T Manager"]

    %% ── Storage ─────────────────────────────────────────────
    vSAN["vSAN"]
    ONTAP["NetApp ONTAP"]
    PowerStore["Dell PowerStore"]
    FlashArray["Pure FlashArray"]

    %% ── SAN / Network ───────────────────────────────────────
    MDS["Cisco MDS (FC)"]
    Brocade["Brocade FOS (FC)"]
    vDS["vSphere vDS"]

    %% ── Backup ──────────────────────────────────────────────
    Veeam["Veeam B&R"]
    CommVault["CommVault"]
    NetBackup["Veritas NetBackup"]

    %% ── DR ──────────────────────────────────────────────────
    SRM["VMware SRM"]
    SnapMirror["SnapMirror"]
    RecoverPoint["RecoverPoint"]

    %% ── Automation ──────────────────────────────────────────
    Ansible["Ansible"]
    Terraform["Terraform"]
    PowerCLI["PowerCLI"]

    %% ── Management ──────────────────────────────────────────
    VCF["VCF / SDDC Mgr"]
    AriaOps["Aria Operations"]
    AriaAuto["Aria Automation"]

    %% ── Security / Identity ─────────────────────────────────
    AD["Active Directory"]
    CyberArk["CyberArk PAM"]
    Venafi["Venafi TLS"]

    %% ── Cloud ───────────────────────────────────────────────
    AWS["AWS"]
    Azure["Azure"]

    %% ── Compute ↔ Compute internals ────────────────────────
    vCenter -->|"vSphere API / VPXA"| ESXi
    ESXi -->|"DPU / kernel modules"| vSAN
    NSX -->|"GENEVE overlay / DFW"| ESXi

    %% ── Compute ↔ Storage ───────────────────────────────────
    ESXi -->|"NFS / iSCSI / VMFS"| ONTAP
    ESXi -->|"iSCSI / NVMe-oF"| PowerStore
    ESXi -->|"iSCSI / NVMe-oF"| FlashArray
    vCenter -->|"VASA / SPBM"| vSAN

    %% ── Compute ↔ SAN ───────────────────────────────────────
    ESXi -->|"FC HBA / zoning"| MDS
    ESXi -->|"FC HBA / zoning"| Brocade
    vCenter -->|"vDS port groups"| vDS

    %% ── Storage ↔ Backup ────────────────────────────────────
    ONTAP -->|"NDMP / Snapshot"| Veeam
    PowerStore -->|"API snapshots"| CommVault
    FlashArray -->|"API snapshots"| NetBackup
    vSAN -->|"changed-block API"| Veeam

    %% ── Backup ↔ DR ─────────────────────────────────────────
    SRM -->|"replication policy"| Veeam
    ONTAP -->|"async replication"| SnapMirror
    PowerStore -->|"async replication"| RecoverPoint
    SRM -->|"orchestrates failover"| vCenter

    %% ── Automation ↔ Compute ────────────────────────────────
    Ansible -->|"VMware modules"| vCenter
    Terraform -->|"vsphere provider"| vCenter
    PowerCLI -->|"PowerShell SDK"| vCenter
    AriaAuto -->|"IaaS blueprint"| vCenter

    %% ── Management orchestration ────────────────────────────
    VCF -->|"lifecycle API"| vCenter
    VCF -->|"lifecycle API"| NSX
    VCF -->|"lifecycle API"| vSAN
    AriaOps -->|"metrics / health"| ESXi
    AriaOps -->|"metrics / health"| ONTAP
    AriaOps -->|"metrics / health"| NSX

    %% ── Identity everywhere ──────────────────────────────────
    AD -->|"SAML / LDAP"| vCenter
    AD -->|"LDAP"| AriaOps
    AD -->|"LDAP"| Veeam
    CyberArk -->|"privileged sessions"| ESXi
    CyberArk -->|"privileged sessions"| ONTAP
    Venafi -->|"cert lifecycle"| NSX
    Venafi -->|"cert lifecycle"| vCenter

    %% ── Cloud connectivity ───────────────────────────────────
    AWS -->|"VMware Cloud on AWS"| vCenter
    Azure -->|"AVS / ExpressRoute"| vCenter
    SnapMirror -->|"Cloud Sync"| AWS

    %% ── Class definitions ───────────────────────────────────
    classDef compute fill:#1565C0,color:#fff,stroke:#0D47A1
    classDef storage fill:#2E7D32,color:#fff,stroke:#1B5E20
    classDef san    fill:#E65100,color:#fff,stroke:#BF360C
    classDef backup fill:#6A1B9A,color:#fff,stroke:#4A148C
    classDef dr     fill:#7B1FA2,color:#fff,stroke:#4A148C
    classDef auto   fill:#00695C,color:#fff,stroke:#004D40
    classDef mgmt   fill:#546E7A,color:#fff,stroke:#37474F
    classDef sec    fill:#B71C1C,color:#fff,stroke:#7F0000
    classDef cloud  fill:#455A64,color:#fff,stroke:#263238

    class ESXi,vCenter,NSX compute
    class vSAN,ONTAP,PowerStore,FlashArray storage
    class MDS,Brocade,vDS san
    class Veeam,CommVault,NetBackup backup
    class SRM,SnapMirror,RecoverPoint dr
    class Ansible,Terraform,PowerCLI,AriaAuto auto
    class VCF,AriaOps mgmt
    class AD,CyberArk,Venafi sec
    class AWS,Azure cloud
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
- [VCF Architecture](../../virtualization/vmware/vmware-cloud-foundation/architecture/)
- [NSX Architecture](../../virtualization/vmware/nsx/architecture/)
- [vSAN Architecture](../../virtualization/vmware/vsan/architecture/)
