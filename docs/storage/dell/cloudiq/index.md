---
tags:
  - dell
---
# CloudIQ

<div class="kb-summary">
Dell CloudIQ — cloud-native AIOps SaaS for Dell storage. ML-driven health scoring, capacity forecasting, and proactive recommendations across PowerMax, Unity, PowerScale, PowerStore, and PowerFlex.

*Applies to: CloudIQ*
</div>

```text
┌──────────────────────────────────────────── Dell CloudIQ ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  CloudIQ: Dell SaaS platform delivering AIOps-based storage health and performance analytics  │   │
│   │     Collects telemetry via Secure Connect Gateway (SCG); health scores, alerts, forecasts     │   │
│   │    Supports PowerStore, PowerMax, Unity XT, PowerScale, Data Domain, and legacy VMAX arrays   │   │
│   │       Proactive recommendations, capacity forecasting, and firmware advisory automation       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Array telemetry → SCG relay → CloudIQ SaaS → health scores, alerts, recommendations                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Analytics Engine      │  │        Array Support        │  │        Cloud Services       │   │
│   │        Health scoring       │  │          PowerStore         │  │        SaaS delivery        │   │
│   │      Anomaly detection      │  │       PowerMax / VMAX       │  │          SCG relay          │   │
│   │      Capacity forecast      │  │           Unity XT          │  │           REST API          │   │
│   │        Perf analytics       │  │          PowerScale         │  │        Webhook alerts       │   │
│   │      Firmware advisory      │  │         Data Domain         │  │        Partner portal       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Dell hosts CloudIQ cloud-side; SCG appliance or VM per site relays array telemetry outbound        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │      Location     │     Protocol     │      Notes       │   │
│   │      Arrays      │   Data source    │    On-premises    │    REST/SCSI     │  Any Dell model  │   │
│   │       SCG        │   Relay agent    │    On-premises    │    HTTPS 443     │ VM or appliance  │   │
│   │     CloudIQ      │  Analytics SaaS  │     Dell cloud    │    HTTPS/REST    │   Multi-tenant   │   │
│   │    Consumers     │  Dashboard/API   │    Browser/app    │   HTTPS/OAuth    │    Ops teams     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SCG VM or appliance on management LAN per site · outbound 443 to cloudiq.dell.com        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CloudIQ        = Dell SaaS analytics platform; cloud-hosted; no on-prem server required            │
│    SCG            = Secure Connect Gateway; relay agent collecting and forwarding telemetry           │
│    Health score   = 0-100 integer computed per-array by CloudIQ ML models; 80+ is healthy             │
│    AIOps          = AI for IT operations; ML detects anomalies and predicts failures early            │
│    Telemetry      = Performance counters, capacity stats, event logs sent from array via SCG          │
│    Recommendation = Actionable CloudIQ suggestion to improve health or capacity posture               │
│    Firmware advisory = CloudIQ alert listing available firmware updates per array model               │
│    Capacity forecast = CloudIQ projection of when a pool or volume will run out of space              │
│    Anomaly        = Deviation from learned baseline; triggers alert if condition is sustained         │
│    Tenant         = CloudIQ org unit; maps to one Dell customer account; multi-site supported         │
│    REST API       = CloudIQ public API for querying health data, metrics, and alert management        │
│    SupportAssist  = Integration with Dell support for automatic SR creation on P1 events              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/"><strong>Operations</strong><span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Authentication, access control, encryption, and hardening.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostics, and escalation.</span></a>
</div>
