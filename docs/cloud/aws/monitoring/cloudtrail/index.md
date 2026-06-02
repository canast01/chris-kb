# AWS CloudTrail


<div class="kb-summary">
AWS CloudTrail reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌─────────────────────────────────── CloudTrail — API Audit Logging ────────────────────────────────────┐
│                                                                                                       │
│  CloudTrail records all AWS API calls for governance, compliance, and security investigation.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Trail Types                  │  │               Event Categories              │   │
│   │     Management trail: control-plane ops      │  │         Management events: API calls        │   │
│   │     Data trail: S3/Lambda data-plane ops     │  │        Data events: object read/write       │   │
│   │        Org trail: all accounts in org        │  │     Insights: unusual activity detection    │   │
│   │     Single-region vs multi-region trail      │  │      Read-only vs write-only filtering      │   │
│   │        Lake: SQL query across events         │  │       Exclude: high-volume read events      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Events delivered to S3 within ~15 min; CloudWatch Logs for real-time analysis.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Storage & Integrity              │  │             Analysis & Alerting             │   │
│   │     S3 bucket: log storage with SSE-KMS      │  │       CloudWatch Logs: metric filters       │   │
│   │     Log file validation: SHA-256 digest      │  │       Athena: ad-hoc SQL queries on S3      │   │
│   │        MFA delete: protect log bucket        │  │     CloudTrail Lake: managed SQL engine     │   │
│   │      Retention: S3 lifecycle to Glacier      │  │      Security Hub: CloudTrail findings      │   │
│   │      Replication: cross-region S3 copy       │  │     EventBridge: real-time rule triggers    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS global backbone · S3 storage infrastructure · Regional CloudTrail endpoints                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Trail           = Configuration defining which events to log and where to deliver them               │
│  Management event= Control-plane API call: CreateInstance, PutBucketPolicy, AttachRole                │
│  Data event      = Data-plane operation: S3 GetObject/PutObject, Lambda Invoke                        │
│  Insights event  = Anomaly detected: unusual API call rate or error rate spike                        │
│  Org trail       = Single trail that captures events from all member accounts in org                  │
│  Log file validation= Digest file lets you verify logs were not tampered after delivery               │
│  CloudTrail Lake = Managed event data store; query with SQL up to 7-year retention                    │
│  Event history   = 90-day free lookup without a trail; management events only                         │
│  userIdentity    = JSON field in each log record identifying who made the API call                    │
│  sourceIPAddress = IP or AWS service that originated the API call in the log record                   │
│  eventName       = Specific AWS API action recorded, e.g. RunInstances, DeleteBucket                  │
│  Athena query    = Ad-hoc SQL against CloudTrail JSON logs stored in S3 via Glue table                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS CloudTrail notes for day-to-day infrastructure operations.

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
