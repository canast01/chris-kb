# Pure1

<div class="kb-summary">
Pure Storage Pure1 cloud-based management and analytics — SaaS architecture, AI-driven health scoring, capacity forecasting, and fleet management via REST API.
</div>

```text
Pure1 — Cloud Monitoring
┌────────────────┐    ┌────────────────┐
│ FlashArray     │    │ FlashBlade     │
│ (on-prem)      │    │ (on-prem)      │
└───────┬────────┘    └───────┬────────┘
        │ phone home           │ phone home
        │ HTTPS outbound       │ HTTPS outbound
        └──────────┬───────────┘
                   ▼
         ┌─────────────────┐
         │   Pure1 Cloud   │
         │  ┌───────────┐  │
         │  │ Analytics │  │
         │  │ AI / ML   │  │
         │  │ Alerts    │  │
         │  └───────────┘  │
         └────────┬────────┘
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
   Browser     Email      REST API
   (GUI)      alerts    (ticketing
              team)      integration)
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
