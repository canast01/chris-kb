# AWS IAM Policies

```text
┌───────────────────────────────────── AWS Identity — IAM Policies ─────────────────────────────────────┐
│                                                                                                       │
│  IAM policy structure: Effect, Action, Resource, Condition — with evaluation logic.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Policy Structure               │  │               Policy Elements               │   │
│   │             Version: 2012-10-17              │  │            Effect: Allow or Deny            │   │
│   │          Statement: array of rules           │  │             Action: s3:GetObject            │   │
│   │           Sid: optional identifier           │  │              Resource: ARN or *             │   │
│   │        Principal: who (resource pol)         │  │         Condition: context key check        │   │
│   │        NotAction/NotResource: invert         │  │        Multiple statements: all eval        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  All statements evaluated; explicit deny in any statement wins over any allow                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Common Conditions               │  │               Policy Examples               │   │
│   │          aws:MultiFactorAuthPresent          │  │         S3 read-only: s3:Get* on ARN        │   │
│   │             aws:RequestedRegion              │  │         EC2 start/stop: specific IDs        │   │
│   │              aws:PrincipalOrgID              │  │          Require tag: StringEquals          │   │
│   │           aws:SourceIp: CIDR check           │  │          Deny if no MFA: condition          │   │
│   │          aws:TagKeys: enforce tags           │  │         Region lock: NotAction+Deny         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IAM policy engine (global) · STS context · CloudTrail · IAM Access Analyzer                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Statement       = Single permission rule with Effect, Action, Resource, Condition                    │
│  Action          = AWS API call: s3:PutObject, ec2:DescribeInstances                                  │
│  Resource ARN    = Amazon Resource Name identifying specific resource                                 │
│  Condition block = Optional; adds context constraints to when policy applies                          │
│  StringEquals    = Condition operator for exact string match                                          │
│  NotAction       = Matches every action except those listed; use carefully                            │
│  aws:PrincipalOrgID= Condition key matching requesting account org membership                         │
│  aws:SourceIp    = Condition key matching caller IP; only works for direct calls                      │
│  aws:VpcSourceIp = Condition key matching caller IP when going through VPC endpoint                   │
│  IAM Access Analyzer= Scans policies for external access and validates syntax                         │
│  Policy simulator= IAM console tool testing policy effect on specific API calls                       │
│  Version 2012-10-17= Current policy language version; always include this                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS IAM Policies notes for day-to-day infrastructure operations.

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
