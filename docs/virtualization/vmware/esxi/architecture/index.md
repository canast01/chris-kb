# ESXi — Architecture

<div class="kb-summary">
ESXi is VMware's Type-1 hypervisor. It is deployed in standalone, standard cluster, vSAN cluster, or stretched cluster configurations depending on resilience, storage, and scale requirements.
</div>

ESXi is VMware's Type-1 hypervisor. It is deployed in several cluster configurations depending on resilience, storage, and scale requirements.

| Cluster Type | Min Hosts | Storage | HA / DRS |
|---|---|---|---|
| Standalone | 1 | Local / external | No |
| Standard Cluster | 3+ | Shared SAN or NAS | Yes |
| vSAN Cluster | 3+ | Pooled from hosts (HCI) | Yes |
| Stretched Cluster | 4+ (2 per site) | vSAN stretched | Yes (site-level) |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>VMkernel, networking, storage paths, CPU/memory scheduling, HA/DRS, and boot architecture.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter, storage, network, backup, and monitoring integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Host naming, BIOS baseline, vmkernel layout, NTP, VIB policy, and cluster sizing.</span></a>
</div>

## ESXi Cluster Deployment Models

![ESXi Cluster Deployment Models](../../../../assets/esxi-architecture-overview.svg)

---

## Host Architecture

```mermaid
graph TB
  ESXI["ESXi Hypervisor\n(VMkernel)"]
  ESXI --> VMK0["vmk0 — Management"]
  ESXI --> VMK1["vmk1 — vMotion"]
  ESXI --> VMK2["vmk2 — vSAN / Storage"]
  ESXI --> VMS(["Virtual Machines"])
  ESXI --> VSWITCH["vSwitch / vDS\n(port groups)"]
  VSWITCH --> VMNIC["Physical NICs\nvmnic0 · vmnic1 · vmnic2 · vmnic3"]
  ESXI --> HBA["FC / NVMe HBAs\n(SAN connectivity)"]

  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff

  class ESXI ctrl
  class VMK0,VMK1,VMK2,VSWITCH,VMNIC,HBA net
  class VMS host
```
