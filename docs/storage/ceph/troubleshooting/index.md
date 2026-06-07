# Ceph — Troubleshooting

<!-- diagram:ceph-troubleshooting -->

<div class="kb-summary">
Ceph troubleshooting: OSD down/out recovery, PG degraded and stuck states, slow requests, nearfull cluster, and escalation to Red Hat/Ceph community support.
</div>

```text
┌──────────────────────────────────────── Ceph Troubleshooting ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Ceph Troubleshooting Overview                                 │   │
│   │         Three sub-sections: Common Issues, Diagnostics (logs/health codes), Escalation        │   │
│   │            Start: ceph health detail — every warning has a health code with context           │   │
│   │        Sev 1: any HEALTH_ERR with inactive PGs or cluster full → open case immediately        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │       Common Issues        │  │        Diagnostics         │  │           Escalation          │   │
│   │           OSD down         │  │      Health code guide     │  │        Red Hat RHCS cases     │   │
│   │      PG degraded/stuck     │  │       OSD log analysis     │  │       Required data bundle    │   │
│   │        Slow requests       │  │      Crash dump review     │  │       Community resources     │   │
│   │    Nearfull/Full cluster   │  │     Network diagnostics    │  │        Emergency commands     │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="common-issues/">
    <span class="kb-card-title">Common Issues</span>
    <span class="kb-card-desc">OSD down, PG stuck, slow requests, nearfull, clock skew, recovery stuck</span>
  </a>
  <a class="kb-card" href="diagnostics/">
    <span class="kb-card-title">Diagnostics</span>
    <span class="kb-card-desc">ceph health codes, OSD logs, crash dump analysis, network diagnostics</span>
  </a>
  <a class="kb-card" href="escalation/">
    <span class="kb-card-title">Escalation</span>
    <span class="kb-card-desc">Red Hat Ceph support cases, community resources, required diagnostic data</span>
  </a>
</div>
