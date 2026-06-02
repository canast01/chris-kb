# AWS EventBridge


<div class="kb-summary">
AWS EventBridge reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌──────────────────────────────── EventBridge — Event-Driven Automation ────────────────────────────────┐
│                                                                                                       │
│  EventBridge routes events from AWS services, custom apps, and SaaS to processing targets.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Event Sources                 │  │               Event Bus Types               │   │
│   │      AWS services: state-change events       │  │     Default bus: all AWS service events     │   │
│   │       Custom apps: PutEvents API calls       │  │       Custom bus: app/domain isolation      │   │
│   │       SaaS partners: Zendesk, Datadog        │  │       Partner bus: SaaS source events       │   │
│   │       Scheduled: cron/rate expressions       │  │        Pipes: filtered point-to-point       │   │
│   │     Cross-account: resource-based policy     │  │       Global endpoint: multi-region HA      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Rules match event patterns and route to targets; multiple targets per rule supported.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Rules & Patterns               │  │                   Targets                   │   │
│   │      Event pattern: JSON field matching      │  │           Lambda: invoke function           │   │
│   │      Prefix/suffix/exists/anything-but       │  │            SNS/SQS: fan-out/queue           │   │
│   │      Input transformer: reshape payload      │  │           Step Functions: workflow          │   │
│   │      Schedule: cron(0 12 * * ? *) expr       │  │           Kinesis Firehose: stream          │   │
│   │         DLQ: failed delivery capture         │  │        EventBridge bus: cross-account       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional EventBridge endpoints · Multi-AZ event bus infrastructure · Global backbone             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Event           = JSON document with source, detail-type, detail, and metadata fields                │
│  Event bus       = Channel receiving events; rules attached to a bus filter and route                 │
│  Rule            = Evaluates event pattern match and routes matching events to targets                │
│  Event pattern   = JSON filter defining which events a rule matches, field by field                   │
│  Input transformer= Modifies the event payload before delivery to the target                          │
│  Schedule        = Cron or rate expression triggering a rule on a time basis                          │
│  DLQ             = Dead-letter queue capturing events that failed target delivery                     │
│  Pipes           = Point-to-point integration with filter, enrich, and transform stages               │
│  Partner event source= SaaS provider sending events directly to EventBridge partner bus               │
│  Global endpoint = Two-bus active-active across two regions; automatic event replication              │
│  PutEvents API   = SDK/CLI method to send custom events to an event bus                               │
│  detail-type     = Human-readable string classifying the event, e.g. EC2 Instance State-change        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS EventBridge notes for day-to-day infrastructure operations.

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
