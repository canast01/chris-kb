# AWS VPC Flow Logs


<div class="kb-summary">
AWS VPC Flow Logs reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌─────────────────────────────── VPC Flow Logs — Network Traffic Capture ───────────────────────────────┐
│                                                                                                       │
│  VPC Flow Logs capture metadata about IP traffic to/from ENIs for security and troubleshooting.       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Capture Scope                 │  │              Log Record Fields              │   │
│   │          VPC level: all ENIs in VPC          │  │        srcaddr, dstaddr: IP addresses       │   │
│   │       Subnet level: all ENIs in subnet       │  │        srcport, dstport: port numbers       │   │
│   │        ENI level: specific interface         │  │        protocol: 6=TCP 17=UDP 1=ICMP        │   │
│   │      Accepted, rejected, or all traffic      │  │           action: ACCEPT or REJECT          │   │
│   │      Custom fields: add/remove columns       │  │        bytes, packets: volume metrics       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Flow logs delivered to S3 or CloudWatch Logs; query with Athena or Logs Insights.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Destinations                 │  │              Analysis Use Cases             │   │
│   │      S3: Athena queries; Parquet format      │  │         Security: detect port scans         │   │
│   │      CloudWatch Logs: Insights queries       │  │      Compliance: audit traffic patterns     │   │
│   │      Kinesis Firehose: real-time stream      │  │     Troubleshoot: find rejected traffic     │   │
│   │      Aggregation interval: 1 or 10 min       │  │        Optimize: identify top talkers       │   │
│   │     Cross-account S3 delivery supported      │  │       GuardDuty: uses flow logs input       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS VPC data plane capture agents · S3/CloudWatch Logs storage infrastructure                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Flow log record = Single aggregated capture of a traffic flow over the interval                      │
│  Aggregation interval= 1 or 10 minutes; shorter captures flows faster but costs more                  │
│  action field    = ACCEPT = SG+NACL allowed; REJECT = SG or NACL denied the flow                      │
│  NODATA          = No traffic was recorded during the aggregation interval                            │
│  SKIPDATA        = Capacity constraints skipped some records during the interval                      │
│  Custom format   = Choose which fields to include; reduces storage cost                               │
│  Parquet format  = Columnar S3 delivery; faster Athena queries and lower scan cost                    │
│  Athena query    = SQL against S3 flow logs via Glue table; pay per TB scanned                        │
│  GuardDuty input = GuardDuty ingests flow logs to detect anomalous traffic patterns                   │
│  Not real-time   = Flow logs are near-real-time; not suitable for live blocking                       │
│  Cost            = Charged for data ingestion; S3 cheaper than CloudWatch Logs                        │
│  IAM role        = Required to grant VPC Flow Logs permission to deliver records                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS VPC Flow Logs notes for day-to-day infrastructure operations.

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
