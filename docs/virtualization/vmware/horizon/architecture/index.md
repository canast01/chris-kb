# Horizon (VDI) — Architecture

<div class="kb-summary">
VMware Horizon delivers virtual desktops and published applications through Connection Servers, Unified Access Gateways, and desktop pools backed by vSphere.
</div>

```
  Control Plane                   Data Plane
┌──────────────────────────┐    ┌──────────────────────────────────────────┐
│  Pod Manager / CPA       │    │  ESXi Cluster — Desktop Pool             │
│  ┌────────────────────┐  │    │  ┌─────────────┐  ┌─────────────────┐    │
│  │  Connection Server │◄─┼────┼─►│ Parent VM / │  │ Instant Clone   │    │
│  │  (primary)         │  │    │  │ Replica     │  │ Child VMs       │    │
│  └────────────────────┘  │    │  └─────────────┘  └─────────────────┘    │
│  ┌────────────────────┐  │    │         ▲                 │              │
│  │  Connection Server │  │    │  ┌──────┴──────┐ ┌───────▼───────┐       │
│  │  (replica)         │  │    │  │   vCenter   │ │  App Volumes  │       │
│  └────────────────────┘  │    │  │  + vSAN     │ │  Manager/DEM  │       │
│  ┌────────────────────┐  │    │  └─────────────┘ └───────────────┘       │
│  │  UAG (DMZ)         │◄─┼────┼──── External clients (Blast/PCoIP)       │
│  └────────────────────┘  │    └──────────────────────────────────────────┘
└──────────────────────────┘
```

![Horizon Architecture](../../../../assets/horizon-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Architecture overview, topology, and how it fits in the stack.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and services.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, design rules, and configuration baselines.</span></a>
</div>
