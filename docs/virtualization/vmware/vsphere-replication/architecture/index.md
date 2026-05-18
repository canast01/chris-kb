# vSphere Replication — Architecture

<div class="kb-summary">
vSphere Replication is a hypervisor-based asynchronous replication solution managed by the VRMS appliance, providing VM-level RPO control without requiring SAN-based replication.
</div>

```
  Site A (Protected)            Site B (Recovery)
┌─────────────────────────┐    ┌─────────────────────────────┐
│  VR Appliance (VRMS)    │    │  VR Appliance (VRMS)        │
│  ┌───────────────────┐  │    │  ┌───────────────────────┐  │
│  │ Manages: RPO per  │◄─┼────┼─►│ Receives replica data │  │
│  │  VM, schedules,   │  │    │  │ Stores .vrepl VMDKs   │  │
│  │  recovery points  │  │    │  │ N instances per VM    │  │
│  └───────────────────┘  │    │  └───────────────────────┘  │
│                         │    │                             │
│  ESXi hosts             │    │  Optional VRS (scale-out)   │
│  ┌───────────────────┐  │    │  ┌───────────────────────┐  │
│  │  hbrsvc (per host)│──┼────┼─►│  +500 VMs per VRS     │  │
│  │  CBT delta tracks │  │    │  └───────────────────────┘  │
│  └───────────────────┘  │    │                             │
│  RPO: 5 min – 24 hrs    │    │  RPO compliance monitored   │
└─────────────────────────┘    └─────────────────────────────┘
```

![vSphere Replication Architecture](../../../../assets/vsphere-replication-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Architecture overview, topology, and how it fits in the stack.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and services.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, design rules, and configuration baselines.</span></a>
</div>
