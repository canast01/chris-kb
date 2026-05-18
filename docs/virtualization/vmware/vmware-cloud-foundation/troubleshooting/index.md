# VCF — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware Cloud Foundation. Covers common SDDC Manager and LCM failure patterns, workload domain issues, diagnostic commands, log collection, and escalation procedures.
</div>

```
VCF Troubleshooting — Triage Decision Map
┌─────────────────────────────────────────────────────┐
│  Issue Reported                                     │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────────────┐
        ▼              ▼                      ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ SDDC Manager │ │ LCM / Bundle │ │ Network / Overlay│
│ UI or API    │ │ failure      │ │ NSX / TEP issue  │
│              │ │              │ │                  │
│ → check      │ │ → lcm-debug  │ │ → NSX transport  │
│   services   │ │   .log       │ │   node status    │
│ → ops-mgr    │ │ → depot      │ │ → TEP ping test  │
│   .log       │ │   connect?   │ │ → BGP status     │
└──────────────┘ └──────────────┘ └──────────────────┘
        │              │                      │
        └──────────────┴──────────────────────┘
                       │ none resolved?
                       ▼
┌─────────────────────────────────────────────────────┐
│  SoS full health check + support bundle             │
│  sudo python3 /opt/vmware/sddc-support/sos          │
│    --health-summary                                 │
│  sudo vcf-support-bundle --type sddc                │
│  → Escalate to Broadcom Support (SR)                │
└─────────────────────────────────────────────────────┘
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
