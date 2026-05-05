# Server Reboot Runbook

## Overview

This runbook provides a safe process for rebooting servers during maintenance or troubleshooting.

## Pre-Checks

- Confirm maintenance approval
- Verify backups completed
- Check logged-in users
- Confirm application owner awareness

## Commands

```bash
who
uptime
systemctl --failed
sudo reboot
```

## Validation

1. Confirm server responds to ping
2. Confirm SSH or RDP access
3. Validate services
4. Review system logs
