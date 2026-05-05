# CyberArk

## Overview

CyberArk manages privileged credentials, password rotation, and secure access to administrative systems.

## Daily Checks

- Review vault health
- Verify password rotation jobs
- Check failed login attempts
- Validate platform services

## Health Commands

```bash
Get-PASComponentSummary
Get-PASAccount
Get-PASSession
```

## Upgrade Workflow

1. Backup vault and configuration
2. Verify platform compatibility
3. Apply upgrade
4. Validate credential access and rotation
