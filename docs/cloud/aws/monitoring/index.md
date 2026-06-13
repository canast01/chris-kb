---
tags:
  - aws
---
# AWS Monitoring

<div class="kb-summary">
AWS observability is built on CloudWatch (metrics, logs, alarms), CloudTrail (API audit trail), and EventBridge (event-driven automation). Coverage includes CloudWatch Agent for OS-level metrics, alarm standards, log retention, and AWS Health for service incident visibility.
</div>

```text
┌─────────────────────────────────────── AWS Monitoring Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    AWS Monitoring — CloudWatch, CloudTrail, and EventBridge                   │   │
│   │   CloudWatch: metrics, logs, alarms, dashboards — native to every AWS service; no agent for   │   │
│   │CloudWatch Agent: installs on EC2 for OS-level metrics (memory, disk) and custom log forwarding│   │
│   │    CloudTrail: API audit log; every AWS API call recorded; multi-region trail ships to S3 +   │   │
│   │       EventBridge: event bus routing rules to targets (Lambda, SNS, SQS, Step Functions,      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CloudWatch collects metrics/logs · CloudTrail audits API calls                                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          CloudWatch         │  │          CloudTrail         │  │         EventBridge         │   │
│   │  Metrics: service built-in  │  │   API calls: all services   │  │ Event bus: default + custom │   │
│   │   Logs: groups + retention  │  │   Multi-region trail: org   │  │  Rules: event pattern match │   │
│   │   Alarms: threshold → SNS   │  │   S3: log delivery + lock   │  │   Targets: Lambda/SQS/SNS   │   │
│   │   Dashboards: metric tiles  │  │   Log integrity validation  │  │  Schedule: cron-like rules  │   │
│   │  Metric filters: log→metric │  │   Athena: query trail logs  │  │    X-acct event bus pipe    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    CloudWatch collects and alerts · CloudTrail records who did what · EventBridge automates responses │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    CloudWatch    │     CW Logs      │     CW Alarms     │    CloudTrail    │   EventBridge    │   │
│   │ Metric: CPUUtil  │  Log group: 30d  │   Alarm: CPU>80%  │  Org trail: all  │  Rule: EC2 stop  │   │
│   │  Dashboard: ops  │  Metric filter   │    Action: SNS    │   S3 delivery    │  Target: Lambda  │   │
│   │ Agent: mem/disk  │ Insights: query  │  Composite alarm  │   Athena query   │  Schedule rule   │   │
│   │ AWS Health: svc  │ Subscription flt │     OK → ALARM    │ Integrity check  │   X-acct pipe    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS CloudWatch backend · S3 for CloudTrail · EventBridge event bus infrastructure · SNS topics       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudWatch metrics = Time-series data from AWS services; 1-min granularity; stored 15 months         │
│  Log group         = CloudWatch Logs container for streams; retention 1 day–10 years or indefinite    │
│  Metric filter     = Extracts numeric values from log events and publishes them as CloudWatch metrics │
│  CW Alarm          = Watches a metric or expression; transitions OK/ALARM/INSUFFICIENT; triggers      │
│  Composite alarm   = AND/OR combination of alarms; reduces alert noise from correlated conditions     │
│  CloudTrail        = Records management events (API calls) and optionally data events (S3/Lambda)     │
│  Org trail         = Single CloudTrail covering all accounts in the AWS Organization; recommended     │
│  Log file integrity= CloudTrail SHA-256 hash validation; detects tampered or deleted log files        │
│  EventBridge rule  = Pattern-matches incoming events and routes them to one or more targets           │
│  AWS Health        = Service health and scheduled events for your specific AWS account and resources  │
│  CloudWatch Agent  = Daemon on EC2/on-prem; collects OS metrics (memory, disk) and custom log files   │
│  Logs Insights     = Interactive CloudWatch Logs query engine; KQL-like syntax; serverless execution  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

![AWS Monitoring Architecture](../../../assets/aws-monitoring-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cloudwatch/">
  <strong>CloudWatch</strong>
  <span>Metrics, dashboards, alarms, and operational visibility.</span>
</a>

<a class="kb-card" href="cloudwatch-logs/">
  <strong>CloudWatch Logs</strong>
  <span>Log groups, retention, metric filters, and search patterns.</span>
</a>

<a class="kb-card" href="cloudwatch-alarms/">
  <strong>CloudWatch Alarms</strong>
  <span>Alarm standards, thresholds, actions, and review.</span>
</a>

<a class="kb-card" href="cloudtrail/">
  <strong>CloudTrail</strong>
  <span>API audit logs, event history, trails, and investigations.</span>
</a>

<a class="kb-card" href="eventbridge/">
  <strong>EventBridge</strong>
  <span>Rules, event buses, schedules, and automation triggers.</span>
</a>

<a class="kb-card" href="aws-health/">
  <strong>AWS Health</strong>
  <span>Service health, account events, and operational impact review.</span>
</a>

</div>
