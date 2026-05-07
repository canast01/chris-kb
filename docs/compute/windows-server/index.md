# Windows Server


## Overview

Windows Server provides core operating system services for enterprise workloads, including Active Directory, file services, DNS, DHCP, IIS, application hosting, and infrastructure management.

## Daily Checks

- Review Event Viewer critical and error logs
- Check disk capacity
- Verify Windows services are running
- Confirm backup status
- Review patch compliance

## Health Commands

```powershell
Get-Service | Where-Object Status -ne Running
Get-EventLog -LogName System -EntryType Error -Newest 20
Get-PSDrive -PSProvider FileSystem
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

## Upgrade Workflow

1. Confirm application compatibility
2. Verify backup and rollback plan
3. Apply patches or upgrade during maintenance window
4. Reboot and validate services
5. Confirm monitoring and backups are healthy
