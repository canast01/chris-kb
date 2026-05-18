# Site Recovery Manager — Architecture

<div class="kb-summary">
VMware Site Recovery Manager automates DR failover and failback by orchestrating protection groups, recovery plans, and vSphere Replication or SAN-based replication.
</div>

```
  Protected Site           Replication Channel         Recovery Site
┌────────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  SRM Server        │────►│ vSphere Repl OR  │────►│  SRM Server        │
│  ┌──────────────┐  │     │ SAN Array SRA    │     │  ┌──────────────┐  │
│  │ Protection   │  │     └──────────────────┘     │  │ Recovery     │  │
│  │ Groups       │  │                              │  │ Plans        │  │
│  │ (VMs + RPO)  │  │     ┌──────────────────┐     │  │ (priority    │  │
│  └──────────────┘  │     │  Site Pairing    │     │  │  groups)     │  │
│                    │◄───►│  TCP 443 / 9086  │◄───►│  └──────────────┘  │
│  vCenter           │     └──────────────────┘     │  vCenter           │
│  (protected)       │                              │  (recovery)        │
└────────────────────┘                              └────────────────────┘
```

![Site Recovery Manager Architecture](../../../../assets/srm-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Architecture overview, topology, and how it fits in the stack.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and services.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, design rules, and configuration baselines.</span></a>
</div>
