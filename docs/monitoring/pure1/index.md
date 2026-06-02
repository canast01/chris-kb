# Pure1

<div class="kb-summary">
Pure Storage Pure1 cloud-based management and analytics — SaaS architecture, AI-driven health scoring, capacity forecasting, and fleet management via REST API.
</div>

```
┌───────────────────────── Pure1 — Pure Storage Cloud Management and Analytics ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Pure1: SaaS management and AI/ML analytics platform for Pure Storage FlashArray and FlashBlade│   │
│   │        Phonehome: arrays connect outbound to pure1.purestorage.com; no inbound required       │   │
│   │    AI-driven workload intelligence, capacity forecasting, and proactive support automation    │   │
│   │         Access at pure1.purestorage.com; browser-based; no on-prem software to install        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pure1 provides global visibility across all arrays; Evergreen subscription includes Pure1          │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Health & Alerts       │  │          Analytics          │  │           Support           │   │
│   │         Health score        │  │         Workload ID         │  │        Auto case open       │   │
│   │       Proactive alerts      │  │         AI forecast         │  │        Remote assist        │   │
│   │        Email/webhook        │  │        Capacity plan        │  │        Proactive swap       │   │
│   │       Severity levels       │  │        Perf analysis        │  │        Evergreen mgmt       │   │
│   │          Audit log          │  │          Benchmark          │  │        License track        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  FlashArrays/FlashBlades on-prem · TCP 443 outbound to pure1.purestorage.com · no gateway needed      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pure1 = Pure Storage SaaS platform for fleet management and AI analytics                             │
│  Phonehome = Array outbound telemetry to Pure cloud; encrypted; no inbound required                   │
│  Evergreen = Pure Storage subscription model; includes Pure1 and hardware refresh rights              │
│  Health score = Composite score per array from telemetry analysis                                     │
│  Workload ID = AI identifying application workload patterns on array (VDI, Oracle, etc.)              │
│  AI forecast = ML-based capacity exhaustion prediction per array                                      │
│  Proactive alert = Pure1 detecting pre-failure condition before customer notices                      │
│  Auto case = Pure1 automatically opening support case with diagnostic data attached                   │
│  Remote assist = Pure Storage engineer connecting to array via Pure1 for support                      │
│  Proactive swap = Pure staging replacement hardware before failure occurs                             │
│  Benchmark = Pure1 comparing array performance to anonymised fleet averages                           │
│  License track = Pure1 showing Purity version and Evergreen subscription status                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>SaaS data pipeline, phone-home architecture, Pure1 Meta analytics engine, and fleet topology.</span></a>
<a class="kb-card" href="design-standards/"><strong>Standards</strong><span>Configuration standards, naming conventions, and baselines.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Installation, upgrades, patching, and decommission.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Day-to-day operational tasks, checks, and procedures.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Pure1 REST API, OAuth2 authentication, array health, capacity, and performance queries.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for common tasks and reporting.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>Integration with other systems and platforms.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Security configuration, hardening, and access control.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Support bundles, case management, and escalation paths.</span></a>
<a class="kb-card" href="health/"><strong>Health</strong><span>Real-time array and drive health, controller status, and SupportAssist phone-home connectivity.</span></a>
<a class="kb-card" href="capacity/"><strong>Capacity</strong><span>Consumed vs effective capacity, snapshot overhead, data reduction ratio, and 90-day growth forecast.</span></a>
<a class="kb-card" href="performance/"><strong>Performance</strong><span>IOPS, throughput, and latency trends per array, volume, and initiator.</span></a>
<a class="kb-card" href="alerts/"><strong>Alerts</strong><span>Active and historical alerts, severity filtering, notification configuration, and alert suppression.</span></a>
<a class="kb-card" href="support/"><strong>Support</strong><span>Case creation, log bundle collection, remote assist enablement, and escalation paths.</span></a>
</div>
