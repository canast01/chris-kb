# SnapCenter — Architecture

<div class="kb-summary">
SnapCenter architecture reference — topology, HA options, components, connectivity ports, plugin model, and sizing guidelines.
</div>

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

```mermaid
graph TB
  SCW["SnapCenter Server\n(Windows / Linux VM)"]
  SCW --> PL1["Plug-in for SQL Server"]
  SCW --> PL2["Plug-in for Oracle"]
  SCW --> PL3["Plug-in for VMware"]
  PL1 & PL2 & PL3 --> ONTAP["NetApp ONTAP\nSnapshot · SnapMirror · SnapVault"]
  ADMIN(["DBA / Storage Admin"]) -->|"web UI / REST API"| SCW
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class SCW,PL1,PL2,PL3 ctrl
  class ONTAP store
  class ADMIN host
```
