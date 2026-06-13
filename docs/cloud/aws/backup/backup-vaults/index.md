---
tags:
  - aws
---
# AWS Backup Vaults


<div class="kb-summary">
AWS Backup Vaults reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌───────────────────────────────────── AWS Backup — Backup Vaults ──────────────────────────────────────┐
│                                                                                                       │
│  Backup vaults store recovery points; secured with KMS, access policies, and vault lock.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Vault Configuration              │  │                  Encryption                 │   │
│   │          Default vault: per account          │  │          KMS CMK: customer-managed          │   │
│   │          Custom vaults: by purpose           │  │         Key policy: who can decrypt         │   │
│   │          Regional: data sovereignty          │  │            Separate key per vault           │   │
│   │         Logical container: IAM gated         │  │             Key rotation: annual            │   │
│   │          Naming: env-purpose-region          │  │         Cross-acct: key grant needed        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Vault KMS key controls who can restore; access policy controls who can list/delete                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Policy                 │  │                  Vault Lock                 │   │
│   │           Resource policy on vault           │  │          Governance: admin override         │   │
│   │          Allow: specific IAM roles           │  │          Compliance: immutable lock         │   │
│   │             Deny: public access              │  │            Min retention enforced           │   │
│   │          Cross-acct: explicit allow          │  │           Max retention: optional           │   │
│   │         Audit: CloudTrail API calls          │  │          Compliance mode: immutable         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Backup storage (S3-backed) · KMS HSM · CloudTrail · IAM policy engine                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Default vault   = Auto-created vault per account; uses AWS-managed key                               │
│  Custom vault    = Admin-created vault with specific CMK and access policy                            │
│  CMK             = Customer-Managed Key in KMS; gives explicit control over access                    │
│  Key grant       = Permission allowing cross-account backup to use CMK for decryption                 │
│  Access policy   = Resource-based IAM policy on vault; controls list/restore/delete                   │
│  Vault lock      = Feature preventing recovery point deletion before retention expires                │
│  Governance mode = Vault lock allowing admin to remove lock before 72-hour grace                      │
│  Compliance mode = Vault lock permanent after grace period; cannot be unlocked                        │
│  Min retention   = Vault lock rule ensuring recovery points cannot expire early                       │
│  Max retention   = Optional lock rule capping maximum retention to limit cost                         │
│  Regional vault  = Vault exists in one region; cross-region requires copy rule                        │
│  Key rotation    = Annual CMK rotation; old key versions retained for decryption                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Backup Vaults notes for day-to-day infrastructure operations.

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

```bash
# Add environment-specific commands here
```

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
