# AWS Lambda


<div class="kb-summary">
AWS Lambda reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌──────────────────────────────────────── AWS Compute — Lambda ─────────────────────────────────────────┐
│                                                                                                       │
│  Serverless function execution: triggers, runtimes, concurrency, VPC, and observability.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Function Configuration            │  │                   Triggers                  │   │
│   │         Runtime: Python/Node/Java/Go         │  │           API Gateway: HTTP invoke          │   │
│   │              Memory: 128MB–10GB              │  │              S3: object events              │   │
│   │           Timeout: max 15 minutes            │  │         SQS/SNS: message processing         │   │
│   │        Ephemeral storage: /tmp 512MB+        │  │         EventBridge: scheduled/event        │   │
│   │       IAM execution role: permissions        │  │          DynamoDB/Kinesis: streams          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Triggers invoke function; execution role grants AWS service access during run                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Concurrency and Scaling            │  │                Observability                │   │
│   │        Burst: 3000 initial, +500/min         │  │         CloudWatch Logs: auto-stream        │   │
│   │          Reserved concurrency: cap           │  │          X-Ray: distributed tracing         │   │
│   │          Provisioned: pre-warm exec          │  │         Insights: cold start metric         │   │
│   │          VPC: ENI in private subnet          │  │          Errors: DLQ or on-failure          │   │
│   │          Cold start: init overhead           │  │         Alarm: error rate threshold         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Lambda micro-VMs (Firecracker) · VPC ENI (if VPC mode) · CloudWatch · X-Ray                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Firecracker     = AWS micro-VM; provides isolation between Lambda executions                         │
│  Cold start      = Latency when Lambda initialises a new execution environment                        │
│  Provisioned concurrency= Pre-warms execution environments; eliminates cold start                     │
│  Reserved concurrency= Caps max executions; guarantees capacity but limits scale                      │
│  DLQ             = Dead Letter Queue; receives events that failed after retries                       │
│  Execution role  = IAM role assumed by Lambda to access S3, DynamoDB, etc.                            │
│  VPC mode        = Lambda ENI placed in VPC subnet; accesses private resources                        │
│  X-Ray           = AWS distributed tracing; shows latency across service calls                        │
│  Burst limit     = Account-level max new concurrent executions per minute                             │
│  Ephemeral /tmp  = Writable scratch space; max 10GB; not shared between invocations                   │
│  Lambda layer    = Shared libraries or runtimes attached to functions                                 │
│  Event source map= Polls SQS/Kinesis/DynamoDB and invokes Lambda with batches                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Lambda notes for day-to-day infrastructure operations.

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
