# Monitoring
```
┌─────────────────────────────────── Monitoring — Platform Overview ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Monitoring Platform — Observability for Virtualisation, Storage, Network, and Compute     │   │
│   │     Products: Aria Operations · CloudIQ · Dell AIOps · InsightIQ · Nexus Dashboard · Pure1    │   │
│   │  Capabilities: metrics collection · alert routing · capacity forecasting · anomaly detection  │   │
│   │    Shared services: syslog · log retention · metrics baseline · event correlation · health    │   │
│   │    Targets: vSphere · NSX · PowerStore · PowerScale · ACI fabric · FlashArray · FlashBlade    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Each monitoring tool serves a distinct domain — together they form a unified observability layer   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        VMware Domain        │  │         Dell Domain         │  │       Network/Storage       │   │
│   │       Aria Operations       │  │        CloudIQ (SaaS)       │  │       Nexus Dashboard       │   │
│   │     vCenter/NSX targets     │  │      Dell AIOps (SaaS)      │  │         Pure1 (SaaS)        │   │
│   │     Capacity forecasting    │  │     PowerStore/PowerMax     │  │       FlashArray/Blade      │   │
│   │      Anomaly detection      │  │      InsightIQ (VM app)     │  │      ACI fabric health      │   │
│   │       Compliance packs      │  │       PowerScale perf       │  │        Flow analytics       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  On-prem: Aria Ops cluster on vSphere · InsightIQ VM on PowerScale · Nexus Dashboard cluster          │
│  SaaS: CloudIQ · Dell AIOps · Pure1 — phone-home telemetry, no local server required                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Aria Operations  = On-prem analytics for vSphere, NSX, storage; collector + analytics nodes          │
│  CloudIQ          = Dell SaaS platform; health scores and capacity forecasts for Dell arrays          │
│  Dell AIOps       = AI-driven insight layer; anomaly correlation and root-cause suggestions           │
│  InsightIQ        = VM appliance for PowerScale/Isilon performance analytics                          │
│  Nexus Dashboard  = Cisco fabric visibility; NDI app for ACI/NX-OS health and assurance               │
│  Pure1            = Pure Storage SaaS; health, capacity, and performance for FlashArray/Blade         │
│  Syslog           = RFC-5424 event stream; aggregated to a central syslog server (e.g. rsyslog)       │
│  Metrics baseline = Documented normal operating ranges; used to tune alert thresholds                 │
│  Event correlation= Linking related alerts to a single root cause to reduce alert noise               │
│  Alert management = Policy-driven routing of alerts to teams, tickets, and paging systems             │
│  Log retention    = Policy governing how long logs are stored on-prem or in cloud storage             │
│  Health score     = Composite 0-100 score aggregating component health indicators                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="pure1/"><strong>Pure1</strong><span>Pure Storage cloud-based monitoring and AI analytics for FlashArray and FlashBlade fleets.</span></a>
<a class="kb-card" href="cloudiq/"><strong>CloudIQ</strong><span>Dell AIOps platform — health scores, capacity forecasting, and anomaly detection across Dell infrastructure.</span></a>
<a class="kb-card" href="aria-operations/"><strong>Aria Operations</strong><span>VMware Aria Operations (vROps) for vSphere performance, capacity, and compliance monitoring.</span></a>
<a class="kb-card" href="insightiq/"><strong>InsightIQ</strong><span>NetApp performance analytics for PowerScale — latency, throughput, workload analysis, and capacity reporting.</span></a>
<a class="kb-card" href="nexus-dashboard/"><strong>Nexus Dashboard</strong><span>Cisco fabric monitoring — health, flow telemetry, policy compliance across ACI and NX-OS.</span></a>
<a class="kb-card" href="dell-aiops/"><strong>Dell AIOps</strong><span>AI-driven anomaly detection and predictive recommendations across the Dell infrastructure estate.</span></a>
</div>

## Operations

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="alert-management/"><strong>Alert Management</strong><span>Alert rule lifecycle: creation, threshold tuning, routing to teams, and suppression during maintenance.</span></a>
<a class="kb-card" href="dashboard-standards/"><strong>Dashboard Standards</strong><span>Dashboard design guidelines, required metrics, refresh intervals, and team ownership standards.</span></a>
<a class="kb-card" href="event-correlation/"><strong>Event Correlation</strong><span>Grouping and deduplication of related alerts into incidents to reduce noise and speed triage.</span></a>
<a class="kb-card" href="health-monitoring/"><strong>Health Monitoring</strong><span>Continuous health checks, availability tracking, and SLA compliance monitoring.</span></a>
<a class="kb-card" href="metrics-baseline/"><strong>Metrics Baseline</strong><span>Baseline performance metrics for normal operating ranges, used to detect drift and anomalies.</span></a>
<a class="kb-card" href="log-retention/"><strong>Log Retention</strong><span>Log retention policies, storage tiering, archival schedules, and compliance retention periods.</span></a>
<a class="kb-card" href="syslog/"><strong>Syslog</strong><span>Syslog server configuration, facility/severity filtering, log forwarding, and retention management.</span></a>
</div>
