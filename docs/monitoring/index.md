# Monitoring

```text
Monitoring Ecosystem
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Pure1     │  │ Aria Ops    │  │   CloudIQ   │
│ (FlashArray │  │ (vSphere /  │  │  (Dell arr. │
│  FlashBlade)│  │  NSX / Pure)│  │  PowerStore)│
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐
│  InsightIQ  │  │   Nexus     │  │ Dell AIOps  │
│ (PowerScale │  │  Dashboard  │  │  (ML anomaly│
│  analytics) │  │  (Cisco     │  │  detection) │
│             │  │   fabric)   │  │             │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
              ┌─────────────────┐
              │   Ops Team      │
              │  ┌───────────┐  │
              │  │ Dashboards│  │
              │  │  Alerts   │  │
              │  │  Reports  │  │
              │  └───────────┘  │
              └─────────────────┘
```

## Platforms

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
