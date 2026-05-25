# AWS FSx
## Overview

AWS FSx notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│                  FSx Variants                           │
│                                                         │
│  FSx for Windows File Server                            │
│  ├── Protocol: SMB (2.1 / 3.0 / 3.1.1)                  │
│  ├── AD-integrated (user auth via AD groups)            │
│  └── Use: Windows apps · DFS shares · home dirs         │
│                                                         │
│  FSx for Lustre                                         │
│  ├── Protocol: POSIX (Lustre client)                    │
│  ├── Throughput: hundreds of GB/s · millions IOPS       │
│  └── Use: HPC · ML training · video processing          │
│                                                         │
│  FSx for NetApp ONTAP                                   │
│  ├── Protocol: NFS · SMB · iSCSI                        │
│  ├── Features: SnapMirror · dedup · thin provision      │
│  └── Use: enterprise storage migration · multi-protocol │
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
