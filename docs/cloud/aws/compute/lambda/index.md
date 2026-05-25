# AWS Lambda
## Overview

AWS Lambda notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│                    Lambda Flow                          │
│                                                         │
│  Event Source                                           │
│  ├── API Gateway (HTTP request)                         │
│  ├── S3 (object created / deleted)                      │
│  ├── EventBridge (scheduled / rule match)               │
│  ├── SQS / SNS (message received)                       │
│  └── DynamoDB Streams (record change)                   │
│        │                                                │
│        ▼                                                │
│  Lambda Function (runtime: Python · Node · Java …)      │
│  ├── Execution role (IAM)                               │
│  ├── Environment variables                              │
│  └── VPC config (optional — for private resource access)│
│        │                                                │
│        ▼                                                │
│  Result / side effects (write to S3 · call API …)       │
└─────────────────────────────────────────────────────────┘
```

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
