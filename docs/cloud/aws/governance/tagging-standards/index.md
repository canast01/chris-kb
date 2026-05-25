# AWS Tagging Standards

```text
Tagging Standards: Mandatory Tags → Enforcement → Reporting
──────────────────────────────────────────────────────────────

  Mandatory Tags on every resource:
  ┌──────────────────────────────────────────────────────┐
  │  Key: env          Values: prod / staging / dev      │
  │  Key: owner        Values: team-name / email         │
  │  Key: cost-centre  Values: CC-XXX                    │
  │  Key: application  Values: app short name            │
  └──────────────────────────────────────────────────────┘
           │
           ▼ enforce via
  ┌──────────────────────────────────────────────────────┐
  │  Enforcement                                         │
  │  AWS Config rule: required-tags ─► NON_COMPLIANT     │
  │  SCP: deny resource create if tag missing (optional) │
  │  AWS Tag Policies (via Organizations)                │
  └──────────────────────────────────────────────────────┘
           │
           ▼ reporting via
  ┌──────────────────────────────────────────────────────┐
  │  Cost Explorer                                       │
  │  Group by tag ──► chargeback per team/cost-centre    │
  │  Tag coverage report ──► untagged resources flagged  │
  └──────────────────────────────────────────────────────┘
```

## Overview

AWS Tagging Standards notes for day-to-day infrastructure operations.

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
