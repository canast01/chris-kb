# Ceph — Troubleshooting

<!-- diagram:ceph-troubleshooting -->

<div class="kb-summary">
Ceph troubleshooting: OSD down/out recovery, PG degraded and stuck states, slow requests, nearfull cluster, and escalation to Red Hat/Ceph community support.
</div>

```mermaid
graph TD
    classDef check fill:#2563eb,color:#fff
    classDef warn fill:#b45309,color:#fff
    classDef err fill:#991b1b,color:#fff
    classDef ok fill:#15803d,color:#fff

    A([ceph -s]):::check --> B{Health status}:::check
    B -- HEALTH_OK --> C([Done — no action needed]):::ok
    B -- HEALTH_WARN --> D[Check specific warning\nceph health detail]:::warn
    D --> E([Clock skew? OSD nearfull?\nSlow ops? → common-issues/]):::warn
    B -- HEALTH_ERR --> F{Error type}:::err
    F -- OSD down --> G([OSD recovery\ncommon-issues/]):::err
    F -- PG inactive --> H([PG diagnostics\ndiagnostics/]):::err
    F -- MON quorum lost --> I([MON recovery\ncommon-issues/]):::err
    F -- Need support --> J([Escalation\nescalation/]):::err
```

| Symptom | Start here |
|---|---|
| OSD_DOWN, OSDs not starting | [Common Issues](common-issues/) |
| PG degraded, undersized, inactive | [Common Issues](common-issues/) |
| HEALTH_ERR OSD_FULL, writes blocked | [Common Issues](common-issues/) |
| Slow ops, client latency > 100 ms | [Common Issues](common-issues/) |
| Clock skew HEALTH_WARN | [Common Issues](common-issues/) |
| MON quorum lost | [Common Issues](common-issues/) |
| Need crash info, log collection, PG deep dive | [Diagnostics](diagnostics/) |
| Opening Red Hat support case | [Escalation](escalation/) |

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
