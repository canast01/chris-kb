# Pure Operations

```
  Pure Operations Hub

  ┌──────────────────────────────────────────────────┐
  │  FlashArray / FlashBlade                         │
  │  ├─ Arrays: health, alerts, capacity             │
  │  ├─ Replication: pods, protection groups         │
  │  ├─ Snapshots: schedules, retention              │
  │  └─ Host connectivity: paths, HBAs               │
  └────────────┬─────────────┬────────────┬──────────┘
               │             │            │
               ▼             ▼            ▼
  ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
  │  Alerts        │ │  Pure1       │ │  Support Cases │
  │  ├─ purealert  │ │  ├─ Health   │ │  ├─ Collect    │
  │  │   list      │ │  ├─ Capacity │ │  │   diag info │
  │  ├─ Severity   │ │  ├─ Perf     │ │  ├─ Portal /   │
  │  │   Critical/ │ │  └─ Alerts  │ │  │   phone     │
  │  │   Warning   │ │             │ │  └─ P1─P4 SLA  │
  │  └─ Email/SNMP │ │  Phone-home │ │                │
  │     /syslog    │ │  TCP 443    │ │  CSM for       │
  └────────────────┘ └─────────────┘ │  billing/SLA   │
                                     └────────────────┘
```

Use this section for practical notes, checks, commands, troubleshooting, design references, and change validation.

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="alerts/">
  <strong>Alerts</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Alerts.</span>
</a>

<a class="kb-card" href="pure1/">
  <strong>Pure1</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Pure1.</span>
</a>

<a class="kb-card" href="support-cases/">
  <strong>Support Cases</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Support Cases.</span>
</a>

</div>
