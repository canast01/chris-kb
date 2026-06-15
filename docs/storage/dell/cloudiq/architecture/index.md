---
tags:
  - architecture
  - dell
---
# CloudIQ — Architecture

<div class="kb-summary">
Cloud-native AIOps SaaS platform hosted by Dell. Receives telemetry from on-premises Dell arrays via the Secure Connect Gateway and produces health scores (0–100), capacity forecasts, and AI-driven recommendations. No on-premises compute required beyond the SCG.

*Applies to: CloudIQ*
</div>

```text
┌───────────────────────────── Dell CloudIQ — AIOps Analytics Architecture ─────────────────────────────┐
│                                                                                                       │
│  SaaS-hosted AIOps platform; collects telemetry from Dell storage via call-home;                      │
│  ML-based anomaly detection, capacity forecasting, and health scoring per system.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data Collection                │  │             Supported Platforms             │   │
│   │           Call-home: API telemetry           │  │             PowerStore, PowerMax            │   │
│   │          No agent on most platforms          │  │             PowerScale, Unity XT            │   │
│   │            15-minute granularity             │  │               Data Domain, ECS              │   │
│   │          13 months: historical data          │  │             PowerFlex, SC Series            │   │
│   │        SaaS: Dell-hosted, no on-prem         │  │               PowerProtect DD               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CloudIQ analyzes patterns across millions of array data points using ML models.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Analytics Features              │  │              Integration Points             │   │
│   │        Health score: 0-100 per system        │  │             REST API: northbound            │   │
│   │       Anomaly: deviation from baseline       │  │              SIEM: event export             │   │
│   │          Capacity forecast: 90-day           │  │            ServiceNow integration           │   │
│   │        Workload intelligence: IO type        │  │           Splunk: telemetry export          │   │
│   │        What-if: right-size scenarios         │  │          Email/Slack: alert notify          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  CloudIQ is SaaS — no on-prem server required; arrays send telemetry outbound to                      │
│  Dell cloud on TCP 443; arrays need internet access or ESRS proxy.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudIQ        = Dell AIOps SaaS platform; storage health and analytics                              │
│  Health score   = 0-100 score per array; below 80 triggers recommended action                         │
│  Anomaly        = ML-detected deviation from normal performance baseline                              │
│  Capacity forecast= 90-day prediction of when storage will fill up                                    │
│  Workload intelligence= classifies IO patterns: random, sequential, mixed                             │
│  What-if        = scenario: what happens to latency if I add X GB of workload?                        │
│  Call-home      = array-to-Dell telemetry channel; also used for ESRS/support                         │
│  SaaS           = Software as a Service; Dell hosts, no customer infra required                       │
│  Connector      = per-platform CloudIQ plugin; enabled on array config                                │
│  REST API       = CloudIQ northbound API; pull metrics into custom dashboards                         │
│  ESRS           = EMC Secure Remote Services; call-home connectivity mechanism                        │
│  Alert policy   = user-defined rule; sends email/Slack when threshold exceeded                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![CloudIQ Architecture](../../../../assets/dell-cloudiq-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with Dell arrays, Secure Connect Gateway, and REST API.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SCG redundancy, notification configuration, and API integration practices.</span></a>
</div>

## Supported Platforms

| Platform | Telemetry Source |
|---|---|
| PowerMax / VMAX | Embedded telemetry agent |
| Unity XT | CloudIQ data collection service |
| PowerScale (Isilon) | OneFS embedded agent |
| PowerStore | REST API |
| PowerFlex (VxFlex OS) | SDC telemetry |

## Data Pipeline

