# Aria Operations for Networks — Architecture

<div class="kb-summary">
Aria Operations for Networks (formerly vRealize Network Insight) provides network visibility, flow analysis, and micro-segmentation planning across NSX-T, physical switches, and cloud environments.
</div>

```
┌─────────────────────────────────────────────────────────────────┐
│          ARIA OPERATIONS FOR NETWORKS — ARCHITECTURE            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
   ┌───────────────────────▼───────────────────────────────┐
   │  DATA SOURCES                                         │
   │  ┌──────────┐  ┌──────────┐  ┌───────────────────┐   │
   │  │ vCenter  │  │  NSX-T   │  │  Physical Switches│   │
   │  │ + ESXi   │  │ Manager  │  │  (SNMP / NetFlow) │   │
   │  └────┬─────┘  └────┬─────┘  └─────────┬─────────┘   │
   └───────┼─────────────┼─────────────────────────────────┘
           └─────────────┴──────────┬──────────┘
                                    ▼
   ┌───────────────────────────────────────────────────────┐
   │  Collector VMs  (one per site / data source group)    │
   │  Aggregate and normalise flow + config data           │
   └───────────────────────┬───────────────────────────────┘
                           │
   ┌───────────────────────▼───────────────────────────────┐
   │  Platform VM  (central analytics node)                │
   │  Flow analysis │ Path tracing │ Security planning     │
   │  IPFIX / sFlow processing │ Search & dashboards       │
   └───────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Architecture overview, topology, and how it fits in the stack.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and services.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, design rules, and configuration baselines.</span></a>
</div>

## Aria Operations for Networks — Platform Architecture

![Aria Operations for Networks Platform Architecture](../../../../assets/aria-operations-for-networks-architecture-overview.svg)
