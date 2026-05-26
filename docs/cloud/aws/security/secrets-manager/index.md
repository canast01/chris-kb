# AWS Secrets Manager

```
┌─────────────────────────────── Secrets Manager — Credential Lifecycle ────────────────────────────────┐
│                                                                                                       │
│  Secrets Manager stores, rotates, and distributes credentials without hardcoding secrets.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Secret Storage                │  │                 Secret Types                │   │
│   │      JSON key-value or plaintext string      │  │         RDS credentials: auto-rotate        │   │
│   │            Encrypted with KMS CMK            │  │      API keys: manual or Lambda rotate      │   │
│   │       Versioned: AWSCURRENT/AWSPENDING       │  │          SSH keys: stored encrypted         │   │
│   │     Resource policy: cross-account share     │  │        OAuth tokens: Lambda rotation        │   │
│   │      Replication: cross-region replicas      │  │         Certificates: alongside ACM         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auto-rotation uses Lambda to update the secret and the target service atomically.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Rotation Workflow               │  │               Access Patterns               │   │
│   │     1. createSecret: AWSPENDING version      │  │        SDK: get-secret-value API call       │   │
│   │       2. setSecret: update the service       │  │         Lambda env: inject at deploy        │   │
│   │       3. testSecret: verify new creds        │  │          ECS/EKS: secret reference          │   │
│   │     4. finishSecret: promote to CURRENT      │  │      CodeBuild: secret ID in buildspec      │   │
│   │       Schedule: days interval or cron        │  │       Cache: SDK caches for 5 minutes       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS KMS HSM · Secrets Manager regional API · Lambda rotation infrastructure                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Secret          = Encrypted credential or config value stored in Secrets Manager                     │
│  AWSCURRENT      = Version label for the current active version of a secret                           │
│  AWSPENDING      = Version label for the new secret during rotation; not yet current                  │
│  Rotation Lambda = Function that rotates the secret value and updates the target service              │
│  get-secret-value= SDK/CLI API that retrieves the plaintext secret value                              │
│  Resource policy = JSON policy on the secret allowing cross-account access                            │
│  Replication     = Cross-region replica; same secret value; independent rotation                      │
│  SDK caching     = AWS SDK caches secret for 5 min; reduces API calls and cost                        │
│  RDS integration = Built-in rotation for RDS; Lambda updates both secret and DB password              │
│  SSM Parameter Store= Simpler alternative; no auto-rotation; SecureString uses KMS                    │
│  Rotation schedule= Interval in days or cron expression for automatic rotation                        │
│  Secret ARN      = Unique identifier for the secret; used in IAM policy resource field                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Secrets Manager notes for day-to-day infrastructure operations.

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
