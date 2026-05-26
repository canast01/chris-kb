# AWS CloudWatch

```
┌─────────────────────────────── CloudWatch — Unified AWS Observability ────────────────────────────────┐
│                                                                                                       │
│  CloudWatch collects metrics, logs, and traces to provide observability across all AWS services.      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Data Sources                 │  │              Core Capabilities              │   │
│   │      AWS services: auto-publish metrics      │  │       Metrics: time-series data points      │   │
│   │      EC2: CloudWatch agent on instances      │  │      Dashboards: cross-service widgets      │   │
│   │          Custom: PutMetricData API           │  │        Alarms: threshold-based alerts       │   │
│   │         Logs: CloudWatch Logs groups         │  │        Logs Insights: query log data        │   │
│   │      X-Ray: distributed trace segments       │  │     Container Insights: EKS/ECS metrics     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Metrics retained 15 months; alarms evaluate period-by-period and notify via SNS/action.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Alarms & Actions               │  │              Advanced Features              │   │
│   │      Threshold: static value comparison      │  │        Anomaly detection: ML baseline       │   │
│   │        Composite alarms: AND/OR logic        │  │      Metric math: cross-metric formulas     │   │
│   │       Actions: SNS, EC2, Auto Scaling        │  │     Contributor Insights: top-N analysis    │   │
│   │     Alarm states: OK/ALARM/INSUFFICIENT      │  │    ServiceLens: trace-metric correlation    │   │
│   │       Suppression: maintenance window        │  │      Synthetics: canary endpoint tests      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional CloudWatch endpoints · S3 backend for log storage · Global backbone                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Namespace       = Logical grouping of metrics, e.g. AWS/EC2, AWS/RDS, Custom/App                     │
│  Dimension       = Key-value pair that identifies a metric, e.g. InstanceId=i-12345                   │
│  Period          = Granularity of metric data points: 1s, 10s, 30s, or multiples of 60                │
│  Statistics      = Aggregation function: Average, Sum, Min, Max, SampleCount, pNN.NN                  │
│  High-resolution = Sub-minute metric with 1s/10s/30s period (custom metrics only)                     │
│  Composite alarm = Alarm that evaluates other alarms with Boolean (AND/OR/NOT) logic                  │
│  Metric math     = Formula combining multiple metrics, e.g. CPUUtilization/100                        │
│  Anomaly detection= ML model trained on metric history to define expected band                        │
│  Contributor Insights= Identifies top-N callers or keys driving a metric spike                        │
│  ServiceLens     = Integrates X-Ray traces with CloudWatch metrics and alarms                         │
│  Synthetics canary= Scripted browser/API test that checks endpoints on a schedule                     │
│  Container Insights= Enhanced metrics for EKS nodes, pods, and containers                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS CloudWatch notes for day-to-day infrastructure operations.

## Where It Fits

Use this page for build work, support checks, troubleshooting, standards, and operational review.

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Confirm service health. |  |  |
| Review alerts. |  |  |
| Check recent changes. |  |  |
| Confirm capacity and performance are within normal range. |  |  |

## Health Commands

~~~bash
# Add environment-specific commands here
~~~

## Common Issues

- Misconfiguration after change work.
- Missing access or permissions.
- Alert noise without clear ownership.
- Drift from documented standards.

## Operational Tasks

| Task | Command |
|---|---|
| Review current configuration. |  |
| Validate dependencies. |  |
| Record changes. |  |
| Confirm monitoring coverage. |  |

## Upgrade Notes

- Check release notes before upgrades.
- Validate backup or rollback options.
- Confirm maintenance window and communication plan.
- Test after the change.

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Document ownership. | Document ownership. |
| Use least privilege access. | Use least privilege access. |
| Validate changes after implementation. | Validate changes after implementation. |
