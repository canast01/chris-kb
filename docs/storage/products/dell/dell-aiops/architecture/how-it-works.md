---
tags:
  - architecture
  - dell
description: "How It Works reference covering Architecture, Component Roles, AIOps Capabilities, Telemetry Sources, Data Flow."
---
# Dell AIOps — How It Works

<div class="kb-summary">
How It Works reference covering Architecture, Component Roles, AIOps Capabilities, Telemetry Sources, Data Flow.

*Applies to: Dell AIOps*
</div>
![Dell AIOps — How It Works](../../../../../assets/storage-dell-dell-aiops-architecture-how-it-works.svg)

Dell AIOps (delivered via CloudIQ / APEX AIOps) is Dell's AI-driven IT operations platform providing anomaly detection, root cause analysis, and predictive recommendations across the Dell storage estate. The platform is fully SaaS-delivered — the only customer-managed component is the Secure Connect Gateway (SCG) virtual appliance.

---

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Storage Arrays\n(PowerMax / PowerStore)" as ARR
participant "Compute\n(vSphere / Bare Metal)" as COMP
participant "Network\n(switches / HBAs)" as NET
participant "Dell AIOps\nPlatform" as AIO
participant "ML Inference\nEngine" as ML
actor "Ops Team" as OPS

ARR -> AIO: Performance + capacity telemetry
COMP -> AIO: Host metrics
NET -> AIO: Flow + error telemetry
AIO -> ML: Correlate cross-domain signals
ML --> AIO: Root cause + impact analysis
AIO -> OPS: Unified alert with context
OPS -> AIO: Acknowledge + annotate
AIO -> ML: Feedback loop (improve model)
@enduml
```

## Architecture

```d2
direction: right

Sources: "Storage Arrays · PowerStore · PowerMax ·\nPowerScale · Unity XT · Data Domain" {shape: rectangle}
SCG: "Secure Connect Gateway · on-prem OVA · polls every\n5 min · HTTPS outbound only" {shape: rectangle}
AIPipeline: "Dell AI Pipeline · cloud-managed · anomaly\ndetection · RCA · capacity forecasting" {shape: rectangle}
Console: "CloudIQ / APEX Console · SaaS portal ·\nrecommendations · health scores · alerts" {shape: rectangle}
Notify: "Notification Channels · PagerDuty · email ·\nwebhooks · ITSM" {shape: rectangle}

Sources -> SCG
SCG -> AIPipeline
AIPipeline -> Console
Console -> Notify
```

---

## Component Roles

| Component | Role |
|---|---|
| CloudIQ / APEX Console | SaaS portal — surfacing recommendations, anomaly dashboard, health scores |
| Secure Connect Gateway (SCG) | On-premises telemetry collection and secure forwarding agent (customer-managed) |
| Dell AI Pipeline (cloud) | Anomaly detection, root cause analysis, and capacity forecasting (Dell-managed) |
| Storage Arrays | Telemetry data sources: PowerStore, PowerMax, PowerScale, Unity XT, Data Domain |

---

## AIOps Capabilities

### Anomaly Detection

Dell AIOps analyses rolling telemetry baselines for each array and surfaces anomalies when metrics deviate significantly from the learned pattern:

- **Performance anomalies**: unexpected latency or IOPS deviations
- **Capacity anomalies**: faster-than-expected capacity growth
- **Configuration drift**: changes from a known-good configuration state

### Root Cause Analysis (RCA)

When an anomaly or health score degradation is detected, AIOps cross-correlates telemetry across the stack to identify likely root causes and generates a ranked list of contributing factors.

### Capacity Forecasting

ML-based capacity models predict when a system will reach capacity thresholds:

- Days until raw capacity threshold (configured at 85%)
- Projected capacity at 30, 60, and 90 days
- Recommended actions (expand, thin provision, tier, etc.)

### Recommendations

| Severity | Examples |
|---|---|
| Critical | Imminent capacity exhaustion, hardware fault requiring immediate action |
| High | Performance degradation root cause identified, firmware vulnerability |
| Medium | Sub-optimal configuration, approaching threshold |
| Low | Best-practice suggestion, non-urgent tuning |

---

## Telemetry Sources

| Platform | Metrics Collected |
|---|---|
| PowerStore | IOPS, latency, throughput, capacity, hardware faults |
| PowerMax | SRDF replication lag, cache hit rates, capacity, performance |
| PowerScale (Isilon) | Protocol throughput, CPU, capacity, SmartPools usage |
| Unity XT | LUN performance, capacity, replication health |
| Data Domain | Dedup ratio, capacity, replication |

---

## Data Flow

1. SCG polls each array's management API at regular intervals (typically every 5 minutes)
2. SCG encrypts and forwards telemetry to Dell's cloud AI pipeline over HTTPS
3. Dell AI models process telemetry against learned baselines and generate anomaly/recommendation events
4. Recommendations and anomaly events appear in the CloudIQ APEX Console within 15–30 minutes of detection
5. Notification rules in CloudIQ deliver alerts to configured channels (PagerDuty, email, webhooks)

---

## See also

- [Dell Aiops — Design Standards](../design-standards/)
- [Dell Aiops — Integrations](../integrations/)
- [Dell Aiops — Deploy](../../deploy/)
