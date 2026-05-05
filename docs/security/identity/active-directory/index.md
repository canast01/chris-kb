# Active Directory

## Overview

Active Directory provides centralized authentication, authorization, and directory services for enterprise environments.

## Daily Checks

- Verify domain controller health
- Check replication status
- Review authentication failures
- Confirm DNS functionality

## Health Commands

```bash
dcdiag
repadmin /replsummary
netdom query fsmo
```

## Upgrade Workflow

1. Verify replication health
2. Backup system state
3. Upgrade domain controllers sequentially
4. Validate authentication and DNS
