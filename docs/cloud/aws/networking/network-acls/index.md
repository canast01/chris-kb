# AWS Network ACLs
## Overview

AWS Network ACLs notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│              Network ACL (stateless, per subnet)        │
│                                                         │
│  Evaluated in rule number order — lowest wins           │
│  Both inbound AND outbound rules required               │
│                                                         │
│  Example inbound rules:                                 │
│  ┌──────┬──────────┬────────────┬────────────────────┐  │
│  │ Rule │ Protocol │ Source     │ Allow / Deny        │  │
│  ├──────┼──────────┼────────────┼────────────────────┤  │
│  │ 100  │ TCP/443  │ 0.0.0.0/0  │ ALLOW              │  │
│  │ 110  │ TCP/22   │ 10.0.0.0/8 │ ALLOW              │  │
│  │ *    │ ALL      │ 0.0.0.0/0  │ DENY (implicit)    │  │
│  └──────┴──────────┴────────────┴────────────────────┘  │
│                                                         │
│  vs Security Groups: NACLs are stateless — ephemeral    │
│  return ports must also be explicitly allowed           │
└─────────────────────────────────────────────────────────┘
```

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
