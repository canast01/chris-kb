# VMware Reference

<div class="kb-summary">
Quick-reference pages for VMware platform decision-making: architecture design decisions with rationale, operational gotchas — underdocumented behaviours and default limits that cause incidents, and VMware licensing — edition structure, per-core pricing, and legacy migration.
</div>

```text
┌─────────────────────────────────────── VMware — Reference ────────────────────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  Reference pages answer "which option should I choose?" and "why does it do that?"                    │
│  Design decisions capture the reasoning behind architectural choices — not just the outcome           │
│  Gotchas document underdocumented defaults, limits, and behaviours that cause incidents               │
│                                                                                                       │
│  DESIGN DECISIONS                                                                                     │
│  vSS vs vDS · vSAN vs external SAN · NSX VLAN vs Overlay transport · HA cluster sizing                │
│  Host profile vs vLCM image management · VCF vs manual deployment · Aria vs native alarms             │
│                                                                                                       │
│  GOTCHAS                                                                                              │
│  vCLS VMs consuming resources · HA slot size overestimation · vSAN resync blocking maintenance        │
│  NTP drift killing SSO · snapshot delta growth rates · vDS rollback window                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="design-decisions/">
  <strong>Design Decisions</strong>
  <span>Architecture choices with rationale — vSS vs vDS, vSAN vs SAN, NSX topology, cluster sizing.</span>
</a>

<a class="kb-card" href="gotchas/">
  <strong>Gotchas</strong>
  <span>Underdocumented behaviours, default limits, and common traps across the VMware platform.</span>
</a>

<a class="kb-card" href="licensing/">
  <strong>Licensing</strong>
  <span>Post-Broadcom edition structure — VVF vs VCF, per-core pricing, add-on SKUs, and legacy perpetual migration.</span>
</a>

</div>
