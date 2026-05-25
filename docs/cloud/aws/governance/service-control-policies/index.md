# AWS Service Control Policies

```text
SCPs: Org Root → OU → Account → IAM Policy evaluation
──────────────────────────────────────────────────────────────

  Request arrives at AWS API
          │
          ▼
  ┌──────────────────────┐
  │  Root SCP            │ ── Deny? ──► ACCESS DENIED
  └──────────┬───────────┘
             │ allow
             ▼
  ┌──────────────────────┐
  │  OU SCP              │ ── Deny? ──► ACCESS DENIED
  └──────────┬───────────┘
             │ allow
             ▼
  ┌──────────────────────┐
  │  Account SCP         │ ── Deny? ──► ACCESS DENIED
  └──────────┬───────────┘
             │ allow (max permissions boundary set)
             ▼
  ┌──────────────────────┐
  │  IAM Policy          │ ── Allow? ──► ACCESS GRANTED
  │  (identity/resource) │ ── Deny? ───► ACCESS DENIED
  └──────────────────────┘

  Note: SCPs do not grant permissions — they only restrict.
  A SCP Allow + no IAM Allow = still denied.
```

## Overview

AWS Service Control Policies notes for day-to-day infrastructure operations.

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
