---
tags:
  - architecture
  - dell
---
# Dell AIOps — Architecture

<div class="kb-summary">
Dell AIOps is a fully SaaS-delivered AI operations platform. Telemetry flows from arrays through the on-premises Secure Connect Gateway to Dell's cloud AI pipeline, which produces anomaly detection, root cause analysis, and prioritised recommendations.

*Applies to: Dell AIOps*
</div>

```text
┌────────────────────────────── Dell AIOps — AI-Driven Storage Operations ──────────────────────────────┐
│                                                                                                       │
│  AIOps umbrella: CloudIQ as the analytics engine; ML trained on millions of metrics;                  │
│  anomaly detection, capacity forecasting, and workload intelligence reduce manual effort.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                AIOps Platform                │  │               AI Capabilities               │   │
│   │         CloudIQ: core analytics SaaS         │  │         Anomaly: vs trained baseline        │   │
│   │           ML model: fleet-trained            │  │          Capacity forecast: 90 days         │   │
│   │        Health score: 0-100 per array         │  │          Workload class: IO pattern         │   │
│   │        Real-time: 15-min granularity         │  │           Right-size: advisor recs          │   │
│   │            Historical: 13 months             │  │         Proactive: auto SR creation         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ML models trained across the entire Dell storage fleet; individual anomalies detected                │
│  by comparing against what is normal for that array type and workload pattern.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Data Sources                 │  │                   Outcomes                  │   │
│   │        Array telemetry via call-home         │  │           Fewer reactive incidents          │   │
│   │          No agent on most platforms          │  │           Optimized capacity spend          │   │
│   │          API connectors per product          │  │         Proactive SR before failure         │   │
│   │         APEX: STaaS consumption data         │  │            Cross-tier visibility            │   │
│   │          Compute + network context           │  │            API: Splunk/ServiceNow           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Entirely SaaS — no on-prem server; arrays connect outbound to Dell cloud on TCP 443;                 │
│  ESRS or ESRS gateway required for call-home; APEX Observer optional on-prem VM.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AIOps          = AI for IT Operations; ML applied to infrastructure management                       │
│  CloudIQ        = Dell AIOps SaaS; storage health, anomaly, capacity analytics                        │
│  ML model       = trained on fleet-wide telemetry; detects per-array anomalies                        │
│  Anomaly        = metric significantly deviating from its historical normal range                     │
│  Capacity intelligence= predicts when arrays will reach threshold, not just current %                 │
│  Workload class = IO pattern label (random read, sequential write, mixed) per LUN                     │
│  Proactive SR   = CloudIQ can auto-open Dell support case before admin notices                        │
│  Health score   = composite score per array; accounts for performance + capacity                      │
│  Cross-tier     = visibility linking compute CPU pressure to storage latency cause                    │
│  Call-home      = telemetry path from array to Dell cloud; same as ESRS channel                       │
│  Right-size     = recommendation to rebalance workloads across arrays                                 │
│  APEX Observer  = on-prem agent that enriches telemetry with local context                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Dell AIOps Architecture](../../../../assets/dell-aiops-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>SaaS architecture, AI capabilities, telemetry sources, data flow, and component roles.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>CloudIQ integration, notification channels, and supported Dell platforms.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Deployment standards, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Role |
|---|---|
| CloudIQ / APEX Console | SaaS portal — recommendations, anomaly dashboard, health scores |
| Secure Connect Gateway (SCG) | On-premises telemetry collection and forwarding (customer-managed) |
| Dell AI Pipeline | Anomaly detection, RCA, and capacity forecasting (Dell-managed cloud) |

---

## Architecture

