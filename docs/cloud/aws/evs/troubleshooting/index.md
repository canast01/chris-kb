---
tags:
  - aws
  - troubleshooting
search:
  boost: 1.5
---
# Amazon EVS — Troubleshooting

<!-- diagram:evs-troubleshooting -->

<div class="kb-summary">
EVS troubleshooting: host failures, vSAN degraded health, HCX connectivity issues, NSX-T networking failures, and AWS support escalation process.

*Applies to: Amazon EVS*
</div>

```text
┌───────────────────────────────────── Amazon EVS Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  EVS Troubleshooting Overview                                 │   │
│   │           Three sub-sections: Common Issues, Diagnostics (bundles/logs), Escalation           │   │
│   │         Host FAILED state: contact AWS support before deleting (preserves diagnostics)        │   │
│   │             Joint issues (HCX, NSX-T/VPC): open both AWS and VMware support cases             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │       Common Issues        │  │        Diagnostics         │  │           Escalation          │   │
│   │      Host FAILED state     │  │    CloudTrail EVS events   │  │       AWS severity levels     │   │
│   │     vSAN degraded health   │  │     VPC Flow Logs query    │  │        Required case data     │   │
│   │    HCX service mesh down   │  │     NSX-T support bundle   │  │        AWS + VMware joint     │   │
│   │    NSX-T routing failure   │  │     Log locations table    │  │       TAM escalation path     │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="common-issues/">
    <span class="kb-card-title">Common Issues</span>
    <span class="kb-card-desc">Host failures, vSAN degraded, HCX down, NSX-T networking, API errors</span>
  </a>
  <a class="kb-card" href="diagnostics/">
    <span class="kb-card-title">Diagnostics</span>
    <span class="kb-card-desc">AWS support bundles, vSAN HCL check, NSX-T support bundle, log collection</span>
  </a>
  <a class="kb-card" href="escalation/">
    <span class="kb-card-title">Escalation</span>
    <span class="kb-card-desc">AWS support case process, TAM escalation, required data for EVS cases</span>
  </a>
</div>

