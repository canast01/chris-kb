# SRM — Architecture

<div class="kb-summary">
VMware Site Recovery Manager DR orchestration — vCenter plugin that automates storage presentation, VM registration, power-on sequencing, and IP customisation across a site pair.
</div>

```text
┌───────────────────────────────────────── SRM — Architecture ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRM — Component Architecture                                 │   │
│   │     SRM Server (Protected) — vCenter plugin at production site; manages protection groups     │   │
│   │            SRM Server (Recovery)  — vCenter plugin at DR site; runs recovery plans            │   │
│   │     SRA (Storage Replication Adapter) — translates SRM calls to array replication commands    │   │
│   │                Ports: 443 (SRM HTTPS) · 9086 (SRM-SRM pairing) · 443 (vCenter)                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three-tier component model — control plane, data plane, and management                             │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Control Plane        │  │          Data Plane         │  │          Management         │   │
│   │ SRM Server (Protected) — vCe│  │ SRM Server (Recovery)  — vCe│  │ Protection Group      — set │   │
│   │          Scheduling         │  │      Replication/Backup     │  │       443 (SRM HTTPS)       │   │
│   │         Policy mgmt         │  │        Data movement        │  │           REST API          │   │
│   │          Catalog/DB         │  │        Dedup/compress       │  │             RBAC            │   │
│   │          Job engine         │  │    9086 (SRM-SRM pairing)   │  │           Alerting          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![SRM Architecture](../../../assets/srm-architecture-overview.svg)

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


