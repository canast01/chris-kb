# Log Retention Policy

## Overview

Log retention policies define how long logs are stored to support compliance, auditing, and incident investigations.

## Standard Retention Periods

- System logs: 30–90 days
- Security logs: 90–365 days
- Audit logs: 1–7 years

## Daily Checks

- Verify log rotation working
- Check storage capacity
- Confirm archive jobs completed

## Health Commands

```bash
logrotate -d /etc/logrotate.conf
df -h
ls -lh /var/log
```

## Validation Workflow

1. Confirm retention policy applied
2. Validate rotation schedule
3. Check archived logs accessible
4. Verify compliance requirements met
