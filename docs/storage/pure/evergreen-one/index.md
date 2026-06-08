# Pure Storage Evergreen//One

<div class="kb-summary">
Evergreen//One Storage-as-a-Service — Pure-owned and managed hardware on-premises or in colocation, with consumption-based billing, 99.9999% availability SLA, and performance guarantees. Covers architecture, operations, security, and troubleshooting.
</div>

```text
┌───────────────────────────────────────── Pure Evergreen//One ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Evergreen//One — Storage-as-a-Service (Pure-Owned, Customer-Operated)             │   │
│   │ Pure-owned and managed hardware installed on-premises or in colocation — customer pays per TiB│   │
│   │  SLA: 99.9999% availability · performance guarantees · consumption-based billing per TiB used │   │
│   │    Pure manages: hardware refresh, Purity upgrades, capacity additions — all non-disruptive   │   │
│   │      Customer operates: volume provisioning, host zoning, snapshots, replication policies     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Evergreen//One combines STaaS economics with on-premises control and guaranteed SLAs               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │        Vendor Support       │   │
│   │ Pure-owned hardware on-prem │  │  Pure1: health + telemetry  │  │ Vendor: hw refresh + Purity │   │
│   │   Consumption billing: TiB  │  │  Volume + host mapping ops  │  │   SLA: 99.9999% + perf SLO  │   │
│   │  99.9999% availability SLA  │  │   Snapshots + replication   │  │  Support portal: case open  │   │
│   │    Min committed capacity   │  │  Capacity: usage reporting  │  │  On-site engineer if needed │   │
│   │  Integration: colo/on-prem  │  │   Alerts: Pure1 proactive   │  │ Data to collect: log bundle │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines STaaS model · Operations run daily tasks · Vendor Support covers incidents    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │  Volume offline  │  purearray list  │   SLA: green OK?  │ Case: SLA breach │  purearray get   │   │
│   │ Billing dispute  │ Pure1 telemetry  │ Capacity headroom │  TAM escalation  │ purevolume list  │   │
│   │  Perf below SLO  │ purelog download │   Perf SLO: met?  │  Remote assist   │  pureport list   │   │
│   │Connectivity loss │ netconfig verify │   Repl state: OK  │  P1/P2 severity  │ purehgroup list  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Pure-owned FlashArray/FlashBlade · customer data centre or colo rack · Power, Cooling, and Network   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Evergreen//One  = Pure Storage-as-a-Service; Pure owns hardware, customer gets consumption pricing   │
│  STaaS           = Storage as a Service; pay-per-TiB model with no CapEx hardware purchase            │
│  99.9999% SLA    = Six nines availability guarantee; ~31 seconds downtime per year maximum            │
│  Perf SLO        = Performance Service Level Objective; latency and IOPS thresholds guaranteed        │
│  Consumption billing = Billed on actual TiB consumed above committed base; metered monthly            │
│  Committed capacity= Minimum TiB reserved in contract; pay for this floor regardless of actual use    │
│  Pure1           = Cloud portal; Pure team monitors SLA health and proactively resolves issues        │
│  Vendor refresh  = Pure ships replacement controllers or blades when hardware reaches EOL             │
│  Colo deployment = Pure-owned array installed in a customer-selected colocation facility              │
│  Log bundle      = Diagnostic data package pulled from array for Pure support case analysis           │
│  TAM             = Technical Account Manager; Pure escalation point for strategic and critical issues │
│  Remote assist   = Pure engineer connects via secure tunnel for live troubleshooting on the array     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic commands, log locations, and error codes.</span>
</a>

<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Purity CLI and Pure1 API commands relevant to Evergreen//One management.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for health checks and consumption reporting.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Evergreen//One operational standards, SLA tracking, and compliance requirements.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>Evergreen//One integration with Pure1, monitoring, and billing systems.</span></a>

</div>
