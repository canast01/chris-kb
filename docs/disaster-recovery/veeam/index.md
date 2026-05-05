# Veeam

## Overview

Veeam provides backup, replication, recovery, and disaster recovery capabilities for virtual, physical, and cloud workloads.

## Daily Checks

- Review failed backup jobs
- Check repository capacity
- Confirm restore points exist
- Validate replication jobs
- Review backup copy jobs

## Health Commands

```powershell
Get-VBRJob
Get-VBRBackup
Get-VBRRepository
Get-VBRSession | Sort-Object CreationTime -Descending | Select-Object -First 10
```

## Upgrade Workflow

1. Back up Veeam configuration database
2. Confirm version compatibility
3. Upgrade Veeam server
4. Upgrade proxies and repositories if required
5. Run test backup and restore validation
