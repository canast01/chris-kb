# vSAN — Architecture Overview

VMware supports four storage architectures. This section covers vSAN in depth.

| Architecture | Storage location | Shared across hosts | vMotion / HA / DRS |
|---|---|---|---|
| DAS | Local to host | No | No |
| SAN (FC / iSCSI / NVMe-oF) | External array | Yes | Yes |
| NAS (NFS / SMB) | External array | Yes | Yes |
| vSAN (HCI) | Pooled from hosts | Yes | Yes |

## VMware Storage Architecture

![VMware Storage Architecture](../../../../assets/vmware-storage-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Storage architecture modes, objects, data path, and core components.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter, NSX, File Services, and Aria Operations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Network requirements, storage policies, naming conventions, and capacity planning.</span></a>
</div>

---

## Cluster Topology

```mermaid
graph TB
  H1["ESXi-01\nCache NVMe + Capacity SSD"] & H2["ESXi-02\nCache NVMe + Capacity SSD"] & H3["ESXi-03\nCache NVMe + Capacity SSD"] --> VSANNET["vSAN VMkernel Network\n25 / 10 GbE dedicated"]
  VSANNET --> DS[("vSAN Datastore\nFTT policy — RAID-1 / RAID-5 / RAID-6")]
  DS --> VM(["VM Workloads"])
  VCSA["vCenter\n(vSAN management)"] --> VSANNET
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef store fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class H1,H2,H3 ctrl
  class VSANNET net
  class DS store
  class VM host
  class VCSA mgmt
```
