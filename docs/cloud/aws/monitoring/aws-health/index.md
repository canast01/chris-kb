# AWS Health


<div class="kb-summary">
AWS Health reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌──────────────────────────────── AWS Health — Service & Account Health ────────────────────────────────┐
│                                                                                                       │
│  AWS Health surfaces service events, scheduled maintenance, and account-specific issues.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Event Sources                 │  │               Health Dashboard              │   │
│   │       Service events: regional outages       │  │          Personal Health Dashboard          │   │
│   │     Account events: limit/config issues      │  │         AWS Status page: public view        │   │
│   │    Scheduled changes: maintenance windows    │  │       EventBridge integration: alerts       │   │
│   │   Operational notifications: best practice   │  │       Organizations view: all accounts      │   │
│   │   Investigations: active AWS support cases   │  │    API: DescribeEvents, DescribeAffected    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Events flow to EventBridge rules → SNS/Lambda; org-level view requires delegated admin.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              EventBridge Rules               │  │               Response Actions              │   │
│   │         Event pattern: source=health         │  │          SNS: notify on-call teams          │   │
│   │          Filter: eventTypeCategory           │  │       Lambda: auto-remediation scripts      │   │
│   │      Filter: specific services/regions       │  │      Slack/PagerDuty: incident creation     │   │
│   │      Cross-account: org-level event bus      │  │       ITSM: ServiceNow ticket creation      │   │
│   │       Archive: store all health events       │  │     Runbook: link affected resource ARN     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS global backbone · Regional control planes · Availability Zone infrastructure                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Personal Health Dashboard= Account-specific view of events affecting your resources                  │
│  Service Health Dashboard = Public AWS status page showing service health per region                  │
│  eventTypeCategory    = Classification: issue, scheduledChange, or accountNotification                │
│  eventTypeCode        = Specific event type, e.g. AWS_EC2_INSTANCE_STOP_SCHEDULED                     │
│  Affected entities    = Specific resource ARNs or account IDs impacted by the event                   │
│  Organizations view   = Aggregated health events across all accounts in the org                       │
│  Delegated admin      = Account designated to view org-wide health events via API                     │
│  EventBridge rule     = Pattern-matched rule forwarding health events to targets                      │
│  Scheduled change     = Planned AWS maintenance requiring customer action or awareness                │
│  Investigation        = Active AWS support engagement linked to a health event                        │
│  DescribeEvents API   = Lists health events matching filters; requires Business/Enterprise            │
│  Upcoming changes     = 14-day advance notice for planned infrastructure maintenance                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Health notes for day-to-day infrastructure operations.

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

```bash
# Add environment-specific commands here
```

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
