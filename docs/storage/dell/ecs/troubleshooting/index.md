---
tags:
  - dell
  - troubleshooting
---
# Dell ECS — Troubleshooting

<div class="kb-summary">
Dell ECS — Troubleshooting navigation for Common Issues, Diagnostics, Escalation.
</div>

```text
┌───────────────────────────────────── Dell ECS — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  ECS troubleshooting: S3 API errors, replication failures, node outages, and capacity issues  │   │
│   │      S3 errors: 403 (auth/ACL), 404 (missing bucket/key), 503 (node overload or rebuild)      │   │
│   │      Replication: lag alerts, site unreachable, bandwidth saturation, or policy mismatch      │   │
│   │    Node issues: node offline, drive failure, rebuild stuck, disk health warnings in Portal    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify error → check ECS Portal Alerts → collect support bundle → open Dell TAC SR               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        S3 API Issues        │  │         Replication         │  │         Node / Disk         │   │
│   │        403 forbidden        │  │          Lag alert          │  │         Node offline        │   │
│   │        404 not found        │  │       Site unreachable      │  │        Drive failure        │   │
│   │         503 overload        │  │        BW saturation        │  │        Rebuild stuck        │   │
│   │         Auth failure        │  │       Policy mismatch       │  │        Disk warnings        │   │
│   │        Perf degraded        │  │          RPO breach         │  │        Capacity full        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Check ECS Portal: Alerts, Nodes status, Disk health, and Geo Replication tabs first                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │      S3 403      │    ACL/policy    │   Bucket policy   │  Fix IAM policy  │   All requests   │   │
│   │     Repl lag     │    BW / site     │   Repl dashboard  │  Raise throttle  │   RPO breached   │   │
│   │   Node offline   │     HW fault     │    Node health    │   Replace node   │   Immediately    │   │
│   │    503 errors    │   Rebuild load   │    Node status    │ Throttle rebuild │    Persistent    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS support bundle collected via Portal > Support; contains logs, config, disk status    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    S3 403         = Forbidden; check bucket policy, IAM user, and ACL; most common auth issue         │
│    S3 404         = Bucket or object not found; verify bucket name, key path, and namespace           │
│    S3 503         = Service unavailable; often during drive rebuild or node failure; retry logic      │
│    Repl lag       = Time between object write and geo sync; monitor in ECS Portal > Replication       │
│    RPO breach     = Replication lag exceeds Recovery Point Objective; DR team must be notified        │
│    BW saturation  = Replication link full; add throttle or schedule during off-peak hours             │
│    Policy mismatch = Source and target replication policy differ; causes objects to be skipped        │
│    Node offline   = ECS detects node unreachable; EC rebuild starts on remaining nodes                │
│    Rebuild stuck  = EC rebuild paused due to I/O overload; throttle client traffic to recover         │
│    Disk warnings  = S.M.A.R.T. pre-failure indicators; replace proactively before drive fails         │
│    Support bundle = ECS diagnostic package; download from Portal > Support > Generate bundle          │
│    Throttle rebuild = Limit EC rebuild I/O rate via Portal to reduce impact on client workloads       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
