# AWS VPC Endpoints


<div class="kb-summary">
AWS VPC Endpoints reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────── VPC Endpoints — Private AWS Service Access ──────────────────────────────┐
│                                                                                                       │
│  VPC Endpoints connect your VPC to AWS services privately without NAT, IGW, or internet.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Gateway Endpoints               │  │      Interface Endpoints (PrivateLink)      │   │
│   │        Services: S3 and DynamoDB only        │  │           Services: most AWS APIs           │   │
│   │      Route table entry: no ENI created       │  │          ENI in subnet: private IP          │   │
│   │             No cost: free to use             │  │         Hourly + data processing fee        │   │
│   │     Policy: restrict bucket/table access     │  │         Policy: restrict API actions        │   │
│   │        Regional; DNS unchanged for S3        │  │        Private DNS: resolve to ENI IP       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Interface endpoints use PrivateLink; traffic stays on AWS backbone; no public internet hop.          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Endpoint Policies               │  │                  Use Cases                  │   │
│   │       JSON resource policy on endpoint       │  │          Private Lambda → S3 no NAT         │   │
│   │      Restrict: specific S3 buckets only      │  │          EC2 → SSM without internet         │   │
│   │        Condition: aws:SourceVpc check        │  │        Compliance: no internet egress       │   │
│   │       Combine with SCP to enforce use        │  │           Reduce NAT GW data costs          │   │
│   │      Audit: CloudTrail endpoint events       │  │      Cross-account via shared endpoint      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS internal backbone · PrivateLink infrastructure per AZ · Regional service endpoints               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Gateway endpoint= Route-table-based endpoint for S3 and DynamoDB; free; regional                     │
│  Interface endpoint= ENI-based PrivateLink endpoint for most AWS services; has ENI IP                 │
│  PrivateLink      = AWS technology powering interface endpoints over internal backbone                │
│  Private DNS      = Endpoint option that resolves service FQDN to private ENI IP                      │
│  Endpoint policy  = IAM resource policy on the endpoint restricting allowed actions                   │
│  aws:SourceVpc    = Condition key used in bucket policies to enforce endpoint usage                   │
│  S3 bucket policy = Deny s3:* unless aws:SourceVpc matches your VPC endpoint                          │
│  Endpoint SG      = Security group on interface endpoint ENI controlling access                       │
│  Cross-account    = Interface endpoint can be shared to other accounts via RAM                        │
│  Cost benefit     = Eliminates NAT GW data processing fee for S3/DynamoDB traffic                     │
│  SSM endpoint     = ssm, ssmmessages, ec2messages endpoints needed for Session Manager                │
│  Endpoint DNS     = Regional + AZ-specific DNS names provided by interface endpoints                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS VPC Endpoints notes for day-to-day infrastructure operations.

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
