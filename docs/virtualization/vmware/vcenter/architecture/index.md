# vCenter — Architecture

<div class="kb-summary">
vCenter Server is the management plane for VMware vSphere, deployed as the VCSA appliance. It supports standard single-node, vCenter HA (3-node active/passive/witness), and Enhanced Linked Mode topologies.
</div>

vCenter Server is the management plane for VMware vSphere. It is deployed as the VCSA appliance and supports several topology options depending on scale and resilience requirements.

| Deployment | Description | Use Case |
|---|---|---|
| Standard VCSA | Single appliance, embedded PSC and DB | Standard production |
| vCenter HA (VCHA) | Active / Passive / Witness — 3 nodes | HA for the management plane |
| Enhanced Linked Mode | Multiple vCenters sharing one SSO domain | Multi-site / large-scale |
| vCenter Cloud Gateway | Connects on-prem to VMware Cloud | Hybrid cloud |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Core services, VCHA, logical hierarchy, service startup order, sizing, ports, and logs.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Storage, NSX, identity, backup, and monitoring integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, cluster baseline, HA/DRS settings, VM standards, and snapshot policy.</span></a>
</div>

---

## vSphere Cluster Topology

```mermaid
graph TB
  VCSA["vCenter Server Appliance\n(VCSA)"] --> CL["vSphere Cluster\nDRS · HA enabled"]
  VCSA --> LCM["Lifecycle Manager\n(patching)"]
  VCSA --> NSX["NSX Manager\n(optional)"]
  CL --> ESX1["ESXi-01"] & ESX2["ESXi-02"] & ESX3["ESXi-03"] & ESX4["ESXi-04"]
  ESX1 & ESX2 & ESX3 & ESX4 --> VDS["vSphere Distributed Switch\nVM Net · vMotion · Storage · Mgmt"]
  VDS --> STORE["Shared Storage\nFlashArray · vSAN · NFS"]

  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef store fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff

  class VCSA,LCM,NSX mgmt
  class CL,VDS net
  class ESX1,ESX2,ESX3,ESX4 ctrl
  class STORE store
```
