---
tags:
  - architecture
  - netapp
---
# ONTAP — Architecture

<div class="kb-summary">
ONTAP architecture reference — HA topology, WAFL filesystem engine, SVM design, cluster networking, protocol stack, and data protection built-ins.

*Applies to: ONTAP 9.x*
</div>

![ONTAP Architecture](../../../../assets/ontap-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>HA topology, WAFL engine, cluster networking, SVM architecture, protocols, and data protection.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware, SnapCenter, Active Directory, Veeam, REST API, and cloud integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, sizing guidelines, and configuration checklist.</span></a>
</div>

| Platform | Storage Type | Target Workload |
|---|---|---|
| AFF (All Flash FAS) | All-NVMe or all-SSD | Latency-sensitive databases, VDI, high-IOPS workloads |
| FAS (Fabric-Attached Storage) | Hybrid flash/disk | Capacity-optimised, mixed, file, and backup workloads |
| ONTAP Select | Software-defined on x86 | Edge, ROBO, dev/test; VMware or KVM hypervisor |

```mermaid
graph TB
  N1["Node 1 (Controller)\nSVM-1 · SVM-2"] <-->|"HA interconnect\n100GbE cluster net"| N2["Node 2 (Controller)\n(takeover on failover)"]
  N1 & N2 --> SHELVES[("Disk Shelves\nNVMe SSD / SAS HDD")]
  N1 --> NAS["NFS · SMB/CIFS"]
  N1 --> SAN["iSCSI · FC · NVMe-oF"]
  N2 --> NAS & SAN
  NAS --> NC(["NAS Clients"])
  SAN --> SC(["SAN Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2 ctrl
  class SHELVES store
  class NC,SC host
```
