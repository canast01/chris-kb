# AWS Access Keys


<div class="kb-summary">
AWS Access Keys reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────────── AWS Identity — Access Keys ──────────────────────────────────────┐
│                                                                                                       │
│  Long-term programmatic credentials: lifecycle, rotation, and replacement with roles.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Access Key Overview              │  │                    Risks                    │   │
│   │         ID + secret: permanent creds         │  │         Long-lived: exposure window         │   │
│   │           Max 2 keys per IAM user            │  │           Leaked: GitHub/log/code           │   │
│   │           Used: CLI/SDK/API calls            │  │         No MFA: bypasses console MFA        │   │
│   │          Status: Active or Inactive          │  │           Root keys: highest risk           │   │
│   │           Rotation: 90-day policy            │  │           No auto-expiry built-in           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Replace access keys with IAM roles wherever possible; keys only for legacy systems                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Rotation Process               │  │                 Alternatives                │   │
│   │              1. Create new key               │  │          IAM roles: no static keys          │   │
│   │           2. Update all consumers            │  │          OIDC: GitHub Actions / EKS         │   │
│   │            3. Deactivate old key             │  │         Instance profile: EC2 roles         │   │
│   │            4. Monitor: no denials            │  │         Secrets Manager: auto-rotate        │   │
│   │              5. Delete old key               │  │           CyberArk: PAM vault keys          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IAM service (global) · STS · CloudTrail · Secrets Manager · GuardDuty                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Access key ID   = 20-char identifier starting with AKIA; public part of credential                   │
│  Secret access key= 40-char secret; shown once at creation; never retrievable again                   │
│  Inactive status = Key exists but rejected; use during rotation test period                           │
│  Rotation        = Creating new key, updating consumers, deleting old key                             │
│  Root access key = Key for root account; delete immediately; use roles instead                        │
│  OIDC            = OpenID Connect; allows services to assume IAM roles without keys                   │
│  Instance profile= Wrapper attaching IAM role to EC2; provides temp credentials                       │
│  Credential report= IAM report listing all keys, last-used date, and rotation age                     │
│  GuardDuty       = Detects access key use from unusual locations or TOR nodes                         │
│  Secrets Manager = Stores and auto-rotates access keys for legacy integrations                        │
│  90-day policy   = Config rule flagging keys older than 90 days as NonCompliant                       │
│  AKIA prefix     = Indicates long-term access key; ASIA prefix = temporary STS key                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── AWS Identity — Access Keys ──────────────────────────────────────┐
│                                                                                                       │
│  Long-term programmatic credentials: lifecycle, rotation, and replacement with roles.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Access Key Overview              │  │                    Risks                    │   │
│   │         ID + secret: permanent creds         │  │         Long-lived: exposure window         │   │
│   │           Max 2 keys per IAM user            │  │           Leaked: GitHub/log/code           │   │
│   │           Used: CLI/SDK/API calls            │  │         No MFA: bypasses console MFA        │   │
│   │          Status: Active or Inactive          │  │           Root keys: highest risk           │   │
│   │           Rotation: 90-day policy            │  │           No auto-expiry built-in           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Replace access keys with IAM roles wherever possible; keys only for legacy systems                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Rotation Process               │  │                 Alternatives                │   │
│   │              1. Create new key               │  │          IAM roles: no static keys          │   │
│   │           2. Update all consumers            │  │          OIDC: GitHub Actions / EKS         │   │
│   │            3. Deactivate old key             │  │         Instance profile: EC2 roles         │   │
│   │            4. Monitor: no denials            │  │         Secrets Manager: auto-rotate        │   │
│   │              5. Delete old key               │  │           CyberArk: PAM vault keys          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IAM service (global) · STS · CloudTrail · Secrets Manager · GuardDuty                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Access key ID   = 20-char identifier starting with AKIA; public part of credential                   │
│  Secret access key= 40-char secret; shown once at creation; never retrievable again                   │
│  Inactive status = Key exists but rejected; use during rotation test period                           │
│  Rotation        = Creating new key, updating consumers, deleting old key                             │
│  Root access key = Key for root account; delete immediately; use roles instead                        │
│  OIDC            = OpenID Connect; allows services to assume IAM roles without keys                   │
│  Instance profile= Wrapper attaching IAM role to EC2; provides temp credentials                       │
│  Credential report= IAM report listing all keys, last-used date, and rotation age                     │
│  GuardDuty       = Detects access key use from unusual locations or TOR nodes                         │
│  Secrets Manager = Stores and auto-rotates access keys for legacy integrations                        │
│  90-day policy   = Config rule flagging keys older than 90 days as NonCompliant                       │
│  AKIA prefix     = Indicates long-term access key; ASIA prefix = temporary STS key                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Access Keys notes for day-to-day infrastructure operations.

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
