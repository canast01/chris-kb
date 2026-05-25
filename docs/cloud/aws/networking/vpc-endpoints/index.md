# AWS VPC Endpoints
## Overview

AWS VPC Endpoints notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│                  VPC Endpoint Types                     │
│                                                         │
│  Gateway Endpoint (free)                                │
│  ├── Services: S3 · DynamoDB only                       │
│  └── Route table entry → prefix list → gateway ep       │
│                                                         │
│  Interface Endpoint (PrivateLink — hourly cost)         │
│  ├── Services: most AWS services (SSM · KMS · ECR …)    │
│  └── Creates ENI in subnet → private IP in VPC          │
│                                                         │
│  Without endpoint:  EC2 → NAT GW → IGW → S3             │
│  With endpoint:     EC2 → VPC Endpoint → S3             │
│  (stays on AWS backbone — no internet traversal)        │
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
