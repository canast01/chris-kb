# Patch Management

## Overview

Patch management keeps operating systems, applications, firmware, and infrastructure platforms secure and stable.

## Daily Checks

- Review missing critical patches
- Confirm failed patch jobs
- Check reboot pending status
- Review maintenance windows

## Health Commands

```powershell
Get-HotFix
Get-CimInstance Win32_QuickFixEngineering
```

## Workflow

1. Review patch scope
2. Confirm backups
3. Patch non-production first
4. Patch production during approved window
5. Validate services after reboot
