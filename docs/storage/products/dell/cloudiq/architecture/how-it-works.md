---
tags:
  - architecture
  - dell
---
# CloudIQ — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Data Pipeline Topology, How It Works, Supported Platforms, Key Capabilities.

*Applies to: CloudIQ*
</div>
![CloudIQ — How It Works](../../../../../assets/storage-dell-cloudiq-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Dell Storage Array\n(PowerMax / PowerStore / etc.)" as ARR
participant "SRS / Secure Connect\nGateway" as SCG
participant "CloudIQ\nSaaS (cloud.dell.com)" as CIQ
participant "AI / ML Engine" as AI
actor "Admin" as ADM

ARR -> SCG: Telemetry (metrics, logs, config)
SCG -> CIQ: Encrypted upload (HTTPS)
CIQ -> AI: Anomaly detection + capacity forecast
AI --> CIQ: Health score + recommendations
CIQ --> ADM: Dashboard + proactive alerts
ADM -> CIQ: View performance / capacity trend
CIQ -> ADM: Predictive report
@enduml
```

## Overview

Dell CloudIQ is a cloud-native AIOps SaaS platform hosted by Dell. It receives telemetry from on-premises Dell infrastructure via the Secure Connect Gateway (SCG) and processes it through machine-learning models to produce health scores, capacity forecasts, and anomaly alerts. CloudIQ requires no on-premises compute beyond the SCG appliance — all analytics run in Dell's cloud.

## Data Pipeline Topology

![Data Pipeline Topology](../../../../../assets/storage-dell-cloudiq-architecture-how-it-works-mermaid-svg.svg)

## How It Works

1. Each on-premises Dell storage system is registered to an SCG appliance
2. The SCG polls the registered systems for telemetry (capacity metrics, performance counters, hardware health) and forwards it to the Dell CloudIQ back-end over outbound HTTPS (port 443)
3. CloudIQ ingests the telemetry, applies ML-based health scoring, and generates alerts when scores drop or anomalies are detected
4. Users access results via the CloudIQ web dashboard or the REST API
5. Notifications are sent via email or webhook based on configured notification rules

CloudIQ health scores range from 0 to 100. Scores below 80 indicate a condition requiring attention; scores below 60 are typically active hardware or configuration alerts.

## Supported Platforms

| Platform | Telemetry Source |
|---|---|
| PowerMax / VMAX | Embedded telemetry agent |
| Unity XT | CloudIQ data collection service |
| PowerScale (Isilon) | OneFS embedded agent |
| PowerStore | REST API |
| PowerFlex (VxFlex OS) | SDC telemetry |
| XtremIO | REST API |

## Key Capabilities

| Capability | Description |
|---|---|
| Health scoring | 0–100 score per system; ML-based anomaly detection flags degraded conditions |
| Capacity forecasting | Trend-based projection of when systems will reach capacity thresholds |
| Proactive recommendations | AI-generated configuration and performance improvement suggestions |
| Cross-platform visibility | Unified dashboard across all registered Dell systems |
| API access | REST API for integrating CloudIQ data into ITSM and capacity planning tools |

---

## See also

- [Cloudiq — Design Standards](../design-standards/)
- [Cloudiq — Integrations](../integrations/)
- [Cloudiq — Deploy](../../deploy/)
