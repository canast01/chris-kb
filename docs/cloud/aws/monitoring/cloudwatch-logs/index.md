# AWS CloudWatch Logs


<div class="kb-summary">
AWS CloudWatch Logs reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌────────────────────────────────── CloudWatch Logs — Log Management ───────────────────────────────────┐
│                                                                                                       │
│  CloudWatch Logs ingests, stores, and queries log data from AWS services and applications.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Ingestion                 │  │             Storage & Retention             │   │
│   │      CloudWatch agent: EC2/on-prem logs      │  │       Log groups: top-level container       │   │
│   │       AWS services: auto-publish logs        │  │      Log streams: per instance/resource     │   │
│   │     Lambda: stdout/stderr auto-captured      │  │         Retention: 1 day to 10 years        │   │
│   │        VPC Flow Logs: network traffic        │  │         Encryption: KMS CMK on group        │   │
│   │      PutLogEvents API: custom app logs       │  │       Export: S3 bucket for long-term       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Metric filters convert log patterns to metrics; subscriptions stream logs to destinations.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Analysis                   │  │            Destinations & Actions           │   │
│   │        Logs Insights: query language         │  │       Metric filter: pattern → metric       │   │
│   │       Fields, filter, stats, sort cmds       │  │     Subscription filter: Kinesis/Lambda     │   │
│   │      Visualize: time-series bar charts       │  │       Cross-account delivery: log sink      │   │
│   │     Save queries: reuse across sessions      │  │      CloudWatch Alarm on metric filter      │   │
│   │      Live tail: real-time log streaming      │  │       OpenSearch: subscription export       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS CloudWatch Logs storage infrastructure · Kinesis data plane · Regional endpoints                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Log group       = Top-level container for logs; retention and encryption set here                    │
│  Log stream      = Sequence of log events from a single source within a log group                     │
│  Log event       = Timestamped record with a message string; basic unit of log data                   │
│  Metric filter   = Pattern match on log events that increments a custom CloudWatch metric             │
│  Subscription filter= Delivers matching log events in real time to Kinesis, Lambda, or Firehose       │
│  Logs Insights   = Query engine for CloudWatch Logs using a purpose-built query language              │
│  fields command  = Logs Insights: selects specific fields from JSON-structured log events             │
│  filter command  = Logs Insights: includes/excludes events matching a pattern or condition            │
│  stats command   = Logs Insights: aggregates field values with count, sum, avg, min, max              │
│  Live tail       = Real-time streaming view of incoming log events in the console                     │
│  Log sink        = Cross-account/cross-region log delivery destination for centralisation             │
│  Export to S3    = Batch export of log data to S3; not real-time; use subscription instead            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS CloudWatch Logs notes for day-to-day infrastructure operations.

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
