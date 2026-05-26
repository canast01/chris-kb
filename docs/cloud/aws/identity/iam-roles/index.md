# AWS IAM Roles

```
┌────────────────────────────────────── AWS Identity — IAM Roles ───────────────────────────────────────┐
│                                                                                                       │
│  IAM roles provide temporary credentials for services, cross-account, and federation.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Role Types                  │  │                 Trust Policy                │   │
│   │         Service role: EC2/Lambda/EKS         │  │        Principal: service or account        │   │
│   │          Cross-account: AssumeRole           │  │            Action: sts:AssumeRole           │   │
│   │            Federation: SAML/OIDC             │  │          Condition: ExternalId/MFA          │   │
│   │        Instance profile: EC2 wrapper         │  │        sts:AssumeRoleWithWebIdentity        │   │
│   │         Linked service role: AWS mgd         │  │            sts:AssumeRoleWithSAML           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Trust policy defines who can assume; permission policy defines what they can do                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Role Session                 │  │                Best Practices               │   │
│   │           Duration: 15min–12hr max           │  │          No static keys: use roles          │   │
│   │        Session name: caller identity         │  │        Least privilege: minimal perms       │   │
│   │          Session tags: pass context          │  │           IRSA: K8s pod-level role          │   │
│   │         Session policy: narrow scope         │  │          Permission boundary: devs          │   │
│   │         Revoke: invalidate sessions          │  │        Review: quarterly unused roles       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  STS (global) · IAM policy engine · CloudTrail · OIDC provider · SAML IdP                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Trust policy    = JSON on role defining which principals can assume it                               │
│  AssumeRole      = STS call returning temporary access key + secret + token                           │
│  Service role    = Role a service (Lambda, EC2) assumes; defined in trust policy                      │
│  Instance profile= Wrapper allowing IAM role to be attached to EC2 instance                           │
│  IRSA            = IAM Roles for Service Accounts; EKS pod assumes IAM role via OIDC                  │
│  Session tag     = Key-value pair attached to role session; flows into policy conditions              │
│  Session policy  = Additional inline policy narrowing role permissions at assume time                 │
│  Linked service role= Role created and managed by AWS for a specific service                          │
│  OIDC provider   = IAM trust configuration for GitHub Actions, EKS, or Cognito                        │
│  Revoke sessions = Add deny policy with condition on token issue time                                 │
│  ExternalId      = Prevents confused deputy; required for third-party role assumptions                │
│  Permission boundary= IAM policy capping maximum role permissions; used for delegation                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS IAM Roles notes for day-to-day infrastructure operations.

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
