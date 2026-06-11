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
│  Key terms:                                                                                           │
│                                                                                                       │
│  HEALTH_ERR    = Critical cluster condition; may halt writes; investigate and resolve immediately     │
│  HEALTH_WARN   = Non-critical condition; I/O continues; address before it escalates to ERR            │
│  OSD_DOWN      = Health code: OSD not responding; check disk (smartctl), network, OSD journal         │
│  PG_DEGRADED   = Health code: PGs have fewer replicas than required; data accessible but at risk      │
│  PG_INACTIVE   = Health code: PG cannot serve I/O; most severe PG state; investigate immediately      │
│  SLOW_OPS      = Health code: ops queued more than 30s; indicates disk I/O or network saturation      │
│  OSD_NEARFULL  = OSD disk usage approaching full ratio; plan capacity expansion before OSD_FULL       │
│  ceph health detail = Enumerates all active health codes with per-item context and affected objects   │
│  sosreport     = Linux system diagnostics bundle; required for Red Hat RHCS support case submission   │
│  ceph report   = Full cluster state JSON snapshot; standard diagnostic data for support cases         │
│  RHCS          = Red Hat Ceph Storage; commercial Ceph distribution with enterprise support SLAs      │
│  crash dump    = Daemon crash archive; ceph crash ls / ceph crash info <id> for investigation         │
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
