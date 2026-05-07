# Linux Server


## Overview

Linux servers provide operating system services for applications, databases, automation, web platforms, monitoring tools, and infrastructure services.

## Daily Checks

- Check system load
- Review disk usage
- Confirm key services are running
- Review logs
- Validate patch status

## Health Commands

```bash
uptime
df -h
free -m
systemctl --failed
journalctl -p err -n 50
```

## Upgrade Workflow

1. Confirm package repositories
2. Verify backup or snapshot
3. Apply updates during maintenance window
4. Reboot if kernel or core packages changed
5. Validate services and logs
