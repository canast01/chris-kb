# CloudIQ

<div class="kb-summary">
Dell CloudIQ cloud-based monitoring platform — architecture, health scoring, capacity forecasting, recommendations, and operational runbooks.
</div>

```
CloudIQ Data Flow
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PowerStore   │  │  PowerMax    │  │  PowerScale  │
│  (on-prem)   │  │  (on-prem)   │  │  (on-prem)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │ telemetry (SRS/ESRS)               │
       └──────────────┬────────────────────┘
                      ▼ HTTPS outbound
         ┌────────────────────────┐
         │  Secure Connect Gateway│  (on-prem relay)
         └────────────┬───────────┘
                      ▼
         ┌────────────────────────┐
         │     CloudIQ Cloud      │
         │  ┌──────────────────┐  │
         │  │  Health Score    │  │
         │  │  ML Analytics    │  │
         │  │  Capacity Fcst   │  │
         │  └──────────────────┘  │
         └────────────┬───────────┘
                      │
           ┌──────────┼──────────┐
           ▼          ▼          ▼
        Alerts   Recommend-   Health
       (email/   ations       Score
        portal)  (portal)     Dashboard
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
