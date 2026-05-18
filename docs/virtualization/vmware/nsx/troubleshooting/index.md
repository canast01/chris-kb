# NSX — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware NSX. Covers common overlay, gateway, and DFW failure patterns, diagnostic commands, log collection, and escalation procedures.
</div>

```
┌─────────────────────────────────────────────────────────────┐
│            NSX Troubleshooting Decision Tree                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Problem reported                                           │
│       │                                                     │
│       ├──► Connectivity loss ──► Common Issues page        │
│       │    (VM, gateway, BGP)                               │
│       │                                                     │
│       ├──► Need diagnostic data ──► Diagnostics page       │
│       │    (logs, traceflow, capture,                       │
│       │     support bundle)                                 │
│       │                                                     │
│       └──► Cannot resolve internally                        │
│            │                                               │
│            ▼                                               │
│       ┌──────────────────────────────────────────────────┐ │
│       │  Escalation page                                 │ │
│       │  • When to escalate criteria                     │ │
│       │  • Data to collect                               │ │
│       │  • Broadcom TAC + SLA tiers                      │ │
│       └──────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
