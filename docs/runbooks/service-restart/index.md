# Service Restart Runbook

## Overview

This runbook provides a controlled process for restarting infrastructure or application services.

## Pre-Checks

- Confirm service owner approval
- Check active users or jobs
- Review recent alerts
- Confirm rollback plan

## Commands

```bash
systemctl status service-name
systemctl restart service-name
systemctl status service-name
journalctl -u service-name -n 50
```

## Validation

1. Confirm service running
2. Check application response
3. Review logs
4. Confirm monitoring is clear
