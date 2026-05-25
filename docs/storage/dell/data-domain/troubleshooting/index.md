# Data Domain — Troubleshooting

```text
┌───────────────────────────────── Dell Data Domain — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Data Domain troubleshooting: backup failures, replication issues, capacity problems      │   │
│   │     Backup failures: DD Boost errors, authentication, network, or capacity full conditions    │   │
│   │      Replication: lag growing, context errors, bandwidth saturation, or firewall blocking     │   │
│   │        Capacity: low space alerts, garbage collect not reclaiming, dedup ratio degraded       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify failure source → check DD alerts and event log → collect support bundle → open SR         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Backup Issues        │  │         Replication         │  │           Capacity          │   │
│   │       DD Boost errors       │  │         Lag growing         │  │       Low space alert       │   │
│   │         Auth failure        │  │        Context error        │  │        GC not helping       │   │
│   │       Network timeout       │  │         BW saturated        │  │        Ratio degraded       │   │
│   │        Capacity full        │  │        Firewall block       │  │       Cloud tier stall      │   │
│   │       License expired       │  │       Schedule missed       │  │         Disk failure        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    First check: DD GUI Alerts panel and event log; then sysstat and support bundle for TAC            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │   Backup fail    │   Auth/network   │    DD Boost log   │   Reset creds    │    Recurring     │   │
│   │     Repl lag     │  BW or firewall  │    Repl context   │  Raise throttle  │    > 24h lag     │   │
│   │    Low space     │    GC needed     │    Space report   │      Run GC      │ After 2 GC runs  │   │
│   │   Disk failure   │     Hardware     │    Disk health    │   Replace disk   │   Immediately    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: DD GUI > Maintenance > Disks for disk health; replace failed disks before rebuild needed │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DD Boost log   = Backup application log combined with DD event log; cross-reference timestamps     │
│    Auth failure   = DD Boost username or password mismatch between backup app and DD user config      │
│    Context error  = Replication context broken; usually firewall port 2051 blocked or IP changed      │
│    Replication lag = Source write rate exceeds replication bandwidth; increase throttle or bandwidth  │
│    BW saturation  = Replication link at 100%; throttle to reduce backup app impact during peak hours  │
│    Garbage collect = Run via CLI: filesys clean start; takes hours; do not abort once started         │
│    GC not helping = GC ran but space not recovered; data may still have valid references; check policy│
│    Ratio degraded = Dedup ratio dropped; check if new data type introduced (compressed, encrypted)    │
│    Cloud tier stall = Cloud tier transfer paused; check internet/proxy connectivity and credentials   │
│    Support bundle = Collect via GUI: Diagnostics > Support Bundle; attach to Dell TAC SR              │
│    sysstat        = DD CLI command; shows filesystem status, service health, and hardware summary     │
│    License expired = DD capacity or feature license expired; check via GUI: Administration > Licenses │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
