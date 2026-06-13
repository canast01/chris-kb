# Nutanix — Troubleshooting

<div class="kb-summary">
Nutanix troubleshooting guide — common operational problems, diagnostic tools and log locations, NCC health check interpretation, and Nutanix GSS escalation procedures.

*Applies to: AOS 6.x · AHV*
</div>

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    NUTANIX TROUBLESHOOTING FLOW                                                       │
│                                                                                                       │
│  ALERT / SYMPTOM                                                                                      │
│       │                                                                                               │
│       ▼                                                                                               │
│  ┌─────────────────────────────────────────────────────────────┐                                      │
│  │  1. RUN NCC                                                 │                                      │
│  │     ncc --health_checks run_all                             │                                      │
│  │     → PASS → monitor, check logs for root cause             │                                      │
│  │     → FAIL → identify which check, read check description   │                                      │
│  └──────────────────────────────┬──────────────────────────────┘                                      │
│                                 │                                                                     │
│       ┌─────────────────────────▼──────────────────────────┐                                          │
│       │  2. CHECK SERVICE HEALTH                           │                                          │
│       │     genesis status · nodetool status               │                                          │
│       │     → all UP → proceed to logs                     │                                          │
│       │     → service DOWN → genesis restart (on CVM)      │                                          │
│       └─────────────────────────┬──────────────────────────┘                                          │
│                                 │                                                                     │
│       ┌─────────────────────────▼──────────────────────────┐                                          │
│       │  3. READ RELEVANT LOG                              │                                          │
│       │     stargate.ERROR · curator.INFO · genesis.out    │                                          │
│       │     → find error timestamp matching incident       │                                          │
│       └─────────────────────────┬──────────────────────────┘                                          │
│                                 │                                                                     │
│       ┌─────────────────────────▼──────────────────────────┐                                          │
│       │  4. COLLECT SUPPORT BUNDLE + ESCALATE              │                                          │
│       │     Prism → Log Collector · logbay collect         │                                          │
│       │     portal.nutanix.com → open GSS case             │                                          │
│       └────────────────────────────────────────────────────┘                                          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="common-issues/">
    <strong>Common Issues</strong>
    <span>CVM down, NCC failures, storage degraded, VM stuck power states, cluster full, and replication failures.</span>
  </a>
  <a class="kb-card" href="diagnostics/">
    <strong>Diagnostics</strong>
    <span>Key log locations, NCC check details, Stargate/Cassandra/Curator diagnostics, and support bundle collection.</span>
  </a>
  <a class="kb-card" href="escalation/">
    <strong>Escalation</strong>
    <span>When to call Nutanix GSS, severity classification, case opening procedure, and what to collect beforehand.</span>
  </a>
</div>
