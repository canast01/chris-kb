# AWS Cross-Account Access

```text
┌───────────────────────────────── AWS Identity — Cross-Account Access ─────────────────────────────────┐
│                                                                                                       │
│  Cross-account IAM role assumption enables multi-account access without static keys.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Role Assumption Flow             │  │                 Trust Policy                │   │
│   │          1. Source calls AssumeRole          │  │         Principal: source account ID        │   │
│   │        2. STS validates trust policy         │  │            Action: sts:AssumeRole           │   │
│   │          3. STS returns temp creds           │  │            Condition: ExternalId            │   │
│   │        4. Caller uses creds in target        │  │           Condition: MFA required           │   │
│   │         5. Creds expire: max 12 hrs          │  │          Condition: source IP range         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Source needs permission to call sts:AssumeRole; target role trust policy allows it                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             IAM Identity Center              │  │           Resource-Based Policies           │   │
│   │         Permission set: wrapped role         │  │         S3 bucket policy: cross-acct        │   │
│   │         SSO: human cross-acct login          │  │          KMS key policy: cross-acct         │   │
│   │           No long-term keys needed           │  │         SNS/SQS: cross-acct publish         │   │
│   │          Centralised access portal           │  │             ECR: cross-acct pull            │   │
│   │        Audit: CloudTrail per account         │  │           No assume needed: direct          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  STS (global) · IAM policy engine · CloudTrail · IAM Identity Center                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AssumeRole      = STS API call exchanging identity for temp role credentials                         │
│  Trust policy    = JSON on target role specifying who can assume it                                   │
│  ExternalId      = Secret condition value preventing confused deputy attacks                          │
│  Confused deputy = Attack where trusted third party is tricked into acting on attacker                │
│  STS             = Security Token Service; issues temporary credentials                               │
│  Temp credentials= Access key + secret + session token; expire in 15min–12hr                          │
│  Session token   = Third credential component required with temp access keys                          │
│  Permission set  = IAM Identity Center construct wrapping cross-account role                          │
│  Resource policy = Policy on resource (S3/KMS/SNS) granting cross-account access                      │
│  Max session     = AssumeRole --duration-seconds; max 43200 (12 hours)                                │
│  Org condition   = aws:PrincipalOrgID condition restricts to accounts in same org                     │
│  CloudTrail      = Both source and target account record the AssumeRole event                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Cross-Account Access notes for day-to-day infrastructure operations.

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
