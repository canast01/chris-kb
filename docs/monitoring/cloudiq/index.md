# CloudIQ (Monitoring)

<div class="kb-summary">
Dell CloudIQ cloud-based monitoring platform — architecture, health scoring, capacity forecasting, recommendations, and operational runbooks.
</div>

```
┌───────────────────────── CloudIQ — Dell Cloud-Based AI/ML Storage Monitoring ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CloudIQ: SaaS monitoring platform for Dell infrastructure — PowerStore, PowerScale, PowerFlex │   │
│   │    AI/ML engine analyses telemetry to predict failures, score health, and recommend actions   │   │
│   │      Data collected by secure gateway (or direct) and pushed to Dell cloud over HTTPS/443     │   │
│   │       No on-premises agent required for most Dell storage — native telemetry forwarding       │   │
│   │    Access via cloudiq.dell.com — browser-based; no software to install at the customer site   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health score, anomaly detection, and capacity forecasting cover entire Dell storage estate         │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Health & Alerts       │  │           Capacity          │  │         Performance         │   │
│   │      Health score 0-100     │  │     Forecast 30-90 days     │  │     Latency/IOPS trends     │   │
│   │      AI anomaly detect      │  │       Thin provision %      │  │      Bandwidth metrics      │   │
│   │       Email / webhook       │  │        Tier breakdown       │  │       Per-volume stats      │   │
│   │       Severity levels       │  │       Growth rate calc      │  │         Heatmap view        │   │
│   │      Acknowledge/snooze     │  │       Reclamation tips      │  │       Baseline compare      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  On-prem: Dell storage arrays · Gateway VM (if used) · Outbound TCP 443 to cloudiq.dell.com           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudIQ = Dell SaaS monitoring platform with AI/ML engine; browser-based at cloudiq.dell.com         │
│  Health score = 0-100 composite score for an array; red <70, yellow 70-89, green ≥90                  │
│  Anomaly = Statistically unusual metric behaviour detected by ML model                                │
│  Secure gateway = Optional on-prem VM proxying telemetry to Dell cloud for air-gapped environments    │
│  Telemetry = Metrics, events, and configuration data forwarded from Dell arrays to CloudIQ            │
│  Forecast = ML-based capacity prediction showing projected full date at current growth rate           │
│  Thin provisioning % = Ratio of allocated capacity to physical capacity; over-commit risk indicator   │
│  Reclamation = Identifying and freeing unused or wasted allocated capacity on volumes                 │
│  Recommendation = AI-generated action to improve health score or avoid predicted issue                │
│  IOPS = Input/Output Operations Per Second; primary storage performance metric                        │
│  Latency = Average time from request to completion; target <1ms for all-flash arrays                  │
│  Bandwidth = Data throughput in MB/s; complements IOPS for large-block workload sizing                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────── CloudIQ — Dell Cloud-Based AI/ML Storage Monitoring ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CloudIQ: SaaS monitoring platform for Dell infrastructure — PowerStore, PowerScale, PowerFlex │   │
│   │    AI/ML engine analyses telemetry to predict failures, score health, and recommend actions   │   │
│   │      Data collected by secure gateway (or direct) and pushed to Dell cloud over HTTPS/443     │   │
│   │       No on-premises agent required for most Dell storage — native telemetry forwarding       │   │
│   │    Access via cloudiq.dell.com — browser-based; no software to install at the customer site   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health score, anomaly detection, and capacity forecasting cover entire Dell storage estate         │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Health & Alerts       │  │           Capacity          │  │         Performance         │   │
│   │      Health score 0-100     │  │     Forecast 30-90 days     │  │     Latency/IOPS trends     │   │
│   │      AI anomaly detect      │  │       Thin provision %      │  │      Bandwidth metrics      │   │
│   │       Email / webhook       │  │        Tier breakdown       │  │       Per-volume stats      │   │
│   │       Severity levels       │  │       Growth rate calc      │  │         Heatmap view        │   │
│   │      Acknowledge/snooze     │  │       Reclamation tips      │  │       Baseline compare      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  On-prem: Dell storage arrays · Gateway VM (if used) · Outbound TCP 443 to cloudiq.dell.com           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudIQ = Dell SaaS monitoring platform with AI/ML engine; browser-based at cloudiq.dell.com         │
│  Health score = 0-100 composite score for an array; red <70, yellow 70-89, green ≥90                  │
│  Anomaly = Statistically unusual metric behaviour detected by ML model                                │
│  Secure gateway = Optional on-prem VM proxying telemetry to Dell cloud for air-gapped environments    │
│  Telemetry = Metrics, events, and configuration data forwarded from Dell arrays to CloudIQ            │
│  Forecast = ML-based capacity prediction showing projected full date at current growth rate           │
│  Thin provisioning % = Ratio of allocated capacity to physical capacity; over-commit risk indicator   │
│  Reclamation = Identifying and freeing unused or wasted allocated capacity on volumes                 │
│  Recommendation = AI-generated action to improve health score or avoid predicted issue                │
│  IOPS = Input/Output Operations Per Second; primary storage performance metric                        │
│  Latency = Average time from request to completion; target <1ms for all-flash arrays                  │
│  Bandwidth = Data throughput in MB/s; complements IOPS for large-block workload sizing                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>SaaS data pipeline, SCG gateway integration, phone-home telemetry collection, and supported array types.</span></a>
<a class="kb-card" href="design-standards/"><strong>Standards</strong><span>Configuration standards, naming conventions, and baselines.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Installation, upgrades, patching, and decommission.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Day-to-day operational tasks, checks, and procedures.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>REST API authentication, endpoints, health queries, recommendations, and capacity reporting.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for common tasks and reporting.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>Integration with other systems and platforms.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Security configuration, hardening, and access control.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Support bundles, case management, and escalation paths.</span></a>
<a class="kb-card" href="health/"><strong>Health</strong><span>Array health scores, controller and drive status, and anomaly-based degradation detection.</span></a>
<a class="kb-card" href="recommendations/"><strong>Recommendations</strong><span>Automated optimisation recommendations, priority ranking, and workload rebalancing guidance.</span></a>
<a class="kb-card" href="capacity/"><strong>Capacity</strong><span>Consumed vs effective capacity, data reduction ratios, and 90-day growth forecast.</span></a>
<a class="kb-card" href="alerts/"><strong>Alerts</strong><span>Active and historical alerts, severity filtering, and notification configuration.</span></a>
<a class="kb-card" href="reporting/"><strong>Reporting</strong><span>Infrastructure health reports, trend exports, and scheduled delivery to stakeholders.</span></a>
</div>
