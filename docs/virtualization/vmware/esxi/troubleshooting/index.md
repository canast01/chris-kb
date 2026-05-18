# ESXi — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware ESXi. Covers common host failure patterns, diagnostic commands, log collection, and escalation procedures for engaging VMware support.
</div>

```
ESXi Triage Decision Tree
┌──────────────────────────────────────────────────────┐
│  SYMPTOM REPORTED                                    │
└──────────────────────┬───────────────────────────────┘
                       │
         ┌─────────────▼─────────────────┐
         │  Host state in vCenter?        │
         └─────┬───────────┬─────────────┘
               │Connected  │Disconnected / Not Responding
               │           └─► restart hostd/vpxa
               │               or check mgmt network
               │               or IPMI console access
    ┌──────────▼──────────────────────┐
    │  Any storage dead paths?        │
    │  esxcli storage core path list  │
    └──────────┬──────────────────────┘
               │0 dead    │Dead paths → rescan / fabric check
    ┌──────────▼──────────────────────┐
    │  vmkernel.log errors?           │
    │  tail -100 /var/log/vmkernel.log│
    └──────────┬──────────────────────┘
               │None      │SCSI errors → storage
               │           NMP errors → path / HBA
               │           link down  → network
    ┌──────────▼──────────────────────┐
    │  VM performance issue?          │
    │  esxtop: %RDY, MCTLSZ, DAVG    │
    └──────────┬──────────────────────┘
               │          │High %RDY → CPU overcommit
               │           High MCTLSZ → memory balloon
               │           High DAVG → storage latency
    ┌──────────▼──────────────────────┐
    │  Escalate: collect support      │
    │  bundle → vm-support -w /tmp/   │
    └─────────────────────────────────┘
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
