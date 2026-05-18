# AWS KMS

```
┌──────────────────────────────────────────────────────────┐
│                KMS — Key Operations                      │
└──────────────────────────────────────────────────────────┘

  ┌──────────────────────┐
  │  CMK (Customer       │
  │  Managed Key)        │
  │  ┌────────────────┐  │
  │  │  Key Material  │  │  ◄── never leaves KMS HSM
  │  │  (stays in KMS)│  │
  │  └────────────────┘  │
  └──────────┬───────────┘
             │
      ┌──────┴───────────────┐
      ▼                      ▼
  GenerateDataKey         Encrypt / Decrypt
  API call                API call
  │                       │
  ▼                       ▼
  Returns:             Encrypt: plaintext ─► ciphertext
  - Plaintext key      Decrypt: ciphertext ─► plaintext
  - Encrypted key
  │
  ▼
  App encrypts data locally
  Stores encrypted key with data
  (envelope encryption)
             │
             ▼
  ┌──────────────────────┐
  │  CloudTrail          │
  │  every API call      │
  │  logged: who, when,  │
  │  which key, result   │
  └──────────────────────┘
  Auto key rotation: annually (aws kms enable-key-rotation)
```

## Overview

AWS KMS notes for day-to-day infrastructure operations.

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
