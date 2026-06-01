# Aria Operations — Troubleshooting

<div class="kb-summary">
Aria Operations — Troubleshooting reference.
</div>

```
┌────────────────────────────────── Aria Operations — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Adapter collection failures: verify credentials, firewall paths, and adapter version     │   │
│   │    Alert noise and false positives: tune symptom thresholds; check adapter collection gaps    │   │
│   │  Missing metric data: confirm remote collector reachability; check collector group assignment │   │
│   │       Dashboard errors: verify data source adapter health; check widget metric mappings       │   │
│   │        support.zip bundle collects all cluster logs; attach to GSS case for escalation        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics isolate adapter or cluster root cause                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      Adapter coll fail      │  │     Cluster diagnostics     │  │         Support.zip         │   │
│   │         Alert noise         │  │         Adapter log         │  │        GSS case open        │   │
│   │         Missing data        │  │         Support.zip         │  │        Skyline health       │   │
│   │       Dashboard error       │  │        REST API debug       │  │        TAM escalation       │   │
│   │       Remote coll down      │  │       Log Insight intg      │  │          Log bundle         │   │
│   │        Capacity wrong       │  │       Metric explorer       │  │        Version compat       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues triage adapter and cluster faults · diagnostics use logs and metric explorer         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   Adapter fail   │   Adapter log    │   /var/log/vrops  │   support.zip    │ Re-auth adapter  │   │
│   │   Alert noise    │ Metric explorer  │    Cluster diag   │   GSS P1 case    │    Tune alert    │   │
│   │   Missing data   │  REST API debug  │   /var/log/casa   │   TAM escalate   │    Re-collect    │   │
│   │  Collector down  │   Support.zip    │   /var/log/coll   │  Skyline health  │   Restart coll   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (cluster nodes + collectors) · RAM DIMMs · Network NICs · vCenter/cloud connectivity         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter collection = Periodic metric pull by an adapter instance; fails on auth or network errors    │
│  Remote collector   = Site-local VM forwarding metrics; offline if unreachable or out of resources    │
│  Alert noise        = Excessive or false-positive alerts caused by overly sensitive symptom thresholds│
│  Metric gap         = Missing data points in a metric time series; caused by collection or node       │
│  Support.zip bundle = Full diagnostic archive from Aria Ops cluster; submitted to GSS for analysis    │
│  Cluster diagnostics = Built-in health tool validating node connectivity, services, and disk usage    │
│  Metric explorer    = UI tool for querying raw metric time series to identify gaps or anomalies       │
│  Capacity calculation = Engine consuming metric history to project resource exhaustion dates          │
│  Skyline Health     = VMware proactive support tool that validates cluster health against best        │
│  REST API           = Aria Ops API for querying metrics, alerts, recommendations programmatically     │
│  Log Insight intg   = Aria Logs integration forwarding Aria Ops cluster logs for structured search    │
│  False positive alert = Alert firing when no real problem exists; tuned via symptom threshold change  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
