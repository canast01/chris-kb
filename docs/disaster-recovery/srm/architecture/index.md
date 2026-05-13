# SRM — Architecture

<div class="kb-summary">
VMware Site Recovery Manager DR orchestration — vCenter plugin that automates storage presentation, VM registration, power-on sequencing, and IP customisation across a site pair.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Site pair topology, recovery plan boot sequence, recovery modes, SRAs, and vSphere Replication.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Dell EMC, Pure Storage, and NetApp SRA integrations; vSphere Replication appliance.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Protection group naming, recovery plan design, RPO targets, and test schedule.</span></a>
</div>

| Component | Role |
|---|---|
| SRM Server | Orchestration engine; deployed as vCenter plugin on each site |
| Site Pair | Bidirectional trust relationship between two SRM instances |
| Protection Group | Set of VMs or datastores failed over together |
| Recovery Plan | Ordered workflow: storage → VM registration → power-on tiers → IP customisation |
| SRA | Vendor plugin translating SRM commands to array replication APIs |
| vSphere Replication | Built-in per-VM replication; no SRA required; 5-minute minimum RPO |

```mermaid
graph LR
  VC_A["vCenter A\n+ SRM Server A + SRA"] --> STG_A[("Storage A")]
  VC_B["vCenter B\n+ SRM Server B + SRA"] --> STG_B[("Storage B")]
  VC_A <-->|"SRM pairing\nTCP 443 / 8095"| VC_B
  STG_A -->|"array replication\nor vSphere Replication"| STG_B
  H_A(["Production VMs\nSite A"]) --> VC_A
  H_B(["DR VMs\nSite B"]) -.-> VC_B
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VC_A ctrl
  class VC_B dr
  class STG_A,STG_B store
  class H_A host
  class H_B dr
```
